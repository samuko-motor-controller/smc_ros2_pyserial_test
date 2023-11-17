
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32MultiArray

from smc_arduino_pyserial_comm import SMCArduinoSerialComm
from time import sleep



class SMCDriveServer(Node):

    def __init__(self):
        super().__init__('smc_drive_server_node')
        self.subscription = self.create_subscription(
            Float32MultiArray,
            '/smc/cmd_vel',
            self.smc_drive_server_callback,
            10)
        self.subscription  # prevent unused variable warning

        self.publisher_ = self.create_publisher(Float32MultiArray, 'smc/wheeldata', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.smc = SMCArduinoSerialComm('/dev/ttyUSB0')
        sleep(4.0)

        self.readAngVelA = 0.000
        self.readAngVelB = 0.000
        self.readAngPosA = 0.000
        self.readAngPosB = 0.000

        self.angVelA = 0.000 #rad/sec
        self.angVelB = 0.000 #rad/sec
        self.smc.sendTargetVel(self.angVelA, self.angVelB)



    def smc_drive_server_callback(self, cmd_vel):
        # self.get_logger().info('I heard: "%s"' % msg.data)
        self.angVelA = cmd_vel.data[0]
        self.angVelB = cmd_vel.data[1]
        self.smc.sendTargetVel(self.angVelA, self.angVelB)

    def timer_callback(self):
        try:
          msg = Float32MultiArray()
          angPosA, angPosB = self.smc.getMotorsPos() # returns angPosA, angPosB
          angVelA, angVelB = self.smc.getMotorsVel() # returns angVelA, angVelB
          msg.data = [angPosA, angVelA, angPosB, angVelB]
          self.publisher_.publish(msg)
          self.get_logger().info("motorA_readings: [%f, %f]\nmotorB_readings: [%f, %f]\n" % (msg.data[0], msg.data[1], msg.data[2], msg.data[3]))
        except:
          pass
        


def main(args=None):
    rclpy.init(args=args)

    smc_drive_server = SMCDriveServer()

    rclpy.spin(smc_drive_server)

    smc_drive_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
