#pragma once
#include <cstdint>

#include "activities/Activity.h"

// Gallery for the low-battery screen. Swipe left/right or the page keys browse the styles; the two touch buttons
// at the bottom keep the shown style (Choose) or leave the setting unchanged (Cancel). The Back gesture, the Home
// key and a configured Confirm key work as well.
class LowBatteryScreenActivity final : public Activity {
 public:
  explicit LowBatteryScreenActivity(GfxRenderer& renderer, MappedInputManager& mappedInput)
      : Activity("LowBatteryScreen", renderer, mappedInput) {}

  void onEnter() override;
  void loop() override;
  void render(RenderLock&&) override;

 private:
  struct ButtonRects {
    int cancelX, chooseX, y, width, height;
  };
  ButtonRects buttonRects() const;
  void choose();
  void step(int delta);

  uint8_t index = 0;
};
