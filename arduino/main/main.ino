
#include <Stepper.h>

const int stepsPerRevolution = 2048;

String command;
int vertAng = -1;
int horAng = -1;

Stepper myStepper = Stepper(stepsPerRevolution, 46, 50, 48, 52);

void setup()
{
	myStepper.setSpeed(10);
	Serial.begin(115200);
	Serial.setTimeout(10);
}

void loop()
{
  //myStepper.step(-10);
	while (Serial.available()) {
		command = Serial.readString();
		/*
			command => verticalWantedAngle|horizontalWantedAngle
		*/
		int indexOfSplit = command.indexOf("|");
		if (indexOfSplit != -1) {
			vertAng = command.substring(0, indexOfSplit).toInt();
			horAng = command.substring(indexOfSplit+1, command.length()).toInt();
		}
	}

	Serial.println(String(vertAng) + " " + String(horAng));
}
