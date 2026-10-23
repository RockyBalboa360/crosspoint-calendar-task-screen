#pragma once
#include <cstdint>

#include "activities/Activity.h"

// Gallery for the low-battery screen: Left/Right (or swipe) browse the styles, Confirm keeps the shown one,
// Back leaves the setting unchanged.
class LowBatteryScreenActivity final : public Activity {
 public:
  explicit LowBatteryScreenActivity(GfxRenderer& renderer, MappedInputManager& mappedInput)
      : Activity("LowBatteryScreen", renderer, mappedInput) {}

  void onEnter() override;
  void loop() override;
  void render(RenderLock&&) override;

 private:
  void step(int delta);

  uint8_t index = 0;
};
