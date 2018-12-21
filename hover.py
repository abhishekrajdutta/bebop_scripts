#!/usr/bin/env python2
import rospy
import numpy as np
import gtsam
from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, quaternion_matrix, euler_from_matrix
from gtsam import Point3, Pose3, Rot3

class Hover():
	def __init__(self):
		# initiliaze
		rospy.init_node('GoForward', anonymous=False)
		self.velPub = rospy.Publisher('bebop/cmd_vel', Twist, queue_size=10)
		rospy.Subscriber('/vrpn_client_node/bebop/pose',PoseStamped, self.poseCallback)

		self.sTcurr_ros = PoseStamped()

		r = rospy.Rate(10)

		self.kp_x = 0.037
		self.kd_x = 0.025
		self.ki_x = 0.0000

		self.kp_y = 0.043
		self.kd_y = 0.03
		self.ki_y = 0.0007

		self.kp_z = 0.25
		self.kd_z = 0.0
		self.ki_z = 0.0

		self.kp_yaw = 0.05
		self.kd_yaw = 0.0
		self.ki_yaw = 0.0

		self.d_x = 0
		self.d_y = 0
		self.d_z = 0

		self.ix = 0
		self.iy = 0
		self.iz = 0
		self.iyaw = 0

		self.goals = []
		self.goals.append([0,0,1.25,0])
		self.goals.append([0.5,0.5,0.75,0])
		self.goals.append([0.5,-0.5,1,0])
		self.goals.append([-0.5,-0.5,0.75,0])
		self.goals.append([-0.5,0.5,1,0])

		self.goalindex = 0

		self.lastT = Pose3()
		self.lastyaw = 0
		self.move_cmd = Twist()

		self.first = 0
		self.count = 0

	def check(self, pose):
		dist = np.sqrt(np.power(pose.x(),2) + np.power(pose.y(),2) +np.power( pose.z(),2))
		print dist
		if self.first == 0:
			if dist<0.25:
				self.first = 1
				self.count = 1
		elif self.first == 1:
			if dist<0.25:
				self.count+=1
			else:
				self.first = 0
				self.count = 0

		if self.count == 20:
			self.first = 0
			self.count = 0
			return 1
		else:
			return 0

	def run(self):
		reached = 0

		r = rospy.Rate(10)
		while not rospy.is_shutdown():

			goal = self.goals[self.goalindex]
			self.sTg = Pose3(Rot3.Rz(goal[3]), Point3(goal[0], goal[1], goal[2]))
			R = quaternion_matrix([self.sTcurr_ros.pose.orientation.x,self.sTcurr_ros.pose.orientation.y,self.sTcurr_ros.pose.orientation.z,self.sTcurr_ros.pose.orientation.w])[0:3,0:3]
			self.sTcurr = Pose3(Rot3(R), Point3(self.sTcurr_ros.pose.position.x, self.sTcurr_ros.pose.position.y, self.sTcurr_ros.pose.position.z))

			currTg = self.sTcurr.between(self.sTg)

			u_pitch = self.kp_x*currTg.x() + self.kd_x*(currTg.x() - self.lastT.x()) + min(max(-0.2,self.ki_x*self.ix),0.2)
			u_roll = self.kp_y*currTg.y() + self.kd_y*(currTg.y() - self.lastT.y())
			currTg_yaw = currTg.rotation().rpy()[2]
			u_yaw = self.kp_yaw*currTg_yaw + self.kd_yaw*(currTg_yaw - self.lastyaw)
			u_z = self.kp_x*currTg.z() + self.kd_z*(currTg.z() - self.lastT.z())

			self.lastT = currTg
			self.lastyaw = currTg_yaw

			self.ix += currTg.x()
			self.iy += currTg.y()
			self.iz += currTg.z()
			self.iyaw +=currTg_yaw

			self.move_cmd.linear.x = min(max(-1,u_pitch),1)
			self.move_cmd.linear.y = min(max(-1,u_roll),1)
			self.move_cmd.linear.z = min(max(-1,u_z),1)
			self.move_cmd.angular.z = min(max(-1,u_yaw),1)

			self.velPub.publish(self.move_cmd)
			reached = self.check(currTg)
			if (reached == 1):
				reached = 0
				self.goalindex += 1

			r.sleep()

	def poseCallback(self, msg):
		self.sTcurr_ros = msg



def main():
	H = Hover()
	H.run()
	rospy.spin()


if __name__ == '__main__':
    main()
