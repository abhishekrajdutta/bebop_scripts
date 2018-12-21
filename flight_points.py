import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, PoseStamped, Pose
import csv


pose = PoseStamped()

def joyCallback(msg):
	global pose,test_writer 
	pose_pub = rospy.Publisher('bebop/captured_pose', PoseStamped, queue_size=10)	
	with open('test.csv', mode='a') as test_file:
		test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		if msg.buttons[2] == 1:
			test_writer.writerow([pose.pose.position.x, pose.pose.position.y, pose.pose.position.z])
			pose_pub.publish(pose)

def poseCallback(msg):
	global pose
	pose = msg

def main():
	rospy.init_node('spacepoints', anonymous=False)		
	rospy.Subscriber('/vrpn_client_node/bebop/pose',PoseStamped,poseCallback)
	rospy.Subscriber('/bebop/joy',Joy, joyCallback)
	
	global test_writer
	rospy.spin()
	

if __name__ == '__main__':
	main()