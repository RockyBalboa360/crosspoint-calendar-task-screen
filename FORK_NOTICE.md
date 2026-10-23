# Unofficial fork: calendar sleep screen for the Xteink X4 Pro

This is an **unofficial, personal fork** of
[CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) **v1.6.5**
(upstream commit `93e98bb78702e29868a16a13b80c40e6b36ccdff`). It is not affiliated with,
endorsed by, or supported by the CrossPoint Reader organization or Xteink. "Xteink" and
"CrossPoint" are names of their respective owners and are used here only to describe
compatibility. Please do not report problems of this fork to the upstream project.

## What this fork adds
A new sleep screen mode **Calendar** and a **Calendar Server URL** setting. Before the device
goes to sleep it joins a saved WiFi network, downloads a 480x800 BMP from the configured URL
to `/.crosspoint/calendar.bmp` and shows it as the sleep screen. If the download fails, the last
stored image is shown.

- `src/network/CalendarFetcher.{h,cpp}` (new): WiFi connect, download, BMP check
- `src/activities/boot_sleep/SleepActivity.{h,cpp}`: the Calendar sleep screen, and a fixed
  warning screen shown instead of the download when the battery is below 10 %
- `src/activities/settings/SettingsActivity.{h,cpp}`: "Calendar Server URL" entry (Display tab)
- `src/CrossPointSettings.h`, `src/SettingsList.h`: setting and enum value, also exposed in the
  web settings
- `lib/I18n/translations/{english,german}.yaml`: new strings
- `platformio.ini`: version string `1.6.5-calendar2`

A matching image server (Cloudflare Worker) is available at
<https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen>.

The idea of an "Calendar Mode" was first proposed upstream in
[pull request #408](https://github.com/crosspoint-reader/crosspoint-reader/pull/408) (closed, not
merged). This fork contains **no code taken from that pull request**; it is a separate, much
smaller implementation written against v1.6.5.

## Usage
1. Copy `firmware.bin` to the SD card and run *Settings → System → SD Card Firmware Update*.
2. *Settings → Display → Calendar Server URL*: enter the URL of your image server.
3. *Settings → Display → Sleep Screen → Calendar*.
4. Save your WiFi network under *Settings → System → WiFi Networks*.

The image is fetched when the device goes to sleep (manually or by timeout). There is no timed
wake-up. Tested on one Xteink X4 Pro only; use at your own risk, no warranty.

## Building
```
git clone --recurse-submodules https://github.com/RockyBalboa360/crosspoint-calendar-task-screen
cd crosspoint-calendar-task-screen
pio run -e x4pro-gh_release     # output: .pio/build/x4pro-gh_release/firmware.bin
```
The released `firmware.bin` was built from this repository at the release tag with PlatformIO
and the platform pinned in `platformio.ini` (pioarduino 55.03.311). On the build host the
PlatformIO library registry was not reachable, so the registry libraries were taken from their
GitHub sources at the same versions (via an untracked `platformio.local.ini`), and the
`greiman/SdFat` dependency declaration of the `SDCardManager` SDK library was dropped because
SdFat was supplied directly:

| Library | Version / source |
|---|---|
| ArduinoJson | v7.4.2 (github.com/bblanchon/ArduinoJson) |
| QRCode | v0.0.1 (github.com/ricmoo/QRCode) |
| PNGdec | 1.1.6 (github.com/bitbank2/PNGdec) |
| JPEGDEC | commit 86282979224c8a32fd51e091ed5a35b0c699a52b (as in `platformio.ini`) |
| arduinoWebSockets | commit 1c8b8deaca30b36494a4f6ea4df23ae862b21662 (= 2.7.3) |
| wolfSSL | 5.7.2 (github.com/wolfSSL/Arduino-wolfSSL) |
| SdFat | 2.3.1 (github.com/greiman/SdFat) |
| freeink-sdk (submodule) | commit 111fdcc7f0176c3ee38391a160ee296bf492dbd8 (github.com/Free-Ink/freeink-sdk) |

## Licenses and attribution
- **CrossPoint Reader** is MIT licensed, Copyright (c) 2025 CrossPoint Reader organization
  (see `LICENSE`, unchanged). The original authors keep the copyright in their code.
- **Modifications in this fork** (the files listed above): Copyright (c) 2026 RockyBalboa360,
  MIT, same terms as `LICENSE`.
- **FreeInk SDK** (submodule): MIT, Copyright (c) 2026 FreeInk; see its `LICENSE` and `NOTICE`
  (which in turn credits the OpenX4 E-Paper Community SDK, MIT).
- **Fonts, expat, miniz, uzlib, and other bundled code** keep the licenses stated in their source
  directories and headers (for example the SIL Open Font License for the Noto fonts under
  `lib/EpdFont/builtinFonts/source/`).
- **Libraries linked into the firmware binary** (license texts in `third_party_licenses/`):
  - **wolfSSL — GPL-2.0-or-later** (or a commercial license from wolfSSL Inc.)
  - **arduinoWebSockets — LGPL-2.1**
  - JPEGDEC and PNGdec — Apache-2.0, Copyright BitBank Software, Inc.
  - SdFat, ArduinoJson, QRCode — MIT
  - Arduino-ESP32 / ESP-IDF via the pioarduino platform — see their respective licenses
- **GPL note:** the released `firmware.bin` contains wolfSSL, which is licensed under the GPL.
  The binary is therefore distributed under the terms of the GPL as far as they apply to it. The
  complete corresponding source is this repository at the release tag, the `freeink-sdk`
  submodule commit and the library versions listed above. The upstream release binaries contain
  the same libraries.

## AI assistance
The changes in this fork were developed with the help of Claude Code (Anthropic) and reviewed
and published by the repository owner.
