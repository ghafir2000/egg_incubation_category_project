#include <AccelStepper.h>
#include <Servo.h>

 

//Define pins for led
#define led 2

//Define pin for vacumm
#define vacume 3
#define selenoid 10


// Define arm motor pins (steppers)
#define arm_hori_dirPin 4  // Direction pin
#define arm_hori_stpPin 5 // Step pin

#define arm_verti_dirPin 12  // Direction pin
#define arm_verti_stpPin 13 // Step pin



// define camera and leds motor pins (steppers)
#define camera_dirPin 8  // Direction pin
#define camera_stpPin 9 // Step pin


#define leds_dirPin 6  // Direction pin
#define leds_stpPin 7 // Step pin

//define servo motors
// Servo inc_servo;
// Servo hat_servo; 
// unsigned long servo_refresh = millis();
// bool automatic_testing = false;

// Create AccelStepper objects for all stepper motors
AccelStepper camera_stepper(AccelStepper::DRIVER, camera_stpPin, camera_dirPin);
AccelStepper arm_hori_stepper(AccelStepper::DRIVER, arm_hori_stpPin, arm_hori_dirPin);
AccelStepper arm_vertii_stepper(AccelStepper::DRIVER, arm_verti_stpPin, arm_verti_dirPin);
AccelStepper leds_stepper(AccelStepper::DRIVER, leds_stpPin, leds_dirPin); 


// Initialize an empty string to store the numeric part and nonnumeric part
String numpart = ""; 
String wordpart = "";
String message="";
int intpart=0;
// int i=0;

// Define some motor parameters
const float stepsPerRevolution = 200; // HS17 has 200 steps per revolution
const float mmPerRevolution = 7.9; // Assuming 8 mm per revolution of the shaft on 17hs3401 stepper 
const float mmPerRevolution_camera = 84.8; // Assuming 27 mm per revolution of the shaft on 17hs3401 stepper 

// define movment arrays in cm
float move_camera_array[] = {0 , 4.5 , 9 , 13.5 , 18 , 22.5 , 27 , 31.5 , 36};

float move_arm_hori_array[] = {0 , 12 , 16.5 , 21 , 25.5 , 30 , 34.5 , 39 , 43.5 ,
 48 , 56 , 74 , 78.5 , 83 , 87.5 , 92 , 96.5 , 101 , 105.5 , 110};

int move_arm_verti_array[] = {0,9};

int move_led_array[] = {0,5};

// Helper function to calculate steps from distance from mm to step 
int distanceToSteps(float distance) {
  float revolutions = distance * 10 / mmPerRevolution;
  int steps = revolutions * stepsPerRevolution;
  return steps;
}  
int distanceToSteps_camera(float distance) {
  float revolutions = distance * 10 / mmPerRevolution_camera; // cm to mm 
  int steps = revolutions * stepsPerRevolution;
  return steps;
}  

// void servo_auto_move(){
//   if(!automatic_testing)
//   {
    
//     if(millis() - servo_refresh >= 60 * 60 * 1000 )
//     {
//       inc_servo.attach(inc_servo_pin);

//       inc_servo.write(90); // standerization 
//       inc_servo.write(135);
//       Serial.println("moved servo");
      
//       delay(1000);      
//       inc_servo.write(45);
//       delay(3000);
//       inc_servo.write(90);

//       hat_servo.attach(hat_servo_pin);

//       hat_servo.write(90); // standerization 
//       hat_servo.write(135);
//       delay(3000);
//       hat_servo.write(45);
//       delay(3000);
//       hat_servo.write(90);
//       servo_refresh = millis();

//     }
//   }
// }
// void test_for_message(){
  
// }



void setup() {

 //set pin model for selenoid
  pinMode(selenoid,OUTPUT);
  digitalWrite(selenoid,HIGH);



  //set pin model for vacumme
  pinMode(vacume,OUTPUT);
  digitalWrite(vacume,HIGH);

  //set pin model for leds
  pinMode(led,OUTPUT);
  digitalWrite(led,LOW);

  
  // Set pin modes for stepper motors
  pinMode(camera_stpPin, OUTPUT);
  pinMode(camera_dirPin, OUTPUT);
  pinMode(arm_hori_stpPin, OUTPUT);
  pinMode(arm_hori_dirPin, OUTPUT);
  pinMode(arm_verti_stpPin, OUTPUT);
  pinMode(arm_verti_dirPin, OUTPUT);
  pinMode(leds_stpPin, OUTPUT);
  pinMode(leds_dirPin, OUTPUT);



  //set the pins for servo motors
  // inc_servo.attach(inc_servo_pin);
  // hat_servo.attach(hat_servo_pin);

  // Set the maximum speed and acceleration for the stepper motor
  camera_stepper.setMaxSpeed(5000);
  camera_stepper.setAcceleration(500);

  arm_hori_stepper.setMaxSpeed(3000);
  arm_hori_stepper.setAcceleration(500);

  arm_vertii_stepper.setMaxSpeed(5000);
  arm_vertii_stepper.setAcceleration(500);

  leds_stepper.setMaxSpeed(5000);
  leds_stepper.setAcceleration(500);

  //get the arduino to connect to serial chanal
  Serial.begin(9600);

}

void loop()
{

  //set conditon to wait for order from the raspery
  if(Serial.available())
  {

    message = Serial.readString();
    //to split message to tow part string and int
    for (int i = 0; i < message.length(); i++) 
    {
      if (isdigit(message.charAt(i))) {
          numpart += message.charAt(i); // Append numeric characters
      } else {
          wordpart += message.charAt(i); // Append non-numeric characters
      }   
    }
    wordpart.trim();
    // Serial.println(wordpart); 
    intpart = numpart.toInt();
     if(wordpart=="move")
    { 
      Serial.println(wordpart); 
      Serial.println(wordpart); 

    }

    else if(wordpart=="EMERGENCY")
    {
      Serial.println(wordpart); 
      camera_stepper.stop();
      arm_hori_stepper.stop();
      arm_vertii_stepper.stop();
      leds_stepper.stop();

      // hat_servo.detach();
      // inc_servo.detach();

      digitalWrite(vacume,1);
      digitalWrite(selenoid,1);
      digitalWrite(led,0);

    }
    else if(wordpart=="arm_stop")
    {
      Serial.println(wordpart); 
      arm_hori_stepper.stop();
      arm_vertii_stepper.stop();

    }
  
  //condtion for stepper motor
    else if(wordpart=="camera_stepper_")
    {
      Serial.println(wordpart); 
      int steps_to_go = distanceToSteps_camera(move_camera_array[intpart]);
      // int movement = steps_to_go - camera_stepper.currentPosition();        
      camera_stepper.moveTo(steps_to_go);

      while (camera_stepper.distanceToGo() != 0) 
        {
          // i=i+1;
        camera_stepper.run();
        // test_for_message();
        // Serial.println("Done A");
        // Serial.println(i);
        // Serial.println(pos);

        }

    }
    else if(wordpart=="arm_hori_stepper_")
  {
    Serial.println(wordpart); 
    int steps_to_go = distanceToSteps(move_arm_hori_array[intpart]);
    // int movement = steps_to_go - arm_hori_stepper.currentPosition();        
    arm_hori_stepper.moveTo(steps_to_go);
    while (arm_hori_stepper.distanceToGo() != 0) 
      {
      arm_hori_stepper.run();
      
      // test_for_message();
      }

  }
    else if(wordpart=="arm_verti_stepper_")
    {
      Serial.println(wordpart);   
      int steps_to_go = distanceToSteps(move_arm_verti_array[intpart]);
      // int movement = steps_to_go - arm_vertii_stepper.currentPosition();        
      arm_vertii_stepper.moveTo(steps_to_go);
      while (arm_vertii_stepper.distanceToGo() != 0) 
        {
        arm_vertii_stepper.run();
        // test_for_message();
        }

    }
  else if(wordpart=="leds_stepper_")
    {
      Serial.println(wordpart); 
      int steps_to_go = distanceToSteps(move_led_array[intpart]);
      // int movement = steps_to_go - leds_stepper.currentPosition();        
      leds_stepper.moveTo(steps_to_go);
      while (leds_stepper.distanceToGo() != 0) 
        {
        leds_stepper.run();
        // test_for_message();

        }

    }
  else if(wordpart=="LED_")
    {
      int mode =intpart;
      digitalWrite(led,mode);
    Serial.println(wordpart); 

      // delay(1000);
    }
  else if(wordpart=="vacume_")
    {
    Serial.println(wordpart); 
      int mode =intpart;
      digitalWrite(vacume,!mode);

    }
  else if(wordpart=="selenoid_")
    {
      int mode =intpart;
      digitalWrite(selenoid,!mode);
    Serial.println(wordpart); 

    }
  
  else if(wordpart=="automatic_testing")
    {
      Serial.println("call_auto_testing");
      // automatic_testing == true;


      // inc_servo.attach(inc_servo_pin);
      // inc_servo.write(90);
      int steps_to_go = distanceToSteps(move_led_array[1]);
      // int movement = steps_to_go - leds_stepper.currentPosition();        
      leds_stepper.moveTo(steps_to_go);
      while (leds_stepper.distanceToGo() != 0) 
        {
        leds_stepper.run();
        // test_for_message();
        }
      delay(100);
    }
  else if(wordpart=="automatic_testing_done")
    {
      // automatic_testing == false;


      int steps_to_go = distanceToSteps(move_arm_hori_array[0]);
      // int movement = steps_to_go - arm_hori_stepper.currentPosition();        
      arm_hori_stepper.moveTo(steps_to_go);
      while (arm_hori_stepper.distanceToGo() != 0) 
        {
        arm_hori_stepper.run();
        // test_for_message();
        }
    }
  }
  
  // Serial.println(intpart);
  // Serial.println(wordpart);
  // delay(1000);
  message="";
  numpart="";
  intpart=0;
  wordpart="";
  
  // i=0;
  // test_for_message();
  // servo_auto_move();
}



