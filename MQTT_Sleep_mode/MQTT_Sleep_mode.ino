/*
 Basic ESP8266 MQTT PIR sketch

*/

#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

// Update these with values suitable for your network.

/********* WiFi Access Point ***********/

#define WLAN_SSID       "nowire"           // Wi-Fi network name
#define WLAN_PASS       "*******"           // Wi-Fi password

/********** MQTT Broker ************/

#define AIO_SERVER      "192.168.0.101"  // MQTT broker IP
#define AIO_SERVERPORT  1883             // MQTT broker port
#define AIO_USERNAME    ""           // MQTT username
#define AIO_KEY         ""           // MQTT password
#define AIO_CID         ""     // MQTT client ID


// Start a counter for serial logging and set the initial value to no motion
int counter = 0;
int previousReading = LOW;

WiFiClient client;
// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY, AIO_CID);

// Setup publish feeds - define topic name in parenthesis
Adafruit_MQTT_Publish status  = Adafruit_MQTT_Publish(&mqtt, AIO_CID "/feeds/motion");
Adafruit_MQTT_Publish motion_topic  = Adafruit_MQTT_Publish(&mqtt, AIO_CID "/feeds/motion");

long lastMsg = 0;
char msg[50];
int value = 0;

/////////////////////////////
//VARS
//the time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 0;

//the time when the sensor outputs a low impulse
long unsigned int lowIn;

//the amount of milliseconds the sensor has to be low
//before we assume all motion has stopped
long unsigned int pause = 5000;

boolean lockLow = true;
boolean takeLowTime;

int pirPin = 4;    // the digital pin connected to the PIR sensor's output
int ledPin = 2;    // the digital pin connected to built-in LED
int switchPin = 5;
bool switchStatus = false;


void MQTT_connect();

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

  // Setup a MQTT subscription


void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
 // status.publish("online");
}

void setup() {
  //pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  digitalWrite(pirPin, LOW);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);


MQTT_connect();

       if(digitalRead(switchPin) == LOW){

          motion_topic.publish("Motion/Home");
          Serial.println("---");
          Serial.println("Motion/Home");


       }
       else {
        if(digitalRead(switchPin) == HIGH){
          motion_topic.publish("Motion/Away");
         Serial.println("---");
         Serial.println("Motion/Away");
        }


       }

       delay(2000);
        Serial.println("Entering Deep Sleep");
       ESP.deepSleep(0);

  //give the sensor some time to calibrate



}

void loop() {
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.




}
