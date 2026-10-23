#!/usr/bin/env python3

import rospy
from rosgraph.masterapi import Master
from rospy.topics import Publisher, Subscriber
from rospy.service import ServiceProxy
from rospy.exceptions import ROSException
import rosservice
import actionlib

class FullInteractivity:
    def __init__(self):
        rospy.init_node("Dynamic Node Handler", anonymous=True)

        self.master = Master()
        self.known_nodes = set()
        self.publishers = {}
        self.subscribers = {}
        self.services = {}
        self.action_clients = {}

        rospy.Timer(rospy.Duration(1), self.discover_and_interact)

    def discover_and_interact(self, event):
        state = self.master.getSystemState()

        self.handle_topics(state[0], state[1])

        self.handle_services()

    def handle_topics(self, publishers, subscribers):
        for topic, nodes in publishers:
            if topic not in self.subscribers:
                rospy.loginfo(f"Subscribing to topic: {topic}")
                self.subscribers[topic] = Subscriber(topic, rospy.AnyMsg, self.generic_callback)

        for topic, nodes in subscribers:
            if topic not in self.publishers:
                rospy.loginfo(f"Creating publisher for topic: {topic}")
                self.publishers[topic] = Publisher(topic, rospy.AnyMsg, queue_size=10)

    def handle_services(self):
        service_list = rosservice.get_service_list()
        for service in service_list:
            if service not in self.services:
                try:
                    rospy.loginfo(f"Creating proxy for service: {service}")
                    service_type = rosservice.get_service_type(service)
                    self.services[service] = ServiceProxy(service, rosservice.get_service_class_by_name(service_type))
                except ROSException as e:
                    rospy.logwarn(f"Failed to create proxy for service {service}: {e}")

    def generic_callback(self, msg):
        rospy.loginfo(f"Received message on {msg._connection_header['topic']}")

    def publish_to_topic(self, topic, msg):
        if topic in self.publishers:
            self.publishers[topic].publish(msg)
            rospy.loginfo(f"Published message to topic: {topic}")
        else:
            rospy.logwarn(f"No publisher available for topic: {topic}")

    def call_service(self, service, *args):
        if service in self.services:
            try:
                response = self.services[service](*args)
                rospy.loginfo(f"Service {service} called successfully. Response: {response}")
                return response
            except ROSException as e:
                rospy.logwarn(f"Failed to call service {service}: {e}")
        else:
            rospy.logwarn(f"No service proxy available for: {service}")

    def connect_to_action(self, action_name, action_type):
        if action_name not in self.action_clients:
            try:
                rospy.loginfo(f"Connecting to action: {action_name}")
                self.action_clients[action_name] = actionlib.SimpleActionClient(action_name, action_type)
                self.action_clients[action_name].wait_for_server()
                rospy.loginfo(f"Connected to action server: {action_name}")
            except Exception as e:
                rospy.logwarn(f"Failed to connect to action server {action_name}: {e}")

if __name__ == "__main__":
    try:
        node = FullInteractivity()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
