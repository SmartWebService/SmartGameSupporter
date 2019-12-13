#include "resource.h"
#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <ArduinoJson.h>
#include <Servo.h>

const String IoT_device_code = "123456";
static const int servoPin = 13;

const String API_SERVER_PROTOCALL = "http://";
const String API_SERVER_URL = "192.168.33.70";
const String API_SERVER_RESTAPI_URI = "/api/iot/";
const String ssid = "KMU_SW";
const String password = "kookminsw";
long last_connected = 0;
WiFiMulti wiFiMulti;
Servo servo;

void setup()
{
    Wire.begin();
    Serial.begin(115200);
    servo.attach(servoPin);
    servo.write(0);

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
            int timer = payload_json["timer"];
            Serial.println(timer);

            if(opcode.equals("gaming")){
              if(timer <= 0){
                  Serial.println("Bombed!");
                  servo.write(180);
                  delay(100000000000000);
              }
            }
            

            Serial.println("opcode:" + opcode);
            Serial.println("");
        }
        http.end(); //Close connection
    }
}
