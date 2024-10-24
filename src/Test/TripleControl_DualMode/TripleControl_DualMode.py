#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430

# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    LEN_GOAL_POSITION           = 4         # Data Byte Length
    
    ADDR_PROFILE_ACCELERATION = 108  # Profile Acceleration address
    ADDR_PROFILE_VELOCITY = 112      # Profile Velocity address
    
    ADDR_PRESENT_POSITION       = 132
    ADDR_DRIVE_MODE = 10
    ADDR_OPERATING_MODE = 11
    LEN_PRESENT_POSITION        = 4         # Data Byte Length
    
    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 500       # Refer to the Maximum Position Limit of product eManual
    DXL_2_MINIMUM_POSITION_VALUE = 0        # Refer to the Minimum Position Limit of product eManual
    DXL_2_MAXIMUM_POSITION_VALUE  = 1800    # Refer to the Maximum Position Limit of product eManual
    DXL_4_MINIMUM_POSITION_VALUE = 0        # Refer to the Minimum Position Limit of product eManual
    DXL_4_MAXIMUM_POSITION_VALUE  = 1800    # Refer to the Maximum Position Limit of product eManual
    
    DXL_REVERSE_MODE_VALUE = 0x01           # 시계방향(시계 방향)
    DXL_NORMAL_MODE_VALUE = 0x00            # 시계방향(반시계 방향) - 디폴트
    DXL_REVERSE_SLAVE_MODE_VALUE = 0x02     # slave 설정
    BAUDRATE                    = 57600



PROTOCOL_VERSION            = 2.0

# Make sure that each DYNAMIXEL ID should have unique ID.
DXL1_ID                     = 1                 # Dynamixel#1 ID : 1 
DXL2_ID                     = 2                 # Dynamixel#1 ID : 2 Master
DXL3_ID                     = 3                 # Dynamixel#1 ID : 3 slave
DXL4_ID                     = 4                 # Dynamixel#1 ID : 4 Master
DXL5_ID                     = 5                 # Dynamixel#1 ID : 5 slave

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyARM'

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

# Example values for Profile Velocity and Acceleration
PROFILE_VELOCITY = 100  # 속도 (rev/min)
PROFILE_ACCELERATION = 50  # 가속도 (rev/min^2)


index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # DXL_1_Goal position
dxl_2_goal_position = [DXL_2_MINIMUM_POSITION_VALUE, DXL_2_MAXIMUM_POSITION_VALUE]   # DXL_2_Goal position
dxl_4_goal_position = [DXL_4_MINIMUM_POSITION_VALUE, DXL_4_MAXIMUM_POSITION_VALUE]   # DXL_4_Goal position

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupSyncWrite instance
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# Initialize GroupSyncRead instace for Present Position
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# 속도 조절
def set_profile_velocity_acceleration(velocity, acceleration, dxl_id):
    # Set Profile Velocity
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_PROFILE_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error setting velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error: {packetHandler.getRxPacketError(dxl_error)}")
    
    # Set Profile Acceleration
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, dxl_id, ADDR_PROFILE_ACCELERATION, acceleration)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Error setting acceleration: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"Error: {packetHandler.getRxPacketError(dxl_error)}")
        
        
# Operating_Mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL5_ID, ADDR_OPERATING_MODE, 3)

# 드라이브 모드 (회전방향을 시계방향으로 설정)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_DRIVE_MODE, DXL_REVERSE_MODE_VALUE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_DRIVE_MODE, DXL_NORMAL_MODE_VALUE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_DRIVE_MODE, DXL_NORMAL_MODE_VALUE)

# 드라이브 모드 (master-slave 설정)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL3_ID, ADDR_DRIVE_MODE, DXL_REVERSE_SLAVE_MODE_VALUE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL5_ID, ADDR_DRIVE_MODE, DXL_REVERSE_SLAVE_MODE_VALUE)


# Set the velocity and acceleration
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL1_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL2_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL4_ID)

        

# Enable Dynamixel#1 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL1_ID)

# Enable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL2_ID)
    
# Enable Dynamixel#4 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % DXL4_ID)

# Add parameter storage for Dynamixel#1 present position value
dxl_addparam_result = groupSyncRead.addParam(DXL1_ID)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam failed" % DXL1_ID)
    quit()

# Add parameter storage for Dynamixel#2 present position value
dxl_addparam_result = groupSyncRead.addParam(DXL2_ID)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam failed" % DXL2_ID)
    quit()
    
# Add parameter storage for Dynamixel#2 present position value
dxl_addparam_result = groupSyncRead.addParam(DXL4_ID)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam failed" % DXL4_ID)
    quit()


while 1:
    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    # Allocate goal position value into byte array
    param_goal_position = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position[index]))]

    param_goal_position2 = [DXL_LOBYTE(DXL_LOWORD(dxl_2_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_2_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_2_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_2_goal_position[index]))]
    
    param_goal_position4 = [DXL_LOBYTE(DXL_LOWORD(dxl_4_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_4_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_4_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_4_goal_position[index]))]
    
    # Add Dynamixel#1 goal position value to the Syncwrite parameter storage
    dxl_addparam_result = groupSyncWrite.addParam(DXL1_ID, param_goal_position)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL1_ID)
        quit()

    # Add Dynamixel#2 goal position value to the Syncwrite parameter storage
    dxl_addparam_result = groupSyncWrite.addParam(DXL2_ID, param_goal_position2)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL2_ID)
        quit()
        
    # Add Dynamixel#4 goal position value to the Syncwrite parameter storage
    dxl_addparam_result = groupSyncWrite.addParam(DXL4_ID, param_goal_position2)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncWrite addparam failed" % DXL4_ID)
        quit()

    # Syncwrite goal position
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    # Clear syncwrite parameter storage
    groupSyncWrite.clearParam()

    while 1:
        # Syncread present position
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Check if groupsyncread data of Dynamixel#1 is available
        dxl_getdata_result = groupSyncRead.isAvailable(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % DXL1_ID)
            quit()

        # Check if groupsyncread data of Dynamixel#2 is available
        dxl_getdata_result = groupSyncRead.isAvailable(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % DXL2_ID)
            quit()
            
        # Check if groupsyncread data of Dynamixel#4 is available
        dxl_getdata_result = groupSyncRead.isAvailable(DXL4_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata failed" % DXL4_ID)
            quit()

        # Get Dynamixel#1 present position value
        dxl1_present_position = groupSyncRead.getData(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        # Get Dynamixel#2 present position value
        dxl2_present_position = groupSyncRead.getData(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        
        # Get Dynamixel#4 present position value
        dxl4_present_position = groupSyncRead.getData(DXL4_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d\t[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_2_goal_position[index], dxl2_present_position, DXL4_ID, dxl_4_goal_position[index], dxl4_present_position))

        if not ((abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD) or (abs(dxl_2_goal_position[index] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD) or (abs(dxl_4_goal_position[index] - dxl4_present_position) > DXL_MOVING_STATUS_THRESHOLD)):
            break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0

# Clear syncread parameter storage
groupSyncRead.clearParam()

# Disable Dynamixel#1 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Disable Dynamixel#2 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Disable Dynamixel#4 Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
    
# Close port
portHandler.closePort()
