
#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <LiquidCrystal_I2C.h>
#include <Stepper.h>

MPU6050 mpu;
LiquidCrystal_I2C lcd(0x27, 16, 2);

int stepsPerRevolution = 2048;

Stepper vertStepper = Stepper(stepsPerRevolution, 47, 51, 49, 53); 
Stepper horStepper = Stepper(stepsPerRevolution, 46, 50, 48, 52); 

bool dmpReady = false;
uint8_t mpuIntStatus;
uint8_t devStatus;
uint16_t packetSize;
uint16_t fifoCount;
uint8_t fifoBuffer[64];

Quaternion q;           // [w, x, y, z] kvaternion
VectorFloat gravity;    // [x, y, z] vektor setrvačnosti
float rotace[3];        // rotace kolem os x,y,z

// actual data from gyro senzor
float z;
float y;
float temp;

// active command
String command;

// wanted angles
float vertAng;
float horAng;

// Rutina přerušení
volatile bool mpuInterrupt = false;
void dmpINT() {
  mpuInterrupt = true;
}

void setup() {  
  Wire.begin();

  lcd.begin();
  lcd.setCursor(0, 0);
  lcd.clear();
  lcd.print("Setup...");
  
  Serial.begin(115200);
  Serial.setTimeout(1);
  while (!Serial);
  setupGyro();
}

void loop() {
  if (!dmpReady) return;

  command = Serial.readString();
  command.trim();
  
  int indexOfSplit = command.indexOf("|");
  if (indexOfSplit != -1) {
    vertAng = command.substring(0, indexOfSplit).toFloat();
    horAng = command.substring(indexOfSplit+1, command.length()).toFloat();
  }
  else if (command == "GET") {
    // DATAZ|Y|TEMP
    Serial.println("DATA" + String(z) + "|" + String(y) + "|" + String(temp));
  }
  
  readGyro();

  //lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(prepareValueToLcd(z));
  lcd.setCursor(0, 1);
  lcd.print(prepareValueToLcd(y));
  lcd.setCursor(8, 0);
  lcd.print(String(temp) + " C" + (char)223);
  
  delay(100);
}

void readGyro() {  
  mpuInterrupt = false;
  mpuIntStatus = mpu.getIntStatus();
  fifoCount = mpu.getFIFOCount();
  if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
    mpu.resetFIFO();
    Serial.println(F("Preteceni zasobniku dat!"));
  }
  else if (mpuIntStatus & 0x02) {
    while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();
    mpu.getFIFOBytes(fifoBuffer, packetSize);
    fifoCount -= packetSize;
    mpu.dmpGetQuaternion(&q, fifoBuffer);
    mpu.dmpGetGravity(&gravity, &q);
    mpu.dmpGetYawPitchRoll(rotace, &q, &gravity);

    z = rotace[0] * 180 / M_PI;
    y = rotace[1] * 180 / M_PI;
    temp = mpu.getTemperature()/340.00+36.53;
  }
}

String prepareValueToLcd(float value) 
{
  String strVal = String(value) + (char)223;
  int len = strVal.length();
  for (int i = 0; i < 7 - len; i++) {
    strVal += " ";
  }
  strVal += "|";
  return strVal;
}

void setupGyro() 
{
  Serial.println("Inicializace I2C zarizeni..");
  mpu.initialize();
  Serial.println("Test pripojenych zarizeni..");
  Serial.println(mpu.testConnection() ? "Modul pripojeni" : "Pripojeni modulu selhalo");
  Serial.println("Inicializace DMP...");
  devStatus = mpu.dmpInitialize();
  if (devStatus == 0) {
    Serial.println("Povoleni DMP...");
    mpu.setDMPEnabled(true);
    attachInterrupt(0, dmpINT, RISING);
    mpuIntStatus = mpu.getIntStatus();
    Serial.println("DMP pripraveno, cekam na prvni preruseni..");
    dmpReady = true;
    packetSize = mpu.dmpGetFIFOPacketSize();
  }
  else {
    // V případě chyby:
    // 1 : selhání připojení k DMP
    // 2 : selhání při nastavení DMP
    Serial.println("DMP inicializace selhala (kod " + String(devStatus) + ")");
  }
}
