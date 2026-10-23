# Kalender-Ruhebildschirm für den Xteink X4 Pro

**Inoffizieller Fork von [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) 1.6.5.**
Der Xteink X4 Pro zeigt als Ruhebildschirm deine Tagesansicht: Wetter für zwei Orte, die
Termine von heute aus Google Kalender und die Aufgaben von heute aus Todoist.

<p align="center">
  <img src="docs/example-calendar-screen.png" alt="Beispiel: Wetter für Berlin und Frankfurt, Termine und Aufgaben (Platzhalterdaten)" width="320"><br>
  <em>Beispielbild mit Platzhalterdaten, so wie es auf dem Display erscheint (480x800, Graustufen)</em>
</p>

> Kein offizielles Projekt. Keine Verbindung zum CrossPoint-Reader-Projekt oder zu Xteink.
> Getestet auf einem X4 Pro, Nutzung auf eigene Gefahr, keine Gewährleistung.

## Wie es funktioniert
1. Ein kleiner **Server** (Cloudflare Worker) holt Wetter, Termine und Aufgaben und zeichnet daraus
   ein Bild: [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen).
2. Diese **Firmware** hat dafür einen neuen Ruhebildschirm **„Calendar“** und die Einstellung
   **„Calendar Server URL“**.
3. Wenn das Gerät einschläft, verbindet es sich mit deinem gespeicherten WLAN, lädt das Bild von der
   URL und zeigt es als Ruhebildschirm an. Schlägt das fehl, bleibt das zuletzt geladene Bild stehen.

## Installation
1. Lade die `firmware.bin` aus den [Releases](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)
   herunter und kopiere sie auf die SD-Karte (Hauptverzeichnis).
2. Am Gerät: *Einstellungen → System → SD Card Firmware Update*, Datei auswählen und bestätigen.
   Die bisherige Firmware bleibt im zweiten Programmspeicher erhalten.
3. *Einstellungen → System → WiFi Networks*: dein WLAN speichern.
4. *Einstellungen → Display → Calendar Server URL*: die Adresse deines Workers eintragen
   (zum Beispiel `https://dein-worker.dein-name.workers.dev`).
5. *Einstellungen → Display → Sleep Screen → Calendar* wählen.

Die Einrichtung des Workers (Google-Dienstkonto, Todoist-Token, Orte) steht in dessen
[README](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen#readme).

## Gut zu wissen
- Das Bild wird **beim Einschlafen** geladen, von Hand oder nach der eingestellten Zeit ohne
  Bedienung. Danach bleibt es stehen, bis du das Gerät aufweckst und erneut einschlafen lässt. Ein
  zeitgesteuertes Aufwachen gibt es nicht.
- Liegt der Akku unter **10 %**, lädt das Gerät nichts herunter. Stattdessen erscheint ein Warnbild
  „Akku schwach“ mit der Ladestandsanzeige. Nach dem Laden wird der Kalender beim nächsten
  Einschlafen wieder aktualisiert.
- Das Bild muss ein BMP mit 480x800 Pixeln sein. Der Worker liefert genau das.
- Die Adresse deines Workers ist öffentlich erreichbar. Wer sie kennt, sieht deine Termine und
  Aufgaben. Gib sie nicht weiter.
- Ein Update über „Check for updates“ ersetzt diese Firmware wieder durch die offizielle.

## Was sich gegenüber CrossPoint 1.6.5 ändert
Neu sind `src/network/CalendarFetcher.{h,cpp}` sowie kleine Anpassungen in `SleepActivity`,
`SettingsActivity`, den Einstellungen und den Übersetzungen (Englisch und Deutsch). Alles andere ist
unverändert. Die genaue Liste, die Bauanleitung und alle Lizenzen stehen in
[FORK_NOTICE.md](FORK_NOTICE.md). Die Anleitung des Originals liegt in
[USER_GUIDE.md](USER_GUIDE.md).

## Selbst bauen
```
git clone --recurse-submodules https://github.com/RockyBalboa360/crosspoint-calendar-task-screen
cd crosspoint-calendar-task-screen
pio run -e x4pro-gh_release
```
Die fertige Datei liegt danach unter `.pio/build/x4pro-gh_release/firmware.bin`.

## Rechtliches und Quellen
- Basis ist **CrossPoint Reader** (MIT, Copyright (c) 2025 CrossPoint Reader organization). Die Datei
  [LICENSE](LICENSE) ist unverändert. Meine Änderungen stehen ebenfalls unter MIT.
- In der Firmware stecken Bibliotheken mit eigenen Lizenzen, darunter **wolfSSL (GPL-2.0 oder neuer)**
  und arduinoWebSockets (LGPL-2.1). Die Lizenztexte liegen in
  [third_party_licenses/](third_party_licenses/), die Quellen und Versionen in
  [FORK_NOTICE.md](FORK_NOTICE.md).
- „Xteink“ und „CrossPoint“ sind Namen ihrer jeweiligen Inhaber und werden hier nur beschreibend
  verwendet.
- Die Änderungen entstanden mit Unterstützung von Claude Code (Anthropic) und wurden vom
  Repository-Inhaber geprüft und veröffentlicht.

---

## English summary
Unofficial fork of **CrossPoint Reader 1.6.5** for the **Xteink X4 Pro**. It adds a **Calendar** sleep
screen: before the device sleeps it downloads a 480x800 BMP from a configurable **Calendar Server URL**
and shows it (weather for two locations, today's Google Calendar events and Todoist tasks, rendered
by [this Cloudflare Worker](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen)).
Install `firmware.bin` from the [Releases](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)
via *Settings → System → SD Card Firmware Update*, then set the URL under *Settings → Display* and choose
*Sleep Screen → Calendar*. Not affiliated with the CrossPoint Reader organization or Xteink; see
[FORK_NOTICE.md](FORK_NOTICE.md) for changes, sources and licenses. Original project:
<https://github.com/crosspoint-reader/crosspoint-reader>.
