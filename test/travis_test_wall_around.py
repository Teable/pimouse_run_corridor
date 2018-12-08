#!/usr/bin/env python
import unittest, rostest
import rosnode, rospy
import time

class WallAroundTest(unittest.TestCase):
	def set_and_get(self,lf,ls,rs,rf):
		with open("/dev/rtlightsensor0","w") as f:
			f.write("%d %d %d %d\n" % (rf,rs,ls,lf))

		time.sleep(0.3)

		with open("/dev/rtmotor_raw_l0","r") as lf,\
		     open("/dev/rtmotor_raw_r0","r") as rf:
			left= int(lf.readline().rstrip())
			right = int(rf.readline().rstrip())

		return left, right

	def test_io(self):
		left, right = self.set_and_get(51,0,0,0) #curve to right by left front sensor
		self.assertTrue(left > right != 0,"don't curve to right by left front sensors")

		left, right = self.set_and_get(0,0,0,51) #curve to right by right front sensor
		self.assertTrue(left > right != 0,"don't curve to right by right front sensors")

		left, right = self.set_and_get(0,0,51,0) #curve to left by right side sensor
		self.assertTrue(left < right, "don't curve to left by left side sensor")

		left, right = self.set_and_get(0,51,0,0) #curve to right by left side sensor
		self.assertTrue(left > right, "don't curve to right by right side sensor")

		left, right = self.set_and_get(50,30,50,50) #trace a wall
		self.assertTrue(left < right, "don't trace a wall")

if __name__ == '__main__':
	time.sleep(3)
	rospy.init_node('travis_test_wall_around')
	rostest.rosrun('pimouse_run_corridor','travis_test_wall_around',WallAroundTest)
