#include "resource.h"
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <ArduinoJson.h>

const String IoT_device_code = "123456";

const String API_SERVER_PROTOCALL = "http://";
const String API_SERVER_URL = "172.30.1.56:8080";
const String API_SERVER_RESTAPI_URI = "/api/iot/";
const String ssid = "2G_Twosome_P";
const String password = "Twosome1016";
long last_connected = 0;
DynamicJsonDocument locale_json(5000);
WiFiMulti wiFiMulti;

void setup()
{
    Wire.begin();
    Serial.begin(115200);
    int count = 0;
    while (count < 20)
    {
        if (wiFiMulti.run() == WL_CONNECTED)
        {
            Serial.println();
            Serial.println("Connected!");
            count = 30;
        }
        else
        {
            WiFi.mode(WIFI_STA);
            wiFiMulti.addAP(ssid.c_str(), password.c_str());
        }
        delay(500);
        Serial.print(".");
        count++;
    }
    Serial.println("Timed out.");
}

void loop()
{
    long now = millis();
    
    if (now >= last_connected + 1000)
    {
        last_connected = now;
        HTTPClient http;
        DynamicJsonDocument payload_json(3000);

        // http://domain/api/iot/<int:iot_code>
        Serial.println(API_SERVER_PROTOCALL + API_SERVER_URL + API_SERVER_RESTAPI_URI + IoT_device_code);
        http.begin(API_SERVER_PROTOCALL + API_SERVER_URL + API_SERVER_RESTAPI_URI + IoT_device_code); //Specify request destination
        int httpCode = http.GET();                                                                        //Send the request
        String payload = http.getString();                                                                   //Get the response payload
        Serial.println(payload);
        deserializeJson(payload_json, payload, DeserializationOption::NestingLimit(5));

        if (httpCode != 200)
        {
            Serial.println("Connect Error - payload: " + payload);
            Serial.println("httpCode : " + String(httpCode));
            Serial.println("");
        }
        else
        {
            String opcode = payload_json["opcode"];

            Serial.println("opcode:" + opcode);
            Serial.println("");
        }
        http.end(); //Close connection
    }
}
