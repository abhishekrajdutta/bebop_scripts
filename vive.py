import rospy
from geometry_msgs.msg import Twist, PoseStamped, Pose
from visualization_msgs.msg import Marker
import csv


pose = PoseStamped()

count = 0

def poseCallback(msg):
	# pose = msg
	markerPub = rospy.Publisher('viveMarker', Marker, queue_size=1)
	marker = Marker()
	marker.header.frame_id = "/world"
	marker.ns = "basic_shapes";
	marker.id = count;
	count += 1 
	marker.type = Marker.SPHERE;
	marker.action = Marker.ADD

	marker.color.r = 0.0
	marker.color.g = 1.0
	marker.color.b = 0.0
	marker.color.a = 1.0

	marker.scale.x = 0.1;
	marker.scale.y = 0.1;
	marker.scale.z = 0.1;    
	marker.pose = msg.pose

	markerPub.publish(marker);

	with open('vive.csv', mode='a') as test_file:
		test_writer = csv.writer(test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)		
		test_writer.writerow([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z])
		rospy.sleep(0.1)

def main():
	rospy.init_node('vive', anonymous=False)		
	rospy.Subscriber('/vrpn_client_node/vive/pose',PoseStamped,poseCallback)

	rospy.spin()
	

if __name__ == '__main__':
	main()