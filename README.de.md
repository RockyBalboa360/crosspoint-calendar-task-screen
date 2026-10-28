[English](README.md) · **Deutsch** · [Français](README.fr.md) · [Español](README.es.md)

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

**Zwei Teile, die zusammengehören:**
- 🧩 **Firmware** (dieses Repository): [crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/tree/feature/calendar-sleep-screen), **aktuelles Release: [Releases](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)**
- ☁️ **Bildserver** (Cloudflare Worker): [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen)

## Wie es funktioniert
1. Ein kleiner **Server** (Cloudflare Worker) holt Wetter, Termine und Aufgaben und zeichnet daraus
   ein Bild: [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen).
2. Diese **Firmware** hat dafür einen neuen Ruhebildschirm **„Calendar“** und die Einstellung
   **„Calendar Server URL“**.
3. Wenn das Gerät einschläft, verbindet es sich mit deinem gespeicherten WLAN, lädt das Bild von der
   URL und zeigt es als Ruhebildschirm an. Schlägt das fehl, bleibt das zuletzt geladene Bild stehen.

## Installation
1. Lade die `firmware.bin` aus dem [aktuellen Release](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases)
   herunter und kopiere sie auf die SD-Karte (Hauptverzeichnis).
2. Am Gerät: *Einstellungen → System → SD Card Firmware Update*, Datei auswählen und bestätigen.
   Die bisherige Firmware bleibt im zweiten Programmspeicher erhalten.
3. *Einstellungen → System → WiFi Networks*: dein WLAN speichern.
4. *Einstellungen → Display → Calendar Server URL*: die Adresse deines Workers eintragen
   (zum Beispiel `https://dein-worker.dein-name.workers.dev`).
5. *Einstellungen → Display → Sleep Screen → Calendar* wählen.

Die Einrichtung des Workers (Google-Dienstkonto, Todoist-Token, Orte) steht in dessen
[README](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen#readme).

## Termine oder Aufgaben zuerst?
Termine und Aufgaben teilen sich den Platz unter dem Wetter. Unter *Einstellungen → Display* legst du fest, wer ihn zuerst bekommt:

| *Kalender-Priorität* | Wirkung |
|---|---|
| *Alle Termine* | alle heutigen Termine, die Aufgaben bekommen den Rest |
| *Feste Terminzahl* | genau N Termine, die Aufgaben bekommen den Rest (Standard, N = 3) |
| *Feste Aufgabenzahl* | genau N Aufgaben, die Termine bekommen den Rest |
| *Alle Aufgaben* | alle Aufgaben, die Termine bekommen den Rest |

*Feste Anzahl* legt N fest (1 bis 8). Passt nicht alles in den Platz, steht am Ende der Rubrik „+N weitere“. Eine
leere Rubrik belegt nur eine Zeile.

<p align="center">
  <img src="docs/layout-priorities.png" alt="Die vier Layouts: alle Termine, feste Terminzahl, feste Aufgabenzahl, alle Aufgaben" width="100%"><br>
  <em>Die vier Layouts (von links): alle Termine, 2 Termine, 3 Aufgaben, alle Aufgaben</em>
</p>

Die Firmware hängt die Wahl als `?priority=…&count=…` an die Server-URL. Dafür brauchst du den aktuellen Worker; ein
älterer Worker ignoriert sie und behält sein festes Layout.

## Gut zu wissen
- Das Bild wird **beim Einschlafen** geladen, von Hand oder nach der eingestellten Zeit ohne
  Bedienung. Danach bleibt es stehen, bis du das Gerät aufweckst und erneut einschlafen lässt. Ein
  zeitgesteuertes Aufwachen gibt es nicht.
- Liegt der Akku unter **10 %**, lädt das Gerät nichts herunter. Stattdessen erscheint ein Warnbild
  „Akku schwach“ mit der Ladestandsanzeige. Nach dem Laden wird der Kalender beim nächsten
  Einschlafen wieder aktualisiert.
- Das **Warnbild bei niedrigem Akku** wählst du unter *Einstellungen → Display → Warnbild bei leerem Akku*:
  eine Galerie mit dem schlichten Akku-Symbol und **16 Zeichnungen** (ein klassischer Akku, 3 futuristische Schaltkreis-Motive, 9 Cartoons und 3 Steampunk-Motive).
  Mit Wischen oder den Seitentasten blätterst du, die Tasten „Wählen“ und „Abbrechen“ am unteren Rand (per Berührung) übernehmen das gezeigte Bild oder verlassen die Galerie.
- Das Bild muss ein BMP mit 480x800 Pixeln sein. Der Worker liefert genau das.
- Die Adresse deines Workers ist öffentlich erreichbar. Wer sie kennt, sieht deine Termine und
  Aufgaben. Gib sie nicht weiter.
- Ein Update über „Check for updates“ ersetzt diese Firmware wieder durch die offizielle.

<p align="center">
  <img src="docs/lowbattery-screens.png" alt="Die 16 Warnbilder bei niedrigem Akku" width="640"><br>
  <em>Die 16 Warnbilder zur Auswahl (unter jedem Bild zeigt das Gerät „Akku schwach“ und den Ladestand)</em>
</p>

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
git checkout feature/calendar-sleep-screen
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

Originalprojekt: <https://github.com/crosspoint-reader/crosspoint-reader>
