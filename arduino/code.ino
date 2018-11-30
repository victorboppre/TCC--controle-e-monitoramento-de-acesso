#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <PubSubClient.h> 

#define TOPIC "test321TCCeletricaEletronica"
#define MAX_STEPS 2048
#define STEP_1 D0
#define STEP_2 D1
#define STEP_3 D2
#define STEP_4 D3
//const char* ssid = "Rep. Jacto aqui vamos trabalhar";     //Rep. Jacto
//const char* password = "amoraes1621";

//const char* ssid = "Boppre";                              //
//const char* password = "3ss4c4rn33fr1bo1";

const char* ssid = "Victor";
const char* password = "victor123";

const char* BROKER_MQTT = "iot.eclipse.org"; 
const char* ID_MQTT = "uahseuhsaeuhasu";
int BROKER_PORT = 1883;

WiFiClient espClient;
PubSubClient MQTT(espClient);

void Open(boolean direction){int step = 0;
  for(int i = 0; i< MAX_STEPS; i++)
  {
    switch(step)
    {
      case 0:
         digitalWrite(STEP_1, LOW);
         digitalWrite(STEP_2, LOW);
         digitalWrite(STEP_3, LOW);
         digitalWrite(STEP_4, HIGH);
      break;

      case 1:
         digitalWrite(STEP_1, LOW);
         digitalWrite(STEP_2, LOW);
         digitalWrite(STEP_3, HIGH);
         digitalWrite(STEP_4, HIGH);
      break;

      case 2:
         digitalWrite(STEP_1, LOW);
         digitalWrite(STEP_2, LOW);
         digitalWrite(STEP_3, HIGH);
         digitalWrite(STEP_4, LOW);
      break;

      case 3:
         digitalWrite(STEP_1, LOW);
         digitalWrite(STEP_2, HIGH);
         digitalWrite(STEP_3, HIGH);
         digitalWrite(STEP_4, LOW);
      break;

      case 4:
         digitalWrite(STEP_1, LOW);
         digitalWrite(STEP_2, HIGH);
         digitalWrite(STEP_3, LOW);
         digitalWrite(STEP_4, LOW);
      break;

      case 5:
         digitalWrite(STEP_1, HIGH);
         digitalWrite(STEP_2, HIGH);
         digitalWrite(STEP_3, LOW);
         digitalWrite(STEP_4, LOW);
      break;

      case 6:
         digitalWrite(STEP_1, HIGH);
         digitalWrite(STEP_2, LOW);
         digitalWrite(STEP_3, LOW);
         digitalWrite(STEP_4, LOW);
      break;

      case 7:
         digitalWrite(STEP_1, HIGH);
         digitalWrite(STEP_2, LOW);
         digitalWrite(STEP_3, LOW);
         digitalWrite(STEP_4, HIGH);
      break;
    }
    if(!direction)
    {
      step++;
    }
    else
    {
      step--;  
    }
    delay(1);
    if(step == 8)
    {
      step = 0;
    }
    if(step == -1)
    {
      step = 7;
    }
  }
}
bool msgCompare(char *stringCompare)
{
 char c[4] = {'o','p','e','n'};
 for(int i = 0; i < 4; i++)
 {
    if(*stringCompare != c[i])
    {
       return false;
    }
    stringCompare ++;  
 } 
 Serial.println("msg received");
 delay(1000);
 MQTT.publish("test321TCCeletricaEletronica1", "Received");
 Open(true);
 for(int i =0; i< 10000; i++)
 {
   delay(1); 
 }
 Open(false);
 return true;
}
void msgReceived(char* topic, byte* payload, unsigned int length)
{
    char msg[10];
    for(int i = 0; i < length ; i++)
    {
      msg[i] = (char)payload[i];
    }
    for(int i = 0; i < length; i++)
    {
      Serial.print(msg[i]);
    }
    msgCompare(&msg[0]);
    Serial.println('.');
}
void VerificaConexoesWiFIEMQTT(void)
{
    if (!MQTT.connected()) 
        reconnectMQTT(); //se não há conexão com o Broker, a conexão é refeita
    
     //reconectWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}
void reconnectMQTT() 
{
    while (!MQTT.connected()) 
    {
        Serial.print("* Tentando se conectar ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) 
        {
            Serial.println("Conectado com sucesso ao broker MQTT!");
            MQTT.subscribe(TOPIC); 
        } 
        else 
        {
            Serial.println("Falha ao reconectar no broker.");
            Serial.println("Havera nova tentatica de conexao em 2s");
            delay(2000);
        }
    }
}
void setup() {
  pinMode(STEP_1,OUTPUT);
  pinMode(STEP_2,OUTPUT);
  pinMode(STEP_3,OUTPUT);
  pinMode(STEP_4,OUTPUT); 
  Serial.begin(115200);
  WiFi.mode(WIFI_STA); // Connect like Station mode (STA)
  WiFi.begin(ssid, password);
  Serial.println(""); // The serial method is only used as a simple debugger
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print('.');  
  }
  Serial.println("\n\n***Connected***\n\n");
  Serial.println(WiFi.localIP());
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  //this method will set the callback when a msg is received.
  MQTT.setCallback(msgReceived);
}

void loop() {
  VerificaConexoesWiFIEMQTT();
  delay(1);
  MQTT.loop();
}
