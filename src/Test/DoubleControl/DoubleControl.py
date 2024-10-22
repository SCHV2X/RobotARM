#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# 이 코드는 Apache License, Version 2.0에 따라 사용이 허가됩니다.
# 이 라이센스를 준수하지 않는 한 이 파일을 사용할 수 없습니다.
# 라이센스 사본은 아래에서 확인할 수 있습니다:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 법률에서 요구되거나 서면으로 동의하지 않는 한, 소프트웨어는
# "있는 그대로" 배포되며, 명시적이거나 묵시적인 어떠한 보증도 제공하지 않습니다.
# 라이센스에 따른 권한과 제한 사항은 라이센스를 참고하십시오.
################################################################################


#*******************************************************************************
#***********************     SyncRead와 SyncWrite 예제    ***********************
#  이 예제를 실행하기 위한 환경 :
#    - Protocol 2.0을 지원하는 DYNAMIXEL(X, P, PRO/PRO(A), MX 2.0 시리즈)
#    - DYNAMIXEL Starter Set (U2D2, U2D2 PHB, 12V SMPS)
#  예제 사용 방법 :
#    - 예제 코드에서 사용 중인 DYNAMIXEL을 MY_DXL에 선택합니다.
#    - 적절한 아키텍처 하위 디렉토리에서 빌드 및 실행합니다.
#    - Raspberry Pi와 같은 ARM 기반 SBC의 경우, linux_sbc 하위 디렉토리를 사용하여 빌드하고 실행합니다.
#    - https://emanual.robotis.com/docs/ko/software/dynamixel/dynamixel_sdk/overview/
#  작성자: Ryu Woon Jung (Leon)
#  관리자: Zerom, Will Son
# *******************************************************************************

import os

# Windows일 경우
if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:  # Linux, Mac 등
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

from dynamixel_sdk import *                    # Dynamixel SDK 라이브러리 사용

#********* DYNAMIXEL 모델 정의 *********
#***** (한 번에 하나의 정의만 사용) *****
MY_DXL = 'X_SERIES'       # X330 (권장 전압: 5.0V), X430, X540, 2X430
# MY_DXL = 'MX_SERIES'    # 2.0 펌웨어 업데이트가 적용된 MX 시리즈
# MY_DXL = 'PRO_SERIES'   # H54, H42, M54, M42, L54, L42
# MY_DXL = 'PRO_A_SERIES' # (A) 펌웨어 업데이트가 적용된 PRO 시리즈
# MY_DXL = 'P_SERIES'     # PH54, PH42, PM54
# MY_DXL = 'XL320'        # [경고] 동작 전압: 7.4V

# 제어 테이블 주소
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64      # 토크 활성화 주소
    ADDR_GOAL_POSITION          = 116     # 목표 위치 주소
    LEN_GOAL_POSITION           = 4       # 데이터 바이트 길이
    ADDR_PRESENT_POSITION       = 132     # 현재 위치 주소
    LEN_PRESENT_POSITION        = 4       # 데이터 바이트 길이
    DXL_MINIMUM_POSITION_VALUE  = 0       # 제품 eManual의 최소 위치 제한 참고
    DXL_MAXIMUM_POSITION_VALUE  = 500     # 제품 eManual의 최대 위치 제한 참고
    BAUDRATE                    = 57600   # 통신 속도
elif MY_DXL == 'PRO_SERIES':
    ADDR_TORQUE_ENABLE          = 562     # PRO 시리즈의 제어 테이블 주소는 다릅니다.
    ADDR_GOAL_POSITION          = 596
    LEN_GOAL_POSITION           = 4
    ADDR_PRESENT_POSITION       = 611
    LEN_PRESENT_POSITION        = 4
    DXL_MINIMUM_POSITION_VALUE  = -150000   # 제품 eManual의 최소 위치 제한 참고
    DXL_MAXIMUM_POSITION_VALUE  = 150000    # 제품 eManual의 최대 위치 제한 참고
    BAUDRATE                    = 57600
elif MY_DXL == 'P_SERIES' or MY_DXL == 'PRO_A_SERIES':
    ADDR_TORQUE_ENABLE          = 512        # 제어 테이블 주소가 DYNAMIXEL 모델마다 다릅니다.
    ADDR_GOAL_POSITION          = 564
    LEN_GOAL_POSITION           = 4          # 데이터 바이트 길이
    ADDR_PRESENT_POSITION       = 580
    LEN_PRESENT_POSITION        = 4          # 데이터 바이트 길이
    DXL_MINIMUM_POSITION_VALUE  = -150000    # 제품 eManual의 최소 위치 제한 참고
    DXL_MAXIMUM_POSITION_VALUE  = 150000     # 제품 eManual의 최대 위치 제한 참고
    BAUDRATE                    = 57600

# DYNAMIXEL 프로토콜 버전 (1.0 / 2.0)
# https://emanual.robotis.com/docs/ko/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# 각 DYNAMIXEL ID는 고유해야 합니다.
DXL1_ID                     = 1                 # DYNAMIXEL#1 ID : 1
DXL2_ID                     = 2                 # DYNAMIXEL#2 ID : 2

# U2D2에 할당된 실제 포트를 사용하십시오.
# 예) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyARM'

TORQUE_ENABLE               = 1                 # 토크 활성화 값
TORQUE_DISABLE              = 0                 # 토크 비활성화 값
DXL_MOVING_STATUS_THRESHOLD = 20                # DYNAMIXEL 이동 상태 임계값

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE, DXL_MAXIMUM_POSITION_VALUE]         # 목표 위치 설정

# PortHandler 인스턴스 초기화
# 포트 경로 설정
# PortHandlerLinux 또는 PortHandlerWindows의 메소드 및 멤버 가져오기
portHandler = PortHandler(DEVICENAME)

# PacketHandler 인스턴스 초기화
# 프로토콜 버전 설정
# Protocol1PacketHandler 또는 Protocol2PacketHandler의 메소드 및 멤버 가져오기
packetHandler = PacketHandler(PROTOCOL_VERSION)

# GroupSyncWrite 인스턴스 초기화
groupSyncWrite = GroupSyncWrite(portHandler, packetHandler, ADDR_GOAL_POSITION, LEN_GOAL_POSITION)

# 현재 위치를 위한 GroupSyncRead 인스턴스 초기화
groupSyncRead = GroupSyncRead(portHandler, packetHandler, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

# 포트 열기
if portHandler.openPort():
    print("포트 열기 성공")
else:
    print("포트 열기 실패")
    print("아무 키나 눌러 종료...")
    getch()
    quit()


# 포트 통신 속도 설정
if portHandler.setBaudRate(BAUDRATE):
    print("통신 속도 변경 성공")
else:
    print("통신 속도 변경 실패")
    print("아무 키나 눌러 종료...")
    getch()
    quit()


# Dynamixel#1 토크 활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d가 성공적으로 연결되었습니다." % DXL1_ID)

# Dynamixel#2 토크 활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d가 성공적으로 연결되었습니다." % DXL2_ID)

# Dynamixel#1 현재 위치 값에 대한 파라미터 저장 추가
dxl_addparam_result = groupSyncRead.addParam(DXL1_ID)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam 실패" % DXL1_ID)
    quit()

# Dynamixel#2 현재 위치 값에 대한 파라미터 저장 추가
dxl_addparam_result = groupSyncRead.addParam(DXL2_ID)
if dxl_addparam_result != True:
    print("[ID:%03d] groupSyncRead addparam 실패" % DXL2_ID)
    quit()

while 1:
    print("아무 키나 눌러 계속하세요! (ESC 키를 눌러 종료)")
    if getch() == chr(0x1b):
        break

    # 목표 위치 값을 바이트 배열로 할당
    param_goal_position = [DXL_LOBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_LOWORD(dxl_goal_position[index])), DXL_LOBYTE(DXL_HIWORD(dxl_goal_position[index])), DXL_HIBYTE(DXL_HIWORD(dxl_goal_position[index]))]

    # Syncwrite 파라미터 저장소에 Dynamixel#1 목표 위치 값 추가
    dxl_addparam_result = groupSyncWrite.addParam(DXL1_ID, param_goal_position)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncWrite addparam 실패" % DXL1_ID)
        quit()

    # Syncwrite 파라미터 저장소에 Dynamixel#2 목표 위치 값 추가
    dxl_addparam_result = groupSyncWrite.addParam(DXL2_ID, param_goal_position)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupSyncWrite addparam 실패" % DXL2_ID)
        quit()

    # 목표 위치 Syncwrite 실행
    dxl_comm_result = groupSyncWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    # Syncwrite 파라미터 저장소 초기화
    groupSyncWrite.clearParam()

    while 1:
        # 현재 위치 Syncread 실행
        dxl_comm_result = groupSyncRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

        # Dynamixel#1의 Syncread 데이터가 사용 가능한지 확인
        dxl_getdata_result = groupSyncRead.isAvailable(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata 실패" % DXL1_ID)
            quit()

        # Dynamixel#2의 Syncread 데이터가 사용 가능한지 확인
        dxl_getdata_result = groupSyncRead.isAvailable(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupSyncRead getdata 실패" % DXL2_ID)
            quit()

        # Dynamixel#1의 현재 위치 값 가져오기
        dxl1_present_position = groupSyncRead.getData(DXL1_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        # Dynamixel#2의 현재 위치 값 가져오기
        dxl2_present_position = groupSyncRead.getData(DXL2_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        print("[ID:%03d] 목표 위치:%03d  현재 위치:%03d\t[ID:%03d] 목표 위치:%03d  현재 위치:%03d" % (DXL1_ID, dxl_goal_position[index], dxl1_present_position, DXL2_ID, dxl_goal_position[index], dxl2_present_position))

        if not ((abs(dxl_goal_position[index] - dxl1_present_position) > DXL_MOVING_STATUS_THRESHOLD) and (abs(dxl_goal_position[index] - dxl2_present_position) > DXL_MOVING_STATUS_THRESHOLD)):
            break

    # 목표 위치 변경
    if index == 0:
        index = 1
    else:
        index = 0

# Syncread 파라미터 저장소 초기화
groupSyncRead.clearParam()

# Dynamixel#1 토크 비활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL1_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Dynamixel#2 토크 비활성화
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL2_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# 포트 닫기
portHandler.closePort()
