import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Pose2D
from turtlesim.msg import Pose
import math

class TurtleControl(Node):

    def __init__(self):
        super().__init__('turtle_control')
        self.init_variables()
        self.init_publisher()
        self.init_subscribers()

    def init_variables(self):
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.x_goal = 0.0
        self.y_goal = 0.0
        self.k_linear = 1.0
        self.k_angular = 4.0
        self.error_tolerance = 0.1

    def init_publisher(self):
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.pub_callback)

    def init_subscribers(self):
        self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.create_subscription(Pose2D, '/goal', self.goal_callback, 10)

    def pose_callback(self, msg):
        self.x = msg.x
        self.y = msg.y
        self.theta = msg.theta

    def goal_callback(self, msg):
        self.x_goal = msg.x
        self.y_goal = msg.y

    def pub_callback(self):
        twist_msg = Twist()

        # Compute the errors
        error_x = self.x_goal - self.x
        error_y = self.y_goal - self.y
        distance_error = math.sqrt(error_x**2 + error_y**2)

        if distance_error < self.error_tolerance:
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = 0.0
        else:
            angle_to_goal = math.atan2(error_y, error_x)
            angular_error = angle_to_goal - self.theta

            twist_msg.linear.x = self.k_linear * distance_error
            twist_msg.angular.z = self.k_angular * angular_error

        self.publisher_.publish(twist_msg)

def main(args=None):
    rclpy.init(args=args)
    turtle_control = TurtleControl()
    rclpy.spin(turtle_control)
    turtle_control.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

