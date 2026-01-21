# Final-Exam-RE-703-BT-Gazebo-Sim

Roberto Nicolas Saputra/ 4222211015

# Case Study
a robot that avoids obstacles, if there is an object in front of it then the robot moves to the right. if there is no obstacle the robot moves forward.

# Behaviour Tree Diagram
<img width="1604" height="846" alt="Robot_BT" src="https://github.com/user-attachments/assets/35d57ed6-ce71-4e41-9093-8c50f97bcdfc" />

# Running Instruction
To run the robot simulation in the gazebo, run the following commands:
cd ~/gazebo_ws
source install/setup.bash
ros2 launch articubot_one launch_sim.launch.py(launch robot)

ros2 run obstacle_bt obstacle_bt (obstacle program)



# Demonstrasion Robot
<img width="2144" height="1352" alt="Behaviour Tree Demo" src="https://github.com/user-attachments/assets/4e5813ea-529f-4105-9a33-bc61a30945bd" />

