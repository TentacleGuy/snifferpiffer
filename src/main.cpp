#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
 
// Flask-Server
const char* serverName = "http://192.168.178.60:5000/data"; 

// Konfiguration deines Heimnetzwerks (STA-Modus)
const char* ssid = "FRITZ!Box 6591 Cable PE";
const char* pw = "55835096080592791565";

// Konfiguration für den Access Point (AP-Modus)
const char* apSSID = "MeinESP32AP";
const char* apPW = "12345678";

// Zeitintervall für Datenaufzeichnung (in Millisekunden)
unsigned long previousMillis = 0;
const long interval = 5000;  // Alle 5 Sekunden

bool snifferActive = false;


void sendDataToServer(String data) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.178.60:5000/data");  // IP des Flask-Servers
    http.addHeader("Content-Type", "application/json");  // JSON-Daten
    
    String payload = "{\"data\":\"" + data + "\"}";  // Beispiel-Daten im JSON-Format
    int httpResponseCode = http.POST(payload);

    if (httpResponseCode <= 0) {
      Serial.print("Fehler beim Senden. HTTP Code: ");
      Serial.println(httpResponseCode);
    }
    http.end();  // Beende HTTP
  } else {
    Serial.println("Keine WLAN-Verbindung");
  }
}



void setAP(int status, const char* apPW, const char* apSSID) {
    switch(status) {
        case '1':
            // Starte den Access Point
            Serial.println("Starte Access Point...");
            WiFi.softAP(apSSID, apPW);
            Serial.print("AP IP-Adresse: ");
            Serial.println(WiFi.softAPIP());
            break;
        
        default:
            break;
    }
}

void setSTA(int status, const char* ssid, const char* pw) {
 if (status == 1) {
     Serial.println("Verbinde mit Heimnetzwerk...");
     WiFi.begin(ssid, pw);

     // Setze Timeout für die Verbindung auf 20 Sekunden (20000 ms)
     unsigned long startAttemptTime = millis();
     
     while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 20000) {
         delay(1000);
         Serial.println("Verbinde...");
     }

     if (WiFi.status() == WL_CONNECTED) {
         Serial.println("Verbunden mit Heimnetzwerk!");
         Serial.print("STA IP-Adresse: ");
         Serial.println(WiFi.localIP());
     } else {
         Serial.println("Fehler: Keine Verbindung zum WLAN hergestellt.");
     }
 }
}

void processCommand(String command) {
  if (command == "start") {
    snifferActive = true;
    Serial.println("Sniffer gestartet");
  } else if (command == "stop") {
    snifferActive = false;
    Serial.println("Sniffer gestoppt");
  }
}

void checkCommand() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.178.60:5000/command");
 
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      String command = http.getString();
      processCommand(command);
    } else {
      Serial.println("Fehler beim Abrufen des Befehls");
      Serial.println("Command: " + http.getString());
      Serial.println("HTTP Response Code: " + String(httpResponseCode));

    }
    http.end();
  } else {
    Serial.println("Keine WLAN-Verbindung");
  }
}

void setup() {
    Serial.begin(115200);

    WiFi.mode(WIFI_AP_STA);

    setAP(1, apPW, apSSID);

    if((ssid != NULL) && (pw != NULL)) {
        setSTA(1, ssid, pw);
    } else {
        Serial.println("noch kein PW für das Heimnnetzerk gesetzt");
    }

}

void loop() {


    unsigned long currentMillis = millis();
    if(currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
    checkCommand();
        if(snifferActive == true) {
            String data = String(random(1000)) + "Testdaten";
            sendDataToServer(data);
        } 
    }
}