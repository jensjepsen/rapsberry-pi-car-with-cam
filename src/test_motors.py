from gpiozero import Robot, Motor

from time import sleep

robot = Robot(left=(17, 27), right=(24, 23))

for i in range(4):
    robot.forward()
    sleep(10)
    robot.right()
    sleep(1)
