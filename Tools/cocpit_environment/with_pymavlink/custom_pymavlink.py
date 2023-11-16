from pymavlink import mavutil
import time
import math



class Custom_mav():

    def __init__(self,ip_sitl) -> None:
        self.myMav = None
        self.connection_string = f"udp:{ip_sitl}:14551"
        self.target_system = None
        self.target_component = None
        self.isArmed = False

    def connect(self):
        self.myMav = mavutil.mavlink_connection(self.connection_string)

        self.progress("wait for heartbeat")
        self.myMav.wait_heartbeat()

        # Set the target system and component IDs for sending messages
        self.target_system = self.myMav.target_system
        self.target_component = self.myMav.target_component
        
        self.progress(f"Heartbeat from system {self.target_system}, component {self.target_component}")

    def send_rc_command(self,rc_channel_values):
        rc_channel_values_as_int = [int(x) for x in rc_channel_values]
        self.myMav.mav.rc_channels_override_send(
            self.target_system,
            self.target_component,
            *rc_channel_values_as_int,
            0, 0, 0, 0
        )
        
    def arm_copter(self):
        self.progress("arm throttle")
        while self.isArmed is False:
            self.myMav.mav.command_long_send(
            self.target_system,            # Target system ID
            self.target_component,         # Target component ID
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Command ID for arming/disarming
            0,                               # Confirmation
            1,                               # Arm (1) or disarm (0)
            0, 0, 0, 0, 0, 0, 0              # Parameters (not used in this command)
            )
            response = self.myMav.recv_match(type='COMMAND_ACK', blocking=True)
            if response.command==400 and response.result==0:
                self.progress(f"command: {response.command}, result: {response.result}")
                self.isArmed = True
            time.sleep(0.1)
        self.progress("autopilot is armed") 
        return self.isArmed

    def get_gps(self):
        while True:
            time.sleep(0.1)
            self.myMav.mav.command_long_send(
            self.target_system,  # Target system ID
            self.target_component,  # Target component ID
            512,  # Command ID's - MAV_CMD_REQUEST_MESSAGE
            0,  # Confirmation
            33,  # Message ID to request - GLOBAL_POSITION_INT
            0, 0, 0, 0, 0, 0,   # Params 1-7 (not used, set to 0)
            0,  # Param 8 (request rate in HZ, 0 for once)
            )

            pos_msg = self.myMav.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
            if pos_msg:       
                alt = (pos_msg.alt / 1000.0) - 584.09
                lat = pos_msg.lat / 10000000
                long = pos_msg.lon / 10000000
                heading = pos_msg.hdg / 100
                self.progress(f"GLOBAL_POSITION_INT : lat={lat}, long={long}, heading={heading}")
                break
        return alt

    def get_attitude(self):

        roll = 0
        pitch = 0
        yaw = 0

        while True:
            time.sleep(0.1)

            self.myMav.mav.command_long_send(
            self.target_system,  # Target system ID
            self.target_component,  # Target component ID
            512,  # Command ID's - MAV_CMD_REQUEST_MESSAGE
            0,  # Confirmation
            30,  # Message ID to request - GLOBAL_POSITION_INT
            0, 0, 0, 0, 0, 0,   # Params 1-7 (not used, set to 0)
            0,  # Param 8 (request rate in HZ, 0 for once)
            )

            atti_msg = self.myMav.recv_match(type="ATTITUDE", blocking=False)

            if atti_msg:
                roll = atti_msg.roll
                pitch = atti_msg.pitch
                yaw = atti_msg.yaw
                break 

        return (roll,pitch,yaw)  


    def takeoff_to100(self):
        self.progress("starting takeoff...")

        self.myMav.mav.command_long_send(
            self.target_system,  # Target system ID
            self.target_component,  # Target component ID
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,0,  # Command ID's - MAV_CMD_REQUEST_MESSAGE
            0,0,0,0,0,0,100
        )

        while True:
            time.sleep(0.1)

            self.myMav.mav.command_long_send(
            self.target_system,  # Target system ID
            self.target_component,  # Target component ID
            512,  # Command ID's - MAV_CMD_REQUEST_MESSAGE
            0,  # Confirmation
            30,  # Message ID to request - GLOBAL_POSITION_INT
            0, 0, 0, 0, 0, 0,   # Params 1-7 (not used, set to 0)
            0,  # Param 8 (request rate in HZ, 0 for once)
            )

            pos_msg = self.myMav.recv_match(type="GLOBAL_POSITION_INT", blocking=False)
            if pos_msg:       
                alt = (pos_msg.alt / 1000.0) - 584.09
                self.progress(f"GLOBAL_POSITION_INT : altitude = {alt}")
                if 99 < alt < 100:
                    break
        self.progress("copter in 100 m")
            
    def close(self):
        self.myMav.close()
        self.progress("mavlink closed")

        
    def progress(self,args):
        print(f"MAV: {args}")
        pass















    # # Wait for a while to observe the changes (adjust as needed)
    # time.sleep(5)

    # # You can also receive and print the current RC_CHANNELS message to verify the changes
    # msg = master.recv_match(type='RC_CHANNELS', blocking=True)
    # print(f"Received RC_CHANNELS message: {msg}")

    # # Close the connection
    # master.close()
