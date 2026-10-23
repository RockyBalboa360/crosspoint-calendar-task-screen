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
}  // namespace

void LowBatteryScreenActivity::onEnter() {
  Activity::onEnter();
  index = SETTINGS.lowBatteryScreen < lowbatteryscreen::styleCount() ? SETTINGS.lowBatteryScreen : 0;
  requestUpdate(true);
}

void LowBatteryScreenActivity::step(const int delta) {
  const int count = lowbatteryscreen::styleCount();
  index = static_cast<uint8_t>((index + delta + count) % count);
  requestUpdate();
}

void LowBatteryScreenActivity::loop() {
  if (mappedInput.wasReleased(MappedInputManager::Button::Back)) {
    finish();
    return;
  }
  if (mappedInput.wasReleased(MappedInputManager::Button::Confirm)) {
    SETTINGS.lowBatteryScreen = index;
    SETTINGS.saveToFile();
    finish();
    return;
  }
  const auto swipe = mappedInput.wasSwipe();
  if (mappedInput.wasReleased(MappedInputManager::Button::Right) ||
      mappedInput.wasReleased(MappedInputManager::Button::Down) || swipe == MappedInputManager::SwipeDir::Left) {
    step(1);
  } else if (mappedInput.wasReleased(MappedInputManager::Button::Left) ||
             mappedInput.wasReleased(MappedInputManager::Button::Up) || swipe == MappedInputManager::SwipeDir::Right) {
    step(-1);
  }
}

void LowBatteryScreenActivity::render(RenderLock&&) {
  renderer.clearScreen();
  lowbatteryscreen::draw(renderer, index, PREVIEW_PERCENT);

  // Footer: position in the gallery and the key hint (small font, below the picture's own text).
  char position[32];
  snprintf(position, sizeof(position), "%d / %d", index + 1, lowbatteryscreen::styleCount());
  const int y = renderer.getScreenHeight() - renderer.getLineHeight(SMALL_FONT_ID) - 8;
  renderer.drawCenteredText(SMALL_FONT_ID, y - renderer.getLineHeight(SMALL_FONT_ID) - 2, position, true,
                            EpdFontFamily::BOLD);
  renderer.drawCenteredText(SMALL_FONT_ID, y, tr(STR_LOW_BATTERY_GALLERY_HINT));
  renderer.displayBuffer(HalDisplay::HALF_REFRESH);
}
