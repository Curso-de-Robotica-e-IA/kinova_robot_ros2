import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped, Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from std_srvs.srv import SetBool  # Substitui o ServoCommandType no Humble

class ServoAdapter(Node):
    """
    Interface node for controlling MoveIt Servo via TwistStamped messages in ROS 2 Humble.
    """

    def __init__(self):
        super().__init__('servo_adapter')
        
        self.trajectory_pub = self.create_publisher(
            JointTrajectory,
            '/joint_trajectory_controller/joint_trajectory',
            10
        )
        
        self.servo_pub = self.create_publisher(
            TwistStamped,
            '/servo_node/delta_twist_cmds',
            10
        )
        
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # No Humble, usamos pause_servo para liberar os controladores
        self.cli = self.create_client(SetBool, '/servo_node/pause_servo')
        self.frame_id = 'base_link' 
        
        self.startup_completed = False
        
        self.startup_timer = self.create_timer(1.0, self.check_service_and_start)

    def check_service_and_start(self):
        """
        Passo 1: Aguarda o serviço pause_servo. 
        Pausa o Servo para permitir que o JointTrajectoryController atue sem conflitos.
        """
        if not self.cli.service_is_ready():
            self.get_logger().info('Aguardando o serviço /servo_node/pause_servo...')
            return  
            
        self.startup_timer.cancel()
        self.get_logger().info('Serviço encontrado. Pausando o Servo para execução da trajetória...')
        
        req = SetBool.Request()
        req.data = True  # True = Pausar o Servo
        
        future = self.cli.call_async(req)
        future.add_done_callback(self.on_servo_paused)

    def on_servo_paused(self, future):
        """
        Passo 2: Após o Servo pausar, publica a trajetória inicial para sair da singularidade.
        """
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Servo pausado. Enviando trajetória inicial...')
                
                msg = JointTrajectory()
                msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4', 'joint_5', 'joint_6']
                
                point = JointTrajectoryPoint()
                point.positions = [0.1, 0.1, 1.5, 0.01, 0.5, 0.01] 
                
                duration = Duration()
                duration.sec = 3
                duration.nanosec = 0
                point.time_from_start = duration
                
                msg.points = [point]
                self.trajectory_pub.publish(msg)
                
                self.get_logger().info('Aguardando 3.5s para a trajetória finalizar...')
                self.trajectory_wait_timer = self.create_timer(3.5, self.unpause_servo)
            else:
                self.get_logger().error('Falha ao pausar o Servo.')
                
        except Exception as e:
            self.get_logger().error(f'Erro na chamada do serviço: {e}')

    def unpause_servo(self):
        """
        Passo 3: Trajetória finalizada. Solicita que o Servo seja despausado para iniciar a teleoperação.
        """
        self.trajectory_wait_timer.cancel() 
        self.get_logger().info('Trajetória finalizada. Despausando o Servo para comandos Twist...')
        
        req = SetBool.Request()
        req.data = False  # False = Despausar o Servo
        
        future = self.cli.call_async(req)
        future.add_done_callback(self.on_servo_unpaused)

    def on_servo_unpaused(self, future):
        """
        Passo 4: Servo despausado. O pipeline de teleoperação é ativado.
        """
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Servo despausado com sucesso!')
                self.startup_completed = True 
                self.get_logger().info('*** ROBÔ PRONTO PARA TELEOPERAÇÃO ***')
            else:
                self.get_logger().error('Falha ao despausar o Servo.')
        except Exception as e:
            self.get_logger().error(f'Erro ao reativar o Servo: {e}')

    def cmd_vel_callback(self, msg: Twist):
        """
        Encaminha os comandos somente após a inicialização ser concluída.
        """
        if not self.startup_completed:
            return
            
        new_msg = TwistStamped()
        new_msg.twist = msg
        new_msg.header.stamp = self.get_clock().now().to_msg()
        new_msg.header.frame_id = self.frame_id
        
        self.servo_pub.publish(new_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ServoAdapter()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()