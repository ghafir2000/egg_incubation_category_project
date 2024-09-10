#include <DHT22.h>
#include <Wire.h>
#include <SoftwareSerial.h>
#include <Servo.h>


//define pin data

//heat and humiditiy sources 
#define inc_heater_pin 2
#define inc_humifier_pin 3

#define hat_heater_pin 4
#define hat_humifier_pin 5

// incubator windows def (dc motor)

// hatcher windows def (dc motor)
#define hat_win_r_up 6
#define hat_win_r_dn 7
#define hat_win_l_up 8
#define hat_win_l_dn 9

#define inc_win_r_up 14
#define inc_win_r_dn 15
#define inc_win_l_up 16
#define inc_win_l_dn 17
//DHT pins 

#define inc_DHT_pin_1 10 
#define inc_DHT_pin_2 11
#define hat_DHT_pin_1 12
#define hat_DHT_pin_2 13

// define pwm servo pins 

#define inc_servo_pin 18
#define hat_servo_pin 19 


 
float tempreture_of_inc = 0;
float humidity_of_inc = 0;
float tempreture_of_hat = 0;
float humidity_of_hat = 0;

unsigned long  Env_gen_refresh = millis(); 
unsigned long  Env_refresh = millis(); 
unsigned long  wins_refresh = millis();
unsigned long wins_refresh_for_up = 0;
bool EMERGENCY = false;
bool auto_wins_up = true;
bool auto_wins_down = true;
bool need_to_close_windows = false;
bool wins_refresh_bool = true;

String command = "";

//define servo motors
Servo inc_servo;
Servo hat_servo; 
unsigned long servo_refresh = millis();
unsigned long servo_timings = millis();
bool automatic_testing = false;
bool servo_moved = false;

void servo_auto_move(){
  if(!automatic_testing)
  {
    if(millis() - servo_refresh >= 10000 and !servo_moved)
    {
      hat_servo.attach(hat_servo_pin);
      hat_servo.write(135);
      inc_servo.attach(inc_servo_pin);
      inc_servo.write(135); // 45 degrees right 

      Serial.println("moved servo");
      servo_moved = true;
    }
    else if(millis() - servo_timings >= 12000 and servo_moved)
    {   
      inc_servo.write(45);
      hat_servo.write(45); /// 45 degres left 
      servo_refresh = millis();
      servo_moved = false;
    }
    else if (millis() - servo_timings >= 14000) 
    {  
      inc_servo.write(90);
      hat_servo.write(90); // back to 90 
      servo_timings = millis(); 
    }
  }
}

DHT22 inc_DHT_1(inc_DHT_pin_1); 
DHT22 inc_DHT_2(inc_DHT_pin_2); 
DHT22 hat_DHT_1(hat_DHT_pin_1); 
DHT22 hat_DHT_2(hat_DHT_pin_2); 


void refresh_temp(){
  if (tempreture_of_inc < 37.65)
    digitalWrite(inc_heater_pin , LOW);
  else 
    digitalWrite(inc_heater_pin , HIGH);
  if (tempreture_of_hat < 37.65)
    digitalWrite(hat_heater_pin , LOW);
  else 
    digitalWrite(hat_heater_pin , HIGH);
}
void refresh_humidity(){
  if (humidity_of_inc < 55.00)
    digitalWrite(inc_humifier_pin , LOW);
  else 
    digitalWrite(inc_humifier_pin , HIGH);
  if (humidity_of_hat < 75.00)
    digitalWrite(hat_humifier_pin , LOW);
  else 
    digitalWrite(hat_humifier_pin , HIGH);
}

 
void setup() {
  Wire.begin();
  Serial.begin(9600);
  
  // incubator windows setup 
  pinMode(inc_win_r_up, OUTPUT);
  pinMode(inc_win_r_dn, OUTPUT);
  pinMode(inc_win_l_up, OUTPUT);
  pinMode(inc_win_l_dn, OUTPUT);
  
  // hatcher windows setup   
  pinMode(hat_win_r_up, OUTPUT);
  pinMode(hat_win_r_dn, OUTPUT);
  pinMode(hat_win_l_up, OUTPUT);
  pinMode(hat_win_l_dn, OUTPUT);

  pinMode(inc_humifier_pin, OUTPUT);
  pinMode(inc_heater_pin, OUTPUT);
  pinMode(hat_humifier_pin, OUTPUT);
  pinMode(hat_heater_pin, OUTPUT);


  pinMode(inc_DHT_pin_1, INPUT);
  pinMode(inc_DHT_pin_2, INPUT);
  pinMode(hat_DHT_pin_1, INPUT);
  pinMode(hat_DHT_pin_2, INPUT);
  
  
  pinMode(inc_servo_pin, OUTPUT);
  inc_servo.attach(inc_servo_pin);
  inc_servo.write(90);  // standerization 

  pinMode(hat_servo_pin, OUTPUT);
  hat_servo.attach(hat_servo_pin);
  hat_servo.write(90);  // standerization 

}

void loop() {
  read_command(command);
  // digitalWrite(inc_heater_pin , LOW);
  // digitalWrite(inc_humifier_pin , LOW);

  servo_auto_move();




  // read command 
  if (Serial.available()) {
    command = Serial.readString();
    command.trim(); 
    // Serial.print("Received data: ");
    // Serial.println(command);
    read_command(command);
    command = "";
  }

  if ((millis() - wins_refresh >= 20 * 60000) && auto_wins_down && !need_to_close_windows ){
    auto_wins_down = false;
    need_to_close_windows = true;
    Serial.println("auto_wins_dn");
    wins_refresh_for_up = millis();
  }
  
  if((millis() - wins_refresh_for_up >= 2 * 60000) && need_to_close_windows && auto_wins_up){
    auto_wins_up = false;
    need_to_close_windows = false;
    wins_refresh = millis();
    Serial.println("auto_wins_up");
  }

  if (millis() - Env_refresh >= 2000) { // 10 min * 60 sec * 1000 ms or overflow of millis variable 

      Env_refresh = millis();   
      float inc_temp_1 = inc_DHT_1.getTemperature();
      float inc_temp_2 = inc_DHT_2.getTemperature();

      float inc_humi_1 = inc_DHT_1.getHumidity();
      float inc_humi_2 = inc_DHT_2.getHumidity();

      float hat_temp_1 = hat_DHT_1.getTemperature();
      float hat_temp_2 = hat_DHT_2.getTemperature();

      float hat_humi_1 = hat_DHT_1.getHumidity();
      float hat_humi_2 = hat_DHT_2.getHumidity();
      


      float tempreture_of_inc = (inc_temp_1+inc_temp_2) /2;
      float humidity_of_inc = (inc_humi_1+inc_humi_2) /2;
      
      float tempreture_of_hat = (hat_temp_1+hat_temp_2) /2;
      float humidity_of_hat = (hat_humi_1+hat_humi_2) /2;

      Serial.print("humidety_of_inc=");
      Serial.print(humidity_of_inc);
      Serial.println(" done");
      

      Serial.print("tempreture_of_inc=");
      Serial.print(tempreture_of_inc);
      Serial.println(" done");


      Serial.print("humidety_of_hat=");
      Serial.print(humidity_of_hat);
      Serial.println(" done");


      Serial.print("tempreture_of_hat=");
      Serial.print(tempreture_of_hat);
      Serial.println(" done");

    
    if (hat_DHT_1.getLastError() != hat_DHT_1.OK || hat_DHT_2.getLastError() != hat_DHT_2.OK || inc_DHT_1.getLastError() != inc_DHT_1.OK || inc_DHT_2.getLastError() != inc_DHT_2.OK) {
      Serial.println("last error :");
      Serial.println(hat_DHT_1.getLastError());
      Serial.println(hat_DHT_2.getLastError());
      Serial.println(inc_DHT_1.getLastError());
      Serial.println(inc_DHT_2.getLastError());

    }

    //message what the sencor read 
    // Serial.println(tempreture_of_inc);
    // Serial.println(huhmidity_of_inc);
    // Serial.println(tempreture_of_hat);
    // Serial.println(huhmidity_of_hat);

    
    if (millis() - Env_gen_refresh >= 5000) { // 10 min * 60 sec * 1000 ms or overflow of millis variable 

      Env_gen_refresh = millis();
      if (EMERGENCY == false){
        refresh_temp();
        refresh_humidity();
      }
    }
  }

  // else if (tempreture_of_inc < 38 && tempreture_of_inc > 37){    
  //   if (inc_high == TRUE)  
  //     digitalWrite(inc_heater_pin , LOW);
  //   else if (tempreture_of_inc == 37)   
  //     digitalWrite(inc_heater_pin , HIGH);
  //     inc_high = FALSE;
  // }    
  // delay(2000); //Collecting period should be : >1.7 second
}

void DC_Motor_reset()
{
  digitalWrite(inc_win_r_up , LOW);
  digitalWrite(inc_win_r_dn , LOW);
  digitalWrite(inc_win_l_up , LOW);
  digitalWrite(inc_win_l_dn , LOW);
  digitalWrite(hat_win_r_up , LOW);
  digitalWrite(hat_win_r_dn , LOW);
  digitalWrite(hat_win_l_up , LOW);
  digitalWrite(hat_win_l_dn , LOW);
  // Serial.println("dc_reset");
  
}

int16_t read_command(String command){
  
  if (command == "wins_up" or !auto_wins_up) {
    digitalWrite(inc_win_r_up , HIGH);
    digitalWrite(inc_win_r_dn , LOW);
    digitalWrite(inc_win_l_up , HIGH);
    digitalWrite(inc_win_l_dn , LOW);
    digitalWrite(hat_win_r_up , HIGH);
    digitalWrite(hat_win_r_dn , LOW);
    digitalWrite(hat_win_l_up , HIGH);
    digitalWrite(hat_win_l_dn , LOW);
    Serial.println("wins_up");
    auto_wins_up = true;
    EMERGENCY = false;
    // delay(2000);
    DC_Motor_reset();
  }
  
  else if (command == "wins_down" or !auto_wins_down){
    digitalWrite(inc_win_r_up , LOW);
    digitalWrite(inc_win_r_dn , HIGH);
    digitalWrite(inc_win_l_up , LOW);
    digitalWrite(inc_win_l_dn , HIGH);
    digitalWrite(hat_win_r_up , LOW);
    digitalWrite(hat_win_r_dn , HIGH);
    digitalWrite(hat_win_l_up , LOW);
    digitalWrite(hat_win_l_dn , HIGH);
    EMERGENCY = false;
    Serial.println("wins_down");
    auto_wins_down = true;

    // delay(2000);
    DC_Motor_reset();
  }   

  else if (command == "EMERGENCY"){
    DC_Motor_reset();
    EMERGENCY = true;
    digitalWrite(hat_humifier_pin , LOW);
    digitalWrite(hat_heater_pin , LOW);
    digitalWrite(inc_humifier_pin , LOW);
    digitalWrite(inc_heater_pin , LOW); 
    Serial.println(command);
    // delay(2000);

  }

  else if(command=="automatic_testing")
  {
    EMERGENCY == true;  //place holde for automatic_testing bool
    // since emergency is already defined and does the same 
  }
  else if(command=="automatic_testing_done")
  {
    EMERGENCY == false;
  }

}