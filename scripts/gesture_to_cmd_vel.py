#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class GestureController:
    """
    A class to subscribe to hand gesture topics and publish velocity commands.
    """
    def __init__(self):
        """
        Initializes the ROS node, publishers, and subscribers.
        """
        # Initialize the ROS node
        rospy.init_node('gesture_to_cmd_vel_node', anonymous=True)

        # --- Parameters ---
        # The angular velocity for turning. Can be adjusted.
        self.turn_speed = 0.5  # radians per second

        # --- Publisher ---
        # Create a publisher to the /cmd_vel topic
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.loginfo("Publisher to /cmd_vel initialized.")

        # --- Subscriber ---
        # Create a subscriber to the /gesture/hand_sign topic
        self.gesture_sub = rospy.Subscriber('/gesture/hand_sign', String, self.gesture_callback)
        rospy.loginfo("Subscriber to /gesture/hand_sign initialized.")

        # Log that the node has started and is waiting for messages
        rospy.loginfo("Gesture controller node started. Waiting for hand signs...")

    def gesture_callback(self, msg):
        """
        Callback function that is executed whenever a message is received on the
        /gesture/hand_sign topic.
        """
        # Get the gesture command from the message data
        gesture = msg.data
        rospy.loginfo("Received gesture: '%s'", gesture)

        # Create a Twist message to send velocity commands
        twist_msg = Twist()

        # By default, the robot is stopped (all velocities are zero)
        # We only need to set the non-zero components based on the command.

        if gesture == "Turn Left":
            # Set the angular z-velocity for a left turn
            twist_msg.angular.z = self.turn_speed
            rospy.loginfo("Action: Turning Left")

        elif gesture == "Turn Right":
            # Set the angular z-velocity for a right turn
            twist_msg.angular.z = -self.turn_speed
            rospy.loginfo("Action: Turning Right")

        else:
            # For any other gesture (or no gesture), stop the robot.
            # All velocities in twist_msg are already 0.0 by default.
            rospy.loginfo("Action: Stopping")

        # Publish the Twist message to the /cmd_vel topic
        self.cmd_vel_pub.publish(twist_msg)

    def run(self):
        """
        Keeps the node running.
        """
        # rospy.spin() keeps python from exiting until this node is stopped
        rospy.spin()

if __name__ == '__main__':
    try:
        # Create an instance of the GestureController class
        controller = GestureController()
        # Keep the node running
        controller.run()
    except rospy.ROSInterruptException:
        # This block is executed if the node is shut down (e.g., with Ctrl+C)
        rospy.loginfo("Gesture controller node shut down.")
        pass

