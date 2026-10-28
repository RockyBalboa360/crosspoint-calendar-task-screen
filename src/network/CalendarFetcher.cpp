#include "CalendarFetcher.h"

#include <Arduino.h>
#include <HalStorage.h>
#include <Logging.h>
#include <WiFi.h>

#include <ctime>
#include <string>
#include <vector>

#include "CrossPointSettings.h"
#include "HttpDownloader.h"
#include "WifiCredentialStore.h"

namespace calendar {
namespace {

constexpr char TMP_PATH[] = "/.crosspoint/calendar.tmp";
constexpr unsigned long CONNECT_TIMEOUT_MS = 12000;
constexpr size_t MAX_NETWORK_ATTEMPTS = 3;
// Any epoch before this means the system clock was never set (TLS certificates
// are validated against it).
constexpr time_t MIN_VALID_EPOCH = 1700000000;
constexpr unsigned long NTP_TIMEOUT_MS = 6000;

bool tryNetwork(const WifiCredential& cred) {
  LOG_DBG("CAL", "Connecting to %s", cred.ssid.c_str());
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true, true);
  delay(100);
  WiFi.setScanMethod(WIFI_ALL_CHANNEL_SCAN);
  WiFi.setSortMethod(WIFI_CONNECT_AP_BY_SIGNAL);
  if (cred.password.empty()) {
    WiFi.begin(cred.ssid.c_str());
  } else {
    WiFi.begin(cred.ssid.c_str(), cred.password.c_str());
  }

  const unsigned long start = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - start < CONNECT_TIMEOUT_MS) {
    delay(100);
  }
  return WiFi.status() == WL_CONNECTED;
}

// Tries the last used network first, then the other saved ones.
bool connectWifi() {
  if (WIFI_STORE.getCredentialCount() == 0) WIFI_STORE.loadFromFile();

  std::vector<WifiCredential> candidates;
  candidates.reserve(MAX_NETWORK_ATTEMPTS);
  const std::string last = WIFI_STORE.getLastConnectedSsid();
  if (!last.empty()) {
    if (auto cred = WIFI_STORE.findCredential(last)) candidates.push_back(*cred);
  }
  for (size_t i = 0; i < WIFI_STORE.getCredentialCount() && candidates.size() < MAX_NETWORK_ATTEMPTS; i++) {
    auto cred = WIFI_STORE.getCredentialAt(i);
    if (cred && cred->ssid != last) candidates.push_back(*cred);
  }
  if (candidates.empty()) {
    LOG_ERR("CAL", "No saved WiFi network");
    return false;
  }

  for (const auto& cred : candidates) {
    if (tryNetwork(cred)) return true;
  }
  LOG_ERR("CAL", "WiFi connection failed");
  return false;
}

// HTTPS verification needs a plausible wall clock; set it over SNTP if the RTC value was not applied.
void ensureClock() {
  if (time(nullptr) >= MIN_VALID_EPOCH) return;
  configTime(0, 0, "pool.ntp.org", "time.google.com");
  const unsigned long start = millis();
  while (time(nullptr) < MIN_VALID_EPOCH && millis() - start < NTP_TIMEOUT_MS) {
    delay(100);
  }
  LOG_DBG("CAL", "Clock %s", time(nullptr) >= MIN_VALID_EPOCH ? "set via NTP" : "still unset");
}

// BMP signature plus a plausible size; anything else (HTML error page, empty file) is rejected.
bool looksLikeBmp(const char* path) {
  HalFile file;
  if (!Storage.openFileForRead("CAL", path, file)) return false;
  uint8_t sig[2] = {0, 0};
  const bool ok = file.fileSize() > 1024 && file.read(sig, 2) == 2 && sig[0] == 'B' && sig[1] == 'M';
  file.close();
  return ok;
}

// Frees the WiFi driver's heap on every exit path so the bitmap decode that follows has it.
struct RadioOff {
  ~RadioOff() {
    if (WiFi.getMode() == WIFI_MODE_NULL) return;
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
  }
};

// Layout choice for the server: "?priority=...&count=N", joined with '&' when the URL already has a query.
std::string requestQuery(const std::string& url) {
  static constexpr const char* PRIORITIES[] = {"events", "events_n", "tasks_n", "tasks"};
  const uint8_t priority = SETTINGS.calendarPriority < 4 ? SETTINGS.calendarPriority : 1;
  char query[40];
  snprintf(query, sizeof(query), "%cpriority=%s&count=%u", url.find('?') == std::string::npos ? '?' : '&',
           PRIORITIES[priority], static_cast<unsigned>(SETTINGS.calendarCount));
  return query;
}

}  // namespace

bool refresh() {
  const RadioOff radioOff;
  std::string url = SETTINGS.calendarUrl;
  if (!url.empty()) url += requestQuery(url);
  if (url.empty()) {
    LOG_ERR("CAL", "No calendar URL configured");
    return false;
  }
  if (!connectWifi()) return false;
  ensureClock();

  if (ESP.getFreeHeap() < HttpDownloader::MIN_TLS_FREE_HEAP) {
    LOG_ERR("CAL", "Not enough heap for download: %u", static_cast<unsigned>(ESP.getFreeHeap()));
    return false;
  }

  Storage.remove(TMP_PATH);
  const auto result = HttpDownloader::downloadToFile(url, TMP_PATH);
  if (result != HttpDownloader::OK) {
    LOG_ERR("CAL", "Download failed (%d)", static_cast<int>(result));
    Storage.remove(TMP_PATH);
    return false;
  }
  if (!looksLikeBmp(TMP_PATH)) {
    LOG_ERR("CAL", "Downloaded file is not a BMP");
    Storage.remove(TMP_PATH);
    return false;
  }

  Storage.remove(IMAGE_PATH);
  if (!Storage.rename(TMP_PATH, IMAGE_PATH)) {
    LOG_ERR("CAL", "Could not store calendar image");
    return false;
  }
  LOG_DBG("CAL", "Calendar image updated");
  return true;
}

}  // namespace calendar
