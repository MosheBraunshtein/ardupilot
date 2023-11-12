from pymavlink import mavutil
import time






def connect():

    # Set the connection string. For example, for a serial connection, it could be something like 'com4' or '/dev/ttyUSB0'.
    connection_string = 'udp:172.17.0.2:14551'   # Change this to your connection string

    # Create a MAVLink connection
    master = mavutil.mavlink_connection(connection_string)

    print("wait")
    # Wait for the connection to be established
    master.wait_heartbeat()
    print("got connection")

    # Print some information about the vehicle
    print(f"Heartbeat from system {master.target_system}, component {master.target_component}")

    # Set the target system and component IDs for sending messages
    target_system = master.target_system
    target_component = master.target_component

    # Specify the channel values (use your own values)
    rc_channel_values = [1500, 1500, 1500, 1500, 0, 0, 0, 0]

    isArmed = False
    print("arm throttle")
    while isArmed is False:
        master.mav.command_long_send(
        master.target_system,            # Target system ID
        master.target_component,         # Target component ID
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Command ID for arming/disarming
        0,                               # Confirmation
        1,                               # Arm (1) or disarm (0)
        0, 0, 0, 0, 0, 0, 0              # Parameters (not used in this command)
        )
        response = master.recv_match(type='COMMAND_ACK', blocking=True)
        if response.command==400 and response.result==0:
            print(f"command: {response.command}, result: {response.result}")
            isArmed = True
        time.sleep(0.1)
    print("autopilot is armed")    




    print("send rc")
    # Send the RC_CHANNELS_OVERRIDE message
    while True:
        time.sleep(0.1)
        master.mav.rc_channels_override_send(
            target_system,
            target_component,
            *rc_channel_values
        )

        master.mav.command_long_send(
        master.target_system,  # Target system ID
        master.target_component,  # Target component ID
        512,  # Command ID's - MAV_CMD_REQUEST_MESSAGE
        0,  # Confirmation
        33,  # Message ID to request - GLOBAL_POSITION_INT
        0, 0, 0, 0, 0, 0,   # Params 1-7 (not used, set to 0)
        0,  # Param 8 (request rate in HZ, 0 for once)
        )

        pos_msg = master.recv_match(type="GLOBAL_POSITION_INT", blocking=False)

        if pos_msg:       
            alt = (pos_msg.alt / 1000.0) - 584.09
            print(f"alt: {alt}")
            if (alt > 75.0):
                rc_channel_values = [1500, 1367, 1400, 1500, 0, 0, 0, 0]   




        # atti_msg = master.recv_match(type="ATTITUDE", blocking=False)
        # if atti_msg:
        #     print(atti_msg) 




















    # # Wait for a while to observe the changes (adjust as needed)
    # time.sleep(5)

    # # You can also receive and print the current RC_CHANNELS message to verify the changes
    # msg = master.recv_match(type='RC_CHANNELS', blocking=True)
    # print(f"Received RC_CHANNELS message: {msg}")

    # # Close the connection
    # master.close()
