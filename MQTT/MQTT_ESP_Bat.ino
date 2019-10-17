#include <ESP8266WiFi.h>
#include <PubSubClient.h>



// Update these with values suitable for your network.

const char* ssid = "nowire";
const char* password = "dontaskmeagain";
const char* mqtt_server = "192.168.0.106";
const char* pub_topic = "/feeds/motion";

//Static IP address configuration
IPAddress staticIP(192, 168, 0, 109); //ESP static ip
IPAddress gateway(192, 168, 0, 1);   //IP Address of your WiFi Router (Gateway)
IPAddress subnet(255, 255, 255, 0);  //Subnet mask
IPAddress dns(0, 0, 0, 0);  //DNS

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;


char message_buff[50];
char message_buff1[50];

int pirPin = 4;
int ledPin = 2;    // the digital pin connected to built-in LED
int switchPin = 5;
bool switchStatus = false;
int sensorValue = 0;
const int analogInPin = A0;

float battery_level(){

sensorValue = analogRead(analogInPin);
float averageADCRead = 1024;
float caliberationValue = 5.2 / averageADCRead;
float batteryLevel =  sensorValue  * caliberationValue;

return batteryLevel;
}



void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.config(staticIP, subnet, gateway);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(20);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
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
  setup_wifi();
   pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  digitalWrite(pirPin, LOW);
  pinMode(switchPin, INPUT_PULLUP);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);
  
  client.setServer(mqtt_server, 1883);
  //client.setCallback(callback);

    if (!client.connected()) {
    reconnect();
  }
  // client.publish(pub_topic, "motion/home");

 if(digitalRead(switchPin) == LOW){

          float batval = battery_level();
          String pubString = "MotionHome/" + String(batval);
          pubString.toCharArray(message_buff, pubString.length()+1);
          client.publish(pub_topic,message_buff);
 
          Serial.println("---");
          Serial.println("MotionHome/" + String(batval));
          

       }
       else {
        if(digitalRead(switchPin) == HIGH){
          float batval1 = battery_level();
          String pubString1 = "MotionAway/" + String(batval1);
          pubString1.toCharArray(message_buff1, pubString1.length()+1);
          
          client.publish(pub_topic,message_buff1);
        
         Serial.println("---");
         Serial.println("MotionAway/" + String(batval1));
       
        }


       }


  delay(2000);
  Serial.println("\ngoing to sleep");
  delay(100);
  ESP.deepSleep(0);
  delay(100);
  Serial.println("\nsleep unsuccessful");

 
}

void loop() {


}
