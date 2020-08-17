import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

class vertMotor:
	def __init__(self):
		self.pin1 = 12
		self.pin2 = 15
		self.pin3 = 13
		self.pin4 = 11

		self.speed = 0.001

		GPIO.setup(self.pin1, GPIO.OUT)
		GPIO.setup(self.pin2, GPIO.OUT)
		GPIO.setup(self.pin3, GPIO.OUT)
		GPIO.setup(self.pin4, GPIO.OUT)

	def step1(self):
		GPIO.output(self.pin1, GPIO.HIGH)
		GPIO.output(self.pin2, GPIO.LOW)
		GPIO.output(self.pin3, GPIO.LOW)
		GPIO.output(self.pin4, GPIO.LOW)
		time.sleep(self.speed)
	def step2(self):
		GPIO.output(self.pin1, GPIO.HIGH)
		GPIO.output(self.pin2, GPIO.HIGH)
		GPIO.output(self.pin3, GPIO.LOW)
		GPIO.output(self.pin4, GPIO.LOW)
		time.sleep(self.speed)
	def step3(self):
		GPIO.output(self.pin1, GPIO.LOW)
		GPIO.output(self.pin2, GPIO.HIGH)
		GPIO.output(self.pin3, GPIO.LOW)
		GPIO.output(self.pin4, GPIO.LOW)
		time.sleep(self.speed)
	def step4(self):
		GPIO.output(self.pin1, GPIO.LOW)
		GPIO.output(self.pin2, GPIO.HIGH)
		GPIO.output(self.pin3, GPIO.HIGH)
		GPIO.output(self.pin4, GPIO.LOW)
		time.sleep(self.speed)
	def step5(self):
		GPIO.output(self.pin1, GPIO.LOW)
		GPIO.output(self.pin2, GPIO.LOW)
		GPIO.output(self.pin3, GPIO.HIGH)
		GPIO.output(self.pin4, GPIO.LOW)
		time.sleep(self.speed)
	def step6(self):
		GPIO.output(self.pin1, GPIO.LOW)
		GPIO.output(self.pin2, GPIO.LOW)
		GPIO.output(self.pin3, GPIO.HIGH)
		GPIO.output(self.pin4, GPIO.HIGH)
		time.sleep(self.speed)
	def step7(self):
		GPIO.output(self.pin1, GPIO.LOW)
		GPIO.output(self.pin2, GPIO.LOW)
		GPIO.output(self.pin3, GPIO.LOW)
		GPIO.output(self.pin4, GPIO.HIGH)
		time.sleep(self.speed)
	def step8(self):
		GPIO.output(self.pin1, GPIO.HIGH)
		GPIO.output(self.pin2, GPIO.LOW)
		GPIO.output(self.pin3, GPIO.LOW)
		GPIO.output(self.pin4, GPIO.HIGH)
		time.sleep(self.speed)

	def rotationUp(self):
		self.step1()
		self.step2()
		self.step3()
		self.step4()
		self.step5()
		self.step6()
		self.step7()
		self.step8()

	def rotationDown(self):
		self.step8()
		self.step7()
		self.step6()
		self.step5()
		self.step4()
		self.step3()
		self.step2()
		self.step1()

	def update(self):
		file = open("wantLocation.txt", "r")
		wantLoc = file.read().split(",")
		file.close()

		file = open("actLocation.txt", "r")
		act = file.read().split(",")
		file.close()

		delta = abs(int(act[1]) - int(wantLoc[1]))

		if (delta > 0):
			if (int(act[1]) < int(wantLoc[1])):
				self.rotationUp()
			else:
				self.rotationDown()

mot = vertMotor()
while True:
	mot.update()
