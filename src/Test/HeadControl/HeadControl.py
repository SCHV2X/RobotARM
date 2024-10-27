# -*- coding: utf-8 -*-
import os
import time

# 운영체제에 따라 키 입력 함수 정의 (Windows와 Unix 계열 OS의 차이)
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

# Dynamixel SDK 불러오기
from dynamixel_sdk import * 

# 모터 모델 설정
MY_DXL = 'X_SERIES'       

# 제어 테이블 주소 설정
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64              # 토크 활성화 주소
    ADDR_GOAL_POSITION          = 116             # 목표 위치 주소
    ADDR_PRESENT_POSITION       = 132             # 현재 위치 주소
    
    ADDR_DRIVE_MODE = 10                           # 구동 모드 주소
    ADDR_OPERATING_MODE = 11                       # 작동 모드 주소
    
    ADDR_PROFILE_ACCELERATION = 108                # 가속도 프로파일 주소
    ADDR_PROFILE_VELOCITY = 112                    # 속도 프로파일 주소
    
    DXL_MINIMUM_POSITION_VALUE  = 1800             # 최소 위치 값
    DXL_MAXIMUM_POSITION_VALUE  = 2550             # 최대 위치 값
    BAUDRATE                    = 57600            # 통신 속도

# 프로토콜 버전 설정
PROTOCOL_VERSION            = 2.0

# Dynamixel ID 설정
DXL_ID                      = 9                   # 첫 번째 모터 ID
DXL2_ID                      = 8                  # 두 번째 모터 ID

# 장치 이름 설정 (U2D2 장치와 연결된 포트)
DEVICENAME                  = '/dev/ttyARM'

# 토크 활성화/비활성화 값 정의
TORQUE_ENABLE               = 1                   # 토크 활성화 값
TORQUE_DISABLE              = 0                   # 토크 비활성화 값
DXL_MOVING_STATUS_THRESHOLD = 20                  # 모터 이동 상태 임계값

# 각도 조정 값 정의
step = 75                                          
step_2 = 200

# 목표 위치 정의
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE + DXL_MOVING_STATUS_THRESHOLD, 
                     DXL_MAXIMUM_POSITION_VALUE - DXL_MOVING_STATUS_THRESHOLD]  

# 포트 핸들러 및 패킷 핸들러 설정
portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# 포트 열기
if portHandler.openPort():
    print("포트 열기에 성공했습니다.")
else:
    print("포트 열기에 실패했습니다.")
    print("아무 키나 눌러 종료...")
    getch()
    quit()

# 통신 속도 설정
if portHandler.setBaudRate(BAUDRATE):
    print("통신 속도 설정에 성공했습니다.")
else:
    print("통신 속도 설정에 실패했습니다.")
    print("아무 키나 눌러 종료...")
    getch()
    quit()

# 속도 및 가속도 설정 함수
def set_profile_velocity_acceleration(velocity, acceleration):
    # 속도 설정
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_VELOCITY, velocity)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"속도 설정 에러: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"에러: {packetHandler.getRxPacketError(dxl_error)}")
    
    # 가속도 설정
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PROFILE_ACCELERATION, acceleration)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"가속도 설정 에러: {packetHandler.getTxRxResult(dxl_comm_result)}")
    elif dxl_error != 0:
        print(f"에러: {packetHandler.getRxPacketError(dxl_error)}")

# 속도와 가속도 값 설정
PROFILE_VELOCITY = 60     # 속도 설정 값 (rev/min)
PROFILE_ACCELERATION = 20  # 가속도 설정 값 (rev/min^2)

# 작동 모드 설정
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, 3)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_OPERATING_MODE, 3)

# 속도 및 가속도 설정 호출
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION)
set_profile_velocity_acceleration(PROFILE_VELOCITY, PROFILE_ACCELERATION)

# 초기 위치로 이동 설정
# 모터 1의 목표 위치 설정
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[0])
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# 모터 2의 목표 위치 설정
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, dxl_goal_position[0])
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# 모터 토크 활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel이 성공적으로 연결되었습니다.")

# 키 입력을 통한 제어 루프
while 1:
    print("아무 키나 눌러 계속 진행! (ESC를 눌러 종료)")
    key_input = getch()
    
    # ESC 키 입력 시 종료
    if key_input == chr(0x1b):
        break
    
    # '1' 키 입력 시 모터를 조임
    elif key_input == '1':
        present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        
        print(f"{present_position}")
        
        if present_position + step >= dxl_goal_position[1]:
            print(f"최대 각도에 도달")
        else:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, present_position + step)
        
    # '2' 키 입력 시 모터를 풂
    elif key_input == '2':
        present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
        
        print(f"{present_position}")
        
        if present_position - step <= dxl_goal_position[0]:
            print(f"최소 각도에 도달")
        else:
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, present_position - step)
    
    # '3' 키 입력 시 집게 몸통 부분을 오른쪽으로 회전
    elif key_input == '3':
        present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION)
        
        print(f"{present_position}")
        
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, present_position + step_2)
    
    # '4' 키 입력 시 집게 몸통 부분을 왼쪽으로 회전
    elif key_input == '4':
        present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL2_ID, ADDR_PRESENT_POSITION)
        
        print(f"{present_position}")
        
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL2_ID, ADDR_GOAL_POSITION, present_position - step_2)
    
    # '5' 키 입력 시 집게를 잡고 2초 후 다시 풀기
    elif key_input == '5':
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[0])
            
        time.sleep(0.5)
        
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[1])
        
        time.sleep(2)
    
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, dxl_goal_position[0])

# 토크 비활성화 및 포트 닫기
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# 포트 닫기
portHandler.closePort()
