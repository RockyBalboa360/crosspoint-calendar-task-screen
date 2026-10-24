#include "LowBatteryScreenActivity.h"

#include <GfxRenderer.h>
#include <HalDisplay.h>
#include <I18n.h>

#include <cstdio>

#include "CrossPointSettings.h"
#include "MappedInputManager.h"
#include "fontIds.h"
#include "util/LowBatteryScreen.h"

namespace {
// Charge level shown in the preview.
constexpr uint16_t PREVIEW_PERCENT = 7;
constexpr int BUTTON_BAND_HEIGHT = 120;
constexpr int BUTTON_HEIGHT = 48;
constexpr int BUTTON_MARGIN = 20;
constexpr int BUTTON_GAP = 16;
}  // namespace

void LowBatteryScreenActivity::onEnter() {
  Activity::onEnter();
  index = SETTINGS.lowBatteryScreen < lowbatteryscreen::styleCount() ? SETTINGS.lowBatteryScreen : 0;
  requestUpdate(true);
}

LowBatteryScreenActivity::ButtonRects LowBatteryScreenActivity::buttonRects() const {
  const int width = renderer.getScreenWidth();
  const int buttonWidth = (width - 2 * BUTTON_MARGIN - BUTTON_GAP) / 2;
  return {BUTTON_MARGIN, BUTTON_MARGIN + buttonWidth + BUTTON_GAP, renderer.getScreenHeight() - BUTTON_HEIGHT - 14,
          buttonWidth, BUTTON_HEIGHT};
}

void LowBatteryScreenActivity::choose() {
  SETTINGS.lowBatteryScreen = index;
  SETTINGS.saveToFile();
  finish();
}

void LowBatteryScreenActivity::step(const int delta) {
  const int count = lowbatteryscreen::styleCount();
  index = static_cast<uint8_t>((index + delta + count) % count);
  requestUpdate();
}

void LowBatteryScreenActivity::loop() {
  const auto rects = buttonRects();
  if (mappedInput.wasReleased(MappedInputManager::Button::Back) ||
      mappedInput.wasTapInRect(rects.cancelX, rects.y, rects.width, rects.height)) {
    finish();
    return;
  }
  if (mappedInput.wasReleased(MappedInputManager::Button::Confirm) ||
      mappedInput.wasTapInRect(rects.chooseX, rects.y, rects.width, rects.height)) {
    choose();
    return;
  }
  const auto swipe = mappedInput.wasSwipe();
  if (mappedInput.wasReleased(MappedInputManager::Button::Right) ||
      mappedInput.wasReleased(MappedInputManager::Button::Down) ||
      mappedInput.wasReleased(MappedInputManager::Button::PageForward) || swipe == MappedInputManager::SwipeDir::Left) {
    step(1);
  } else if (mappedInput.wasReleased(MappedInputManager::Button::Left) ||
             mappedInput.wasReleased(MappedInputManager::Button::Up) ||
             mappedInput.wasReleased(MappedInputManager::Button::PageBack) ||
             swipe == MappedInputManager::SwipeDir::Right) {
    step(-1);
  }
}

void LowBatteryScreenActivity::render(RenderLock&&) {
  renderer.clearScreen();
  lowbatteryscreen::draw(renderer, index, PREVIEW_PERCENT, BUTTON_BAND_HEIGHT);

  const auto rects = buttonRects();
  // Position and hint above the two buttons.
  char info[64];
  snprintf(info, sizeof(info), "%d / %d   %s", index + 1, lowbatteryscreen::styleCount(),
           tr(STR_LOW_BATTERY_GALLERY_HINT));
  renderer.drawCenteredText(SMALL_FONT_ID, rects.y - renderer.getLineHeight(SMALL_FONT_ID) - 8, info);

  const struct {
    int x;
    const char* label;
    int lineWidth;
  } buttons[] = {{rects.cancelX, tr(STR_CANCEL), 2}, {rects.chooseX, tr(STR_LOW_BATTERY_CHOOSE), 5}};
  for (const auto& button : buttons) {
    renderer.drawRoundedRect(button.x, rects.y, rects.width, rects.height, button.lineWidth, 12, true);
    const int textWidth = renderer.getTextWidth(UI_10_FONT_ID, button.label, EpdFontFamily::BOLD);
    renderer.drawText(UI_10_FONT_ID, button.x + (rects.width - textWidth) / 2,
                      rects.y + (rects.height - renderer.getLineHeight(UI_10_FONT_ID)) / 2, button.label, true,
                      EpdFontFamily::BOLD);
  }
  renderer.displayBuffer(HalDisplay::HALF_REFRESH);
}
