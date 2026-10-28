**English** · [Deutsch](README.de.md) · [Français](README.fr.md) · [Español](README.es.md)

# Calendar sleep screen for the Xteink X4 Pro

**Unofficial fork of [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) 1.6.5.**
Your Xteink X4 Pro shows your day as its sleep screen: weather for two locations, today's events from
Google Calendar and today's tasks from Todoist.

<p align="center">
  <img src="docs/example-calendar-screen.png" alt="Example: weather for Berlin and Frankfurt, events and tasks (placeholder data)" width="320"><br>
  <em>Example image with placeholder data, exactly as it appears on the display (480x800, grayscale)</em>
</p>

> Not an official project. No connection to the CrossPoint Reader project or to Xteink.
> Tested on one X4 Pro, use at your own risk, no warranty.

**Two parts that belong together:**
- 🧩 **Firmware** (this repository): [crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/tree/feature/calendar-sleep-screen), **latest release: [Releases](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)**
- ☁️ **Image server** (Cloudflare Worker): [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen)

## How it works
1. A small **server** (Cloudflare Worker) fetches weather, events and tasks and draws them as an image:
   [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen).
2. This **firmware** adds a new sleep screen **"Calendar"** and the setting **"Calendar Server URL"**.
3. When the device goes to sleep, it connects to your saved WiFi, downloads the image from that URL and shows
   it as the sleep screen. If that fails, the last downloaded image stays.

## Installation
1. Download `firmware.bin` from the [latest release](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)
   and copy it to the root of the SD card.
2. On the device: *Settings → System → SD Card Firmware Update*, pick the file and confirm.
   The previous firmware stays in the second app slot.
3. *Settings → System → WiFi Networks*: save your WiFi.
4. *Settings → Display → Calendar Server URL*: enter the address of your worker
   (for example `https://your-worker.your-name.workers.dev`).
5. *Settings → Display → Sleep Screen → Calendar*.

Setting up the worker (Google service account, Todoist token, locations) is described in its
[README](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen#readme).

## Events or tasks first?
Events and tasks share the space below the weather. Under *Settings → Display* you decide who gets it first:

| *Calendar priority* | Effect |
|---|---|
| *All events* | all of today's events, tasks get the rest |
| *Fixed events* | exactly N events, tasks get the rest (default, N = 3) |
| *Fixed tasks* | exactly N tasks, events get the rest |
| *All tasks* | all tasks, events get the rest |

*Fixed count* sets N (1 to 8). If something does not fit, the section ends with "+N more" (shown as "+N weitere"
by the German worker). An empty section only takes one line.

<p align="center">
  <img src="docs/layout-priorities.png" alt="The four layouts: all events, fixed events, fixed tasks, all tasks" width="100%"><br>
  <em>The four layouts (left to right): all events, 2 events, 3 tasks, all tasks</em>
</p>

The firmware appends the choice to the server URL as `?priority=…&count=…`. This needs the current worker; an older
worker ignores it and keeps its fixed layout.

## Good to know
- The image is downloaded **when the device falls asleep**, by hand or after the idle timeout. It then stays until
  you wake the device and let it fall asleep again. There is no timed wake-up.
- Below **10 % battery** the device downloads nothing. It shows a "Battery low" picture with the charge level instead.
  After charging, the calendar is refreshed the next time the device goes to sleep.
- Choose the **low battery picture** under *Settings → Display → Low battery screen*: a gallery with the plain
  battery icon and **16 drawings** (a classic battery, 3 futuristic circuit designs, 9 cartoons and 3 steampunk
  designs). Swipe or use the side keys to browse; the touch buttons "Choose" and "Cancel" at the bottom accept the
  shown picture or leave the gallery.
- The image must be a 480x800 BMP. The worker delivers exactly that.
- The address of your worker is public. Anyone who knows it can see your events and tasks. Do not share it.
- Using "Check for updates" replaces this firmware with the official one again.

<p align="center">
  <img src="docs/lowbattery-screens.png" alt="The 16 low battery pictures" width="640"><br>
  <em>The 16 low battery pictures to choose from (under each picture the device shows "Battery low" and the charge level)</em>
</p>

## What changes compared to CrossPoint 1.6.5
New are `src/network/CalendarFetcher.{h,cpp}` and small changes in `SleepActivity`, `SettingsActivity`, the
settings and the translations (English and German). Everything else is unchanged. The exact list, build
instructions and all licenses are in [FORK_NOTICE.md](FORK_NOTICE.md). The original manual is
[USER_GUIDE.md](USER_GUIDE.md).

## Build it yourself
```
git clone --recurse-submodules https://github.com/RockyBalboa360/crosspoint-calendar-task-screen
cd crosspoint-calendar-task-screen
git checkout feature/calendar-sleep-screen
pio run -e x4pro-gh_release
```
The finished file is then at `.pio/build/x4pro-gh_release/firmware.bin`.

## Legal and sources
- Based on **CrossPoint Reader** (MIT, Copyright (c) 2025 CrossPoint Reader organization). The [LICENSE](LICENSE)
  file is unchanged. My changes are also MIT licensed.
- The firmware contains libraries with their own licenses, among them **wolfSSL (GPL-2.0 or later)** and
  arduinoWebSockets (LGPL-2.1). License texts are in [third_party_licenses/](third_party_licenses/), sources and
  versions in [FORK_NOTICE.md](FORK_NOTICE.md).
- "Xteink" and "CrossPoint" are names of their respective owners and are used here only descriptively.
- The changes were made with the help of Claude Code (Anthropic) and reviewed and published by the repository owner.

Original project: <https://github.com/crosspoint-reader/crosspoint-reader>
