#include "LowBatteryScreen.h"

#include <GfxRenderer.h>
#include <I18n.h>
#include <InflateReader.h>
#include <Logging.h>
#include <Memory.h>

#include <algorithm>
#include <cstdio>

#include "fontIds.h"
#include "images/LowBatteryArt.h"

namespace {

// Minimum screen size for the pictures: the art plus room for the text below it.
constexpr int MIN_SCREEN_WIDTH = lowbatteryart::WIDTH;
constexpr int MIN_SCREEN_HEIGHT = lowbatteryart::HEIGHT + 100;

// Inflates picture `index` into a temporary buffer and paints its ink pixels as horizontal runs.
bool drawArt(const GfxRenderer& renderer, const int index, const int originX) {
  auto raw = makeUniqueNoThrow<uint8_t[]>(lowbatteryart::RAW_BYTES);
  if (!raw) {
    LOG_ERR("LBS", "OOM: %u bytes", static_cast<unsigned>(lowbatteryart::RAW_BYTES));
    return false;
  }
  const auto& entry = lowbatteryart::ENTRIES[index];
  InflateReader reader;
  if (!reader.init(false)) return false;
  reader.setSource(entry.data, entry.size);
  if (!reader.read(raw.get(), lowbatteryart::RAW_BYTES)) {
    LOG_ERR("LBS", "Picture %d is corrupt", index + 1);
    return false;
  }

  constexpr int rowBytes = lowbatteryart::WIDTH / 8;
  for (int y = 0; y < lowbatteryart::HEIGHT; y++) {
    const uint8_t* row = raw.get() + static_cast<size_t>(y) * rowBytes;
    int runStart = -1;
    for (int x = 0; x <= lowbatteryart::WIDTH; x++) {
      const bool ink = x < lowbatteryart::WIDTH && (row[x >> 3] & (0x80 >> (x & 7)));
      if (ink && runStart < 0) {
        runStart = x;
      } else if (!ink && runStart >= 0) {
        renderer.fillRect(originX + runStart, y, x - runStart, 1, true);
        runStart = -1;
      }
    }
  }
  return true;
}

void drawPlainIcon(const GfxRenderer& renderer, const uint16_t percent) {
  const int pageWidth = renderer.getScreenWidth();
  const int pageHeight = renderer.getScreenHeight();
  constexpr int BODY_W = 240;
  constexpr int BODY_H = 120;
  constexpr int NUB_W = 20;
  constexpr int NUB_H = 50;
  constexpr int BORDER = 8;
  const int x = (pageWidth - BODY_W - NUB_W) / 2;
  const int y = pageHeight / 2 - 220;

  renderer.drawRect(x, y, BODY_W, BODY_H, BORDER, true);
  renderer.fillRect(x + BODY_W, y + (BODY_H - NUB_H) / 2, NUB_W, NUB_H, true);
  const int innerW = BODY_W - 2 * (BORDER + 4);
  const int fillW = std::max(8, innerW * std::min<int>(percent, 100) / 100);
  renderer.fillRect(x + BORDER + 4, y + BORDER + 4, fillW, BODY_H - 2 * (BORDER + 4), true);

  int textY = y + BODY_H + 50;
  renderer.drawCenteredText(UI_12_FONT_ID, textY, tr(STR_CALENDAR_LOW_BATTERY), true, EpdFontFamily::BOLD);
  textY += renderer.getLineHeight(UI_12_FONT_ID) + 10;
  char level[8];
  snprintf(level, sizeof(level), "%u%%", static_cast<unsigned>(percent));
  renderer.drawCenteredText(UI_12_FONT_ID, textY, level, true, EpdFontFamily::BOLD);
  textY += renderer.getLineHeight(UI_12_FONT_ID) + 30;
  for (const auto& line : renderer.wrappedText(UI_10_FONT_ID, tr(STR_CALENDAR_CHARGE_HINT), pageWidth - 80, 4)) {
    renderer.drawCenteredText(UI_10_FONT_ID, textY, line.c_str());
    textY += renderer.getLineHeight(UI_10_FONT_ID) + 4;
  }
}

}  // namespace

namespace lowbatteryscreen {

uint8_t styleCount() { return lowbatteryart::COUNT + 1; }

void draw(const GfxRenderer& renderer, const uint8_t style, const uint16_t percent) {
  const int pageWidth = renderer.getScreenWidth();
  const int pageHeight = renderer.getScreenHeight();
  const bool pictureFits = pageWidth >= MIN_SCREEN_WIDTH && pageHeight >= MIN_SCREEN_HEIGHT;
  if (style == 0 || style > lowbatteryart::COUNT || !pictureFits ||
      !drawArt(renderer, style - 1, (pageWidth - lowbatteryart::WIDTH) / 2)) {
    drawPlainIcon(renderer, percent);
    return;
  }

  // Text band under the picture: title with the charge level, then the hint.
  char title[48];
  snprintf(title, sizeof(title), "%s  %u%%", tr(STR_CALENDAR_LOW_BATTERY), static_cast<unsigned>(percent));
  int y = lowbatteryart::HEIGHT + 16;
  renderer.drawCenteredText(UI_12_FONT_ID, y, title, true, EpdFontFamily::BOLD);
  y += renderer.getLineHeight(UI_12_FONT_ID) + 10;
  for (const auto& line : renderer.wrappedText(UI_10_FONT_ID, tr(STR_CALENDAR_CHARGE_HINT), pageWidth - 60, 3)) {
    renderer.drawCenteredText(UI_10_FONT_ID, y, line.c_str());
    y += renderer.getLineHeight(UI_10_FONT_ID) + 2;
  }
}

}  // namespace lowbatteryscreen
