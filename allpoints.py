import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, PoseStamped, Pose
import csv


pose = PoseStamped()

def poseCallback(msg):
	pose = msg
	with open('all.csv', mode='a') as test_file:
		test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		test_writer.writerow([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])

def main():
	rospy.init_node('allpoints', anonymous=False)		
	rospy.Subscriber('/vrpn_client_node/bebop/pose',PoseStamped,poseCallback)
	global test_writer
	rospy.spin()
	

if __name__ == '__main__':
	main()