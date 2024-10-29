#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time

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

from dynamixel_sdk import * # Uses Dynamixel SDK library

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
    
ADDR_DRIVE_MODE = 10
ADDR_OPERATING_MODE = 11
    
ADDR_PROFILE_ACCELERATION = 108  # Profile Acceleration address
ADDR_PROFILE_VELOCITY = 112      # Profile Velocity address

DXL_REVERSE_MODE_VALUE = 0x01           # 시계방향(시계 방향)
DXL_NORMAL_MODE_VALUE = 0x00            # 시계방향(반시계 방향) - 디폴트

DXL_NORMAL_SLAVE_MODE_VALUE = 0x02     # slave 설정
DXL_REVERSE_SLAVE_MODE_VALUE = 0x03

# 0 ~ 4095 범위 안에서 설정
DXL_MINIMUM_POSITION_VALUE_1 = 1000
DXL_MAXIMUM_POSITION_VALUE_1 = 3000

DXL_MINIMUM_POSITION_VALUE_2 = 230
DXL_MAXIMUM_POSITION_VALUE_2 = 2400

DXL_MINIMUM_POSITION_VALUE_4 = 50
DXL_MAXIMUM_POSITION_VALUE_4 = 2047

DXL_MINIMUM_POSITION_VALUE_6 = 2050
DXL_MAXIMUM_POSITION_VALUE_6 = 4095

DXL_MINIMUM_POSITION_VALUE_7 = 0
DXL_MAXIMUM_POSITION_VALUE_7 = 4095

DXL_MINIMUM_POSITION_VALUE_8 = 0
DXL_MAXIMUM_POSITION_VALUE_8 = 4095

DXL_MINIMUM_POSITION_VALUE_9 = 1800
DXL_MAXIMUM_POSITION_VALUE_9 = 2550

BAUDRATE                    = 57600

# DYNAMIXEL Protocol Version (1.0 / 2.0)
PROTOCOL_VERSION            = 2.0

DXL1_ID                      = 1

DXL2_ID                      = 2
DXL3_ID                      = 3

DXL4_ID                      = 4
DXL5_ID                      = 5

DXL6_ID                      = 6

DXL7_ID                      = 7

DXL8_ID                      = 8

DXL9_ID                      = 9

# Use the actual port assigned to the U2D2.
DEVICENAME                  = '/dev/ttyARM'

TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

# 키보드 누를 때마다 움직이는 범위
step_1 = 50
step_2 = 50
step_4 = 100
step_6 = 100
step_7 = 100
step_8 = 200
step_9 = 75

# Goal position
dxl_goal_position_1 = [DXL_MINIMUM_POSITION_VALUE_1 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_1 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_2 = [DXL_MINIMUM_POSITION_VALUE_2 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_2 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_4 = [DXL_MINIMUM_POSITION_VALUE_4 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_4 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_6 = [DXL_MINIMUM_POSITION_VALUE_6 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_6 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_7 = [DXL_MINIMUM_POSITION_VALUE_7 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_7 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_8 = [DXL_MINIMUM_POSITION_VALUE_8 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_8 - DXL_MOVING_STATUS_THRESHOLD]
dxl_goal_position_9 = [DXL_MINIMUM_POSITION_VALUE_9 + DXL_MOVING_STATUS_THRESHOLD, DXL_MAXIMUM_POSITION_VALUE_9 - DXL_MOVING_STATUS_THRESHOLD]

portHandler = PortHandler(DEVICENAME)

packetHandler = PacketHandler(PROTOCOL_VERSION)

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
    
# 속도 및 가속도 세팅 함수
def set_profile_velocity_acceleration(velocity, acceleration, ID):
    # Set Profile Velocity
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID, ADDR_PROFILE_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"[속도 세팅 함수] Error setting velocity: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"[속도 세팅 함수] Error: {packetHandler.getRxPacketError(dxl_error)}")
    
    # Set Profile Acceleration
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID, ADDR_PROFILE_ACCELERATION, acceleration)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"[가속도 세팅 함수] Error setting acceleration: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"[가속도 세팅 함수] Error: {packetHandler.getRxPacketError(dxl_error)}")

# 초기 위치 함수
def set_init_position(ID, minPosition):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, ID, ADDR_GOAL_POSITION, minPosition)
    if dxl_comm_result != COMM_SUCCESS:
        print("[초기 위치 함수] %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("[초기 위치 함수] %s" % packetHandler.getRxPacketError(dxl_error))

# 토크 설정 함수
def Enable_Torque(T_ENABLE, ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDR_TORQUE_ENABLE, T_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("[토크 설정 함수] %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("[토크 설정 함수] %s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

# 토크 해제 함수       
def Disable_Torque(T_ENABLE, ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDR_TORQUE_ENABLE, T_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("[토크 해제 함수] %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("[토크 해제 함수] %s" % packetHandler.getRxPacketError(dxl_error))
        
# 드라이브 모드 (master-slave 설정)
def durl_mode(ID):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, ID, ADDR_DRIVE_MODE, DXL_REVERSE_SLAVE_MODE_VALUE)
    if dxl_comm_result != COMM_SUCCESS:
        print("[드라이브 모드 (master-slave 설정)] %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("[드라이브 모드 (master-slave 설정)] %s" % packetHandler.getRxPacketError(dxl_error))

# 속도와 가속도 값 설정
PROFILE_VELOCITY = 40     # Adjust this value (rev/min)
PROFILE_ACCELERATION = 5  # Adjust this value (rev/min^2)

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL6_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL7_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL8_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL9_ID, ADDR_OPERATING_MODE, 3)

# 방향 설정
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_DRIVE_MODE, DXL_REVERSE_MODE_VALUE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_DRIVE_MODE, DXL_NORMAL_MODE_VALUE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL4_ID, ADDR_DRIVE_MODE, DXL_REVERSE_MODE_VALUE)


#슬레이브 모드 ( 듀얼모드)
durl_mode(DXL3_ID)
durl_mode(DXL5_ID)

# 속도 및 가속도 조절
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL1_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL2_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL4_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL6_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL7_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL8_ID)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION, DXL9_ID)

# 초기 위치로 이동
set_init_position(DXL1_ID, 2050)
set_init_position(DXL2_ID, dxl_goal_position_2[0])
set_init_position(DXL4_ID, dxl_goal_position_4[0])
set_init_position(DXL6_ID, dxl_goal_position_6[0])
set_init_position(DXL7_ID, 1500)
set_init_position(DXL8_ID, 1500)
set_init_position(DXL9_ID, dxl_goal_position_9[1])

# Enable Dynamixel Torque
Enable_Torque(TORQUE_ENABLE, DXL1_ID)
Enable_Torque(TORQUE_ENABLE, DXL2_ID)
Enable_Torque(TORQUE_ENABLE, DXL4_ID)
Enable_Torque(TORQUE_ENABLE, DXL6_ID)
Enable_Torque(TORQUE_ENABLE, DXL7_ID)
Enable_Torque(TORQUE_ENABLE, DXL8_ID)
Enable_Torque(TORQUE_ENABLE, DXL9_ID)

while 1:
    print("\n1번부터 9번까지의 숫자를 눌러 모터를 선택할 수 있으며, ESC를 누르면 초기 위치로 이동합니다. \'+\'를 누르면 2번과 4번 모터를 움직여 로봇팔을 세울 수 있습니다.\n")
    key_input = getch()
    
    if key_input == chr(0x1b):  # ESC 키를 누르면 종료
        set_init_position(DXL1_ID, 2050)
        set_init_position(DXL2_ID, dxl_goal_position_2[0])
        set_init_position(DXL4_ID, dxl_goal_position_4[0])
        set_init_position(DXL6_ID, dxl_goal_position_6[0])
        set_init_position(DXL7_ID, 1500)
        set_init_position(DXL8_ID, 1500)
        set_init_position(DXL9_ID, dxl_goal_position_9[1])
        break
    
    # 1번 모터 제어
    elif key_input == '1':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL1_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_1 >= dxl_goal_position_1[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, present_position + step_1)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL1_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_1 <= dxl_goal_position_1[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL1_ID, ADDR_GOAL_POSITION, present_position - step_1)
    # 2번 모터 제어
    elif key_input == '2':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_2 >= dxl_goal_position_2[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, present_position + step_2)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_2 <= dxl_goal_position_2[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, present_position - step_2)
    # 4번 모터 제어
    elif key_input == '4':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL4_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_4 >= dxl_goal_position_4[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, present_position + step_4)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL4_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_4 <= dxl_goal_position_4[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, present_position - step_4)
                    
    # 6번 모터 제어
    elif key_input == '6':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL6_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_6 >= dxl_goal_position_6[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL6_ID, ADDR_GOAL_POSITION, present_position + step_6)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL6_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_6 <= dxl_goal_position_6[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL6_ID, ADDR_GOAL_POSITION, present_position - step_6)
    
    # 7번 모터 제어
    elif key_input == '7':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL7_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_7 >= dxl_goal_position_7[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL7_ID, ADDR_GOAL_POSITION, present_position + step_7)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL7_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_7 <= dxl_goal_position_7[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL7_ID, ADDR_GOAL_POSITION, present_position - step_7)
    # 8번 모터 제어
    elif key_input == '8':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL8_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_8 >= dxl_goal_position_8[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL8_ID, ADDR_GOAL_POSITION, present_position + step_8)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL8_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_8 <= dxl_goal_position_8[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL8_ID, ADDR_GOAL_POSITION, present_position - step_8)
    
    # 9번 모터 제어
    elif key_input == '9':
        print("----모터{key_input}에 들어왔습니다. 종료하려면 0을 누르세요. 움직이려면 .와 /으로 움직이세요")
        while 1:
            key_input_1 = getch()
            if key_input_1 == '0':
                break
            elif key_input_1 == '.':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL9_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position + step_9 >= dxl_goal_position_9[1]:
                    print(f"max angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL9_ID, ADDR_GOAL_POSITION, present_position + step_9)
            elif key_input_1 == '/':
                present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL9_ID, ADDR_PRESENT_POSITION)
                print(f"{present_position}")
                if present_position - step_9 <= dxl_goal_position_9[0]:
                    print(f"min angle")
                else:
                    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL9_ID, ADDR_GOAL_POSITION, present_position - step_9)
    # 2번, 4번 모터 동시 제어 (로봇팔 세우기)
    elif key_input == '=':
        print("----2번, 4번 모터를 동시에 제어합니다. 초기 상태로 이동시키려면 ESC를 누르세요.")
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, 1000)
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL4_ID, ADDR_GOAL_POSITION, 600)
    else :
        print("1,2,3,4,5,6,7,8,9,0,\'=\' 중 선택해주세요. 나가려면 esc를 눌러주세요.")

# Disable Dynamixel Torque
#Disable_Torque(TORQUE_DISABLE, DXL1_ID)
#Disable_Torque(TORQUE_DISABLE, DXL2_ID)
#Disable_Torque(TORQUE_DISABLE, DXL4_ID)
#Disable_Torque(TORQUE_DISABLE, DXL6_ID)
#Disable_Torque(TORQUE_DISABLE, DXL7_ID)
#Disable_Torque(TORQUE_DISABLE, DXL8_ID)
#Disable_Torque(TORQUE_DISABLE, DXL9_ID)


# Close port
portHandler.closePort()
