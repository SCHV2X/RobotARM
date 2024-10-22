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

from dynamixel_sdk import *

# DYNAMIXEL 설정
ADDR_TORQUE_ENABLE          = 64      # 토크 활성화 주소
ADDR_GOAL_POSITION          = 116     # 목표 위치 주소
ADDR_PRESENT_POSITION       = 132     # 현재 위치 주소

ADDR_OPERATING_MODE = 11              # 동작 모드 설정 주소

ADDR_PROFILE_ACCELERATION = 108       # 가속도 프로파일 주소
ADDR_PROFILE_VELOCITY = 112           # 속도 프로파일 주소

ADDR_DRIVE_MODE = 10                  # 드라이브 모드 주소

ADDR_HOMING_OFFSET = 20               # 홈 오프셋 설정 주소

DXL_MINIMUM_POSITION_VALUE  = 0       # 최소 위치 값 (eManual 참조)
DXL_MAXIMUM_POSITION_VALUE  = 2300    # 최대 위치 값 (eManual 참조)
DXL_REVERSE_MODE_VALUE = 0x01         # 시계방향(정방향) 설정 값
DXL_HOMING_OFFSET_VALUE = 1023        # 홈 오프셋 값

BAUDRATE = 57600                      # 통신 속도 (Baudrate)

PROTOCOL_VERSION = 2.0                # 프로토콜 버전 (1.0 / 2.0)

DXL_ID = 1                            # Dynamixel ID

DEVICENAME = '/dev/ttyARM'            # 포트 이름

TORQUE_ENABLE = 1                     # 토크 활성화 값
TORQUE_DISABLE = 0                    # 토크 비활성화 값
DXL_MOVING_STATUS_THRESHOLD = 20      # Dynamixel 움직임 상태 임계값

index = 0

# 포트 핸들러 초기화
portHandler = PortHandler(DEVICENAME)

# 패킷 핸들러 초기화
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 포트 열기
if portHandler.openPort():
    print("포트를 성공적으로 열었습니다")
else:
    print("포트 열기 실패")
    print("아무 키나 눌러서 종료하세요...")
    getch()
    quit()

# 통신 속도 설정
if portHandler.setBaudRate(BAUDRATE):
    print("통신 속도를 성공적으로 변경했습니다")
else:
    print("통신 속도 변경 실패")
    print("아무 키나 눌러서 종료하세요...")
    getch()
    quit()

# 속도 및 가속도 프로파일 설정 함수
def set_profile_velocity_acceleration(velocity, acceleration):
    # 속도 설정
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"속도 설정 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"오류: {packetHandler.getRxPacketError(dxl_error)}")
    
    # 가속도 설정
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_ACCELERATION, acceleration)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"가속도 설정 오류: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"오류: {packetHandler.getRxPacketError(dxl_error)}")
        
# 프로파일 속도 및 가속도 값 예시
PROFILE_VELOCITY = 100  # 설정 값 (rev/min)
PROFILE_ACCELERATION = 50  # 설정 값 (rev/min^2)

# 속도 및 가속도 설정
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION)

# 드라이브 모드 설정
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_DRIVE_MODE, DXL_REVERSE_MODE_VALUE)

# 동작 모드 설정
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, 3)

# 0점 조절
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_HOMING_OFFSET, DXL_HOMING_OFFSET_VALUE)

# 토크 활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel이 성공적으로 연결되었습니다")

# 루프 실행
while 1:
    print("아무 키나 눌러서 계속하세요! (종료하려면 ESC를 누르세요)")
    if getch() == chr(0x1b):
        break

    print(index)

    # 현재 위치 읽기
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

    # 목표 위치 설정 및 증가
    if index == 2300:
        break
    else:
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, index)
        print("목표 위치 설정")
        
        index += 100
        print(index)
        
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

    # 현재 위치 다시 읽기
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4
