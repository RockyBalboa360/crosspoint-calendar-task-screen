#pragma once

namespace calendar {

// Last successfully downloaded calendar image (BMP rendered by the calendar server).
constexpr char IMAGE_PATH[] = "/.crosspoint/calendar.bmp";

// Joins a saved WiFi network, downloads SETTINGS.calendarUrl to IMAGE_PATH and
// switches the radio off again. Returns true only when a new, valid image was
// stored; on any failure the previous image is kept.
bool refresh();

}  // namespace calendar
