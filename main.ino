#include <Servo.h>

Servo servo;


// We get the pins
int data;
int const updateLed = 8;
int const pyLed = 12;

int const trigPin = 10;
int const echoPin = 11;
int const sensorLed = 7;

int const restartPin = 4;

bool isOpen;
int openAngle = 30;
int closeAngle = 90;

void setup() {
    // put your setup code here, to run once:
    
    Serial.begin(115200);

    // We initialize what mode the pins is
    pinMode(13, OUTPUT);
    digitalWrite(13, HIGH);
    
    pinMode(updateLed, OUTPUT);
    pinMode(pyLed, OUTPUT);

    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
  
    pinMode(sensorLed, OUTPUT);

    digitalWrite(restartPin, HIGH);
    pinMode(restartPin, OUTPUT);
      
    servo.attach(3);
    servo.write(openAngle);
    
}

void loop() {
    // put your main code here, to run repeatedly:

    // I just put "m_" at the front of the function cause it can cause error when using some libraries
    
    m_ultraSonicSensorUpdate();

    m_dataChecker();

    m_openChecker();
    m_LEDUpdate();
}

void m_LEDUpdate() {
    digitalWrite(updateLed, LOW);
    delay(1000);
    digitalWrite(updateLed, HIGH);
    delay(1000);
}

// This will handle if the trash can would open or not
void m_openChecker() { 
    if (isOpen) {
      servo.write(openAngle);
    }
    else {
      servo.write(closeAngle);
    }
}

void m_ultraSonicSensorUpdate() {
    long duration;
    long distance;
  
    digitalWrite(trigPin, HIGH);
    delay(1);
    digitalWrite(trigPin, LOW);
  
    duration = pulseIn(echoPin, HIGH);
  
    distance = (duration / 2) / 29.1;

    Serial.println(distance);
  
    // Checking if theres an object at 0.25 meters
    if (distance <= 25 && distance >= 0) {
      isOpen = true;
      digitalWrite(sensorLed, HIGH);
    }
    else {
      isOpen = false;
      digitalWrite(sensorLed, LOW);
    }
    delay(60);
}

// This will handle the information sent by python / Speech recognition
void m_dataChecker() {
    while (Serial.available()) {
      data = Serial.read();
      
      m_ultraSonicSensorUpdate();
      m_openChecker();
      m_LEDUpdate();
    }

    if (data == '1') {
      // servo.write(0);
      digitalWrite(pyLed, HIGH);
      isOpen = true;
    }

    else if (data == '0') {
      // servo.write(160);
      digitalWrite(pyLed, LOW);
      isOpen = false;
      m_ultraSonicSensorUpdate();
      m_openChecker();
    }
    else if (data == '2') {
      digitalWrite(restartPin, LOW);
    }
    Serial.print(data);
}
