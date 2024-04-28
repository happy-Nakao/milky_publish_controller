#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from milkypublisher_ros.msg import milky_Data


class Milky():
    def __init__(self):
        rospy.Subscriber("milky_publisher_json_to_pub", milky_Data, self.callback)
        
    def callback(self, milk):
        self.X = milk.controller.floatX
        self.Y = milk.controller.floatY
        self.talker(self.X, self.Y)      
        
    def talker(self, X, Y): 
        print(X)
        print(Y) 
        
    
if __name__ == '__main__':
    rospy.init_node("milk",anonymous=True)
    milky = Milky()
    rospy.spin()