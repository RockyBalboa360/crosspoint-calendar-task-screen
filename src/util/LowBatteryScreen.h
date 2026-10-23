#pragma once
#include <cstdint>

class GfxRenderer;

namespace lowbatteryscreen {

// Number of selectable styles: 0 = plain battery icon, 1..N = pictures from images/LowBatteryArt.h.
uint8_t styleCount();

// Draws the low-battery screen for `style` into the framebuffer; the caller clears the screen and refreshes it.
// Pictures need a 480x720 or larger portrait screen and fall back to the plain icon otherwise.
void draw(const GfxRenderer& renderer, uint8_t style, uint16_t percent);

}  // namespace lowbatteryscreen
