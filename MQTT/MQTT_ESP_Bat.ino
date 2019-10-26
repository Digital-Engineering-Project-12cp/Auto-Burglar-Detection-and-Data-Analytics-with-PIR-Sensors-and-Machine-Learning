#include <ESP8266WiFi.h>
#include <DNSServer.h>
#include <ESP8266WebServer.h>
#include <WiFiManager.h>
#include <PubSubClient.h>
#include "FS.h"
#include <ArduinoJson.h>



//const char* mqtt_server = "192.168.0.102";
//const char* pub_topic = "/feeds/motion";

char mqtt_server[40];
char token[30] = "/feeds/moto";
const char* pub_topic = "";

WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

char message_buff[50];

const int analogInPin = A0;
int sensorValue = 0;
int switchPin = 5;
int pirPin = 4;

bool shouldSaveConfig = false;


void saveConfigCallback () {
  Serial.println("Should save config");
  shouldSaveConfig = true;
}


float battery_level(){

sensorValue = analogRead(analogInPin);
float averageADCRead = 1024;
float caliberationValue = 5.2 / averageADCRead;
float batteryLevel =  sensorValue  * caliberationValue;

return batteryLevel;
}


void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
  } else {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }

}


void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}





void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);



  if (!SPIFFS.begin()) {
    Serial.println("Failed to mount FS");
    return;
  }
  loadConfig();
  WiFiManagerParameter custommqttserver("server", "mqtt server", mqtt_server, 50);
  WiFiManagerParameter customtoken("token", "token", token, 35);

  WiFiManager wifiManager;
  wifiManager.setSaveConfigCallback(saveConfigCallback);

  wifiManager.addParameter(&custommqttserver);
  wifiManager.addParameter(&customtoken);






 //wifiManager.resetSettings();



  wifiManager.autoConnect("AutoConnectAP");

  wifiManager.setSTAStaticIPConfig(IPAddress(192,168,0,109), IPAddress(192,168,0,1), IPAddress(255,255,255,0));


  strcpy(mqtt_server, custommqttserver.getValue());
  strcpy(token, customtoken.getValue());


   if (shouldSaveConfig) {
    saveConfig();
    }
    pub_topic = token;
    delay(500);
    const char* mqttServer = mqtt_server;
    Serial.println("Connected.");
    client.setServer(mqtt_server, 1883);


}


bool loadConfig() {
  File configFile = SPIFFS.open("/config.json", "r");
  if (!configFile) {
    Serial.println("Failed to open config file");
    return false;
  }

  size_t size = configFile.size();
  if (size > 1024) {
    Serial.println("Config file size is too large");
    return false;
  }

  // Allocate a buffer to store contents of the file.
  std::unique_ptr<char[]> buf(new char[size]);

  configFile.readBytes(buf.get(), size);

  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& json = jsonBuffer.parseObject(buf.get());

  if (!json.success()) {
    Serial.println("Failed to parse config file");
    return false;
  }

  strcpy(mqtt_server, json["mqtt_server"]);
  strcpy(token, json["token"]);
  Serial.println("mqtt_server: ");
  Serial.println(mqtt_server);
  Serial.println("token: ");
  Serial.println(token);
  return true;
}



bool saveConfig() {
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& json = jsonBuffer.createObject();
  json["mqtt_server"] = mqtt_server;
  json["token"] = token;

  File configFile = SPIFFS.open("/config.json", "w");
  if (!configFile) {
    Serial.println("Failed to open config file for writing");
    return false;
  }

  json.printTo(configFile);
  configFile.close();
  return true;
}



void forceConfigMode() {
  Serial.println("Reset");
  WiFi.disconnect();
  Serial.println("Dq");
  delay(500);
  //ESP.restart();
  delay(5000);
}





void loop(){
  if (!client.connected()) {
    reconnect();
  }


  if (digitalRead(switchPin) == HIGH) {
    forceConfigMode();
    }

  if (digitalRead(switchPin) == LOW) {
  float batval = battery_level();
  String pubString = "Motion/" + String(batval);
  pubString.toCharArray(message_buff, pubString.length()+1);
  client.publish(pub_topic,message_buff);

  Serial.println("---");
  Serial.println("MotionHome/" + String(batval));

  delay(2000);
  Serial.println("\ngoing to sleep");
  delay(100);
  ESP.deepSleep(0);
  delay(100);
  Serial.println("\nsleep unsuccessful");



  }


}
