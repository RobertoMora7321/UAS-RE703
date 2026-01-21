#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

import py_trees
import py_trees_ros


# =========================
# CONDITION: CHECK OBSTACLE
# =========================
class CheckObstacle(py_trees.behaviour.Behaviour):

    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.obstacle = False

        self.sub = self.node.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

    def scan_callback(self, msg):
        front_ranges = msg.ranges[len(msg.ranges)//3 : 2*len(msg.ranges)//3]
        self.obstacle = min(front_ranges) < 0.5

    def update(self):
        if self.obstacle:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE


# =========================
# ACTION: TURN
# =========================
class Turn(py_trees.behaviour.Behaviour):

    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.pub = self.node.create_publisher(Twist, '/cmd_vel', 10)

    def update(self):
        cmd = Twist()
        cmd.angular.z = 0.5
        self.pub.publish(cmd)
        return py_trees.common.Status.RUNNING


# =========================
# ACTION: MOVE FORWARD
# =========================
class MoveForward(py_trees.behaviour.Behaviour):

    def __init__(self, name, node):
        super().__init__(name)
        self.node = node
        self.pub = self.node.create_publisher(Twist, '/cmd_vel', 10)

    def update(self):
        cmd = Twist()
        cmd.linear.x = 0.2
        self.pub.publish(cmd)
        return py_trees.common.Status.RUNNING
def create_tree(node):
    root = py_trees.composites.Selector("Root", memory=False)
    avoid_sequence = py_trees.composites.Sequence("Avoid Obstacle", memory=False)

    check_obstacle = CheckObstacle("CheckObstacle", node)
    turn = Turn("Turn", node)

    move_forward = MoveForward("MoveForward", node)

    avoid_sequence.add_children([check_obstacle, turn])
    root.add_children([avoid_sequence, move_forward])

    return root
def main():
    rclpy.init()
    node = Node("obstacle_bt_node")

    tree = create_tree(node)
    behaviour_tree = py_trees_ros.trees.BehaviourTree(tree)

    behaviour_tree.setup(node=node)

    try:
        behaviour_tree.tick_tock(period_ms=100)
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    behaviour_tree.shutdown()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
