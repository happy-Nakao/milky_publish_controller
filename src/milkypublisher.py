#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Dict
import rospy
from std_msgs.msg import String
import socket
import json
import time
from milkypublisher_ros.msg import milky_Data,milky_Pose,milky_Mutablepose
 
UDP_IP = "192.168.102.181"  # 受信するIPアドレス（すべてのIPアドレスを受信する場合は "0.0.0.0"）
UDP_PORT = 4001  # 受信するポート番号
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


class MilkyPublisher_Json2Pub():
    def __init__(self):
        self.r = rospy.Rate(25)

    def talker(self): 
        print('publishはじめるよー')
        while True:
            print('publishしてんでい')
            pub = rospy.Publisher("milky_publisher_json_to_pub",milky_Data,queue_size=1)
            data1, addr = sock.recvfrom(65536)  # データを受信（最大65536バイト）
            message = data1.decode('utf-8')  # 受信したデータをUTF-8でデコード
            # JSONデータを辞書型に変換する
            dict_data = json.loads(message)
            
            controller = dict_data['controller']
            date = dict_data['date']
            detectData = dict_data['detectData']
            frameSetting = dict_data['frameSetting']

            floatX = controller['floatX']
            floatY = controller['floatY']
            mutablePose = detectData["mutablePose"]
            color = frameSetting["color"]
            frameResolutionHeight = frameSetting["frameResolutionHeight"]
            frameResolutionWidth = frameSetting["frameResolutionWidth"]

            milky_data_pub = milky_Data()
            milky_data_pub.controller.floatX = floatX
            milky_data_pub.controller.floatY = floatY
            milky_data_pub.date = date
            vals = []
            for pose_data in mutablePose:
                vals.append(json.dumps(pose_data))
            milky_data_pub.detectData.mutablePose = vals 
            milky_data_pub.frameSetting.color = color
            milky_data_pub.frameSetting.frameResolutionHeight = frameResolutionHeight
            milky_data_pub.frameSetting.frameResolutionWidth = frameResolutionWidth 

            #print(milky_data_pub)
            pub.publish(milky_data_pub)
            self.r.sleep()

       
if __name__ == '__main__':
    rospy.init_node("milky_publisher_json2pub",anonymous=True)
    milky = MilkyPublisher_Json2Pub()
    milky.talker()
    rospy.spin()