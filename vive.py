import rospy
from geometry_msgs.msg import Twist, PoseStamped, Pose
import csv


pose = PoseStamped()

def poseCallback(msg):
	pose = msg
	with open('vive.csv', mode='a') as test_file:
		test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if msg.buttons[2] == 1:
			test_writer.writerow([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])

def main():
	rospy.init_node('vive', anonymous=False)		
	rospy.Subscriber('/vrpn_client_node/vive/pose',PoseStamped,poseCallback)
	global test_writer
	rospy.spin()
	

if __name__ == '__main__':
	main()