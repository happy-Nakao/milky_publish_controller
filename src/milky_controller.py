#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import rosparam
from geometry_msgs.msg import Twist
from milkypublisher_ros.msg import milky_Data

class MilkyCtrMegarover():
    def __init__(self):
        # Publisher
        self.vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        # Subscriber
        rospy.Subscriber("milky_publisher_json_to_pub", milky_Data, self.callback)
        # Value
        self.twist = Twist()
        
    def callback(self, milk):
        self.X = milk.controller.floatX
        self.Y = milk.controller.floatY
        self.joyCB(self.X, self.Y)

    def joyCB(self, X, Y):
        try:
            self.twist.angular.z = -0.8 * X
            self.twist.linear.x = 0.6 * Y
            self.vel_pub.publish(self.twist)
        except rospy.ROSInterruptException:
            rospy.logerr("!Interrupted!")
            pass

if __name__ == '__main__':
    rospy.init_node("milky_teleop", anonymous = True)
    mcm = MilkyCtrMegarover()
    rospy.spin()