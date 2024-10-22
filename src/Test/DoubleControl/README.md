# Dynamixel SyncRead 및 SyncWrite 제어 프로그램 설명

이 Python 코드는 **Dynamixel SDK**를 사용하여 두 개의 Dynamixel 모터의 위치를 동기화하여 제어하는 예제입니다. 이 코드는 SyncRead와 SyncWrite 방식을 이용해 두 모터의 목표 위치 설정 및 현재 위치를 읽을 수 있도록 설계되었습니다.

## 주요 변수 및 상수

- **MY_DXL**: 제어할 Dynamixel 모터의 모델을 정의합니다. 이 코드에서는 `X_SERIES`를 사용합니다.
- **ADDR_TORQUE_ENABLE**: 모터의 토크를 활성화하기 위한 주소입니다.
- **ADDR_GOAL_POSITION**: 목표 위치를 설정하는 주소입니다.
- **ADDR_PRESENT_POSITION**: 현재 위치를 읽는 주소입니다.
- **DXL_MINIMUM_POSITION_VALUE**: 모터의 최소 위치 값입니다.
- **DXL_MAXIMUM_POSITION_VALUE**: 모터의 최대 위치 값입니다.
- **BAUDRATE**: 통신 속도를 정의하며, 이 코드에서는 `57600`으로 설정되어 있습니다.
- **PROTOCOL_VERSION**: Dynamixel 모터가 사용하는 프로토콜 버전입니다. 이 코드에서는 `2.0` 버전을 사용합니다.
- **DXL1_ID, DXL2_ID**: 제어할 두 모터의 ID 값입니다. 기본적으로 `1`과 `2`로 설정되어 있습니다.
- **DEVICENAME**: 모터가 연결된 시리얼 포트의 이름입니다.
- **TORQUE_ENABLE**: 토크 활성화를 위한 값(1).
- **TORQUE_DISABLE**: 토크 비활성화를 위한 값(0).
- **DXL_MOVING_STATUS_THRESHOLD**: 모터가 이동 중임을 확인하기 위한 임계값입니다.
- **dxl_goal_position**: 두 모터가 이동할 목표 위치 값을 배열로 정의합니다.

## 코드 실행 흐름

1. **포트 열기**:
    - `portHandler.openPort()`로 지정된 포트를 열어 Dynamixel 모터와의 통신을 시작합니다.
    - 포트 열기에 실패하면 프로그램이 종료됩니다.

2. **보드레이트 설정**:
    - `portHandler.setBaudRate()`로 보드레이트(통신 속도)를 설정합니다. 여기서는 `57600`으로 설정되어 있습니다.

3. **토크 활성화**:
    - `packetHandler.write1ByteTxRx()`를 사용하여 두 개의 모터에 대해 토크를 활성화합니다. 성공 여부는 콘솔에 출력됩니다.

4. **목표 위치 설정 및 현재 위치 확인**:
    - 무한 루프를 통해 사용자가 키 입력을 할 때마다 두 모터의 목표 위치를 설정합니다.
    - `groupSyncRead`를 사용해 두 모터의 현재 위치를 읽고, 목표 위치와 현재 위치를 콘솔에 출력합니다.
    - 두 모터가 목표 위치에 도달하면 다음 목표 위치로 자동으로 전환됩니다.

5. **토크 비활성화**:
    - 모터 사용이 끝나면 `packetHandler.write1ByteTxRx()`로 두 모터의 토크를 비활성화합니다.

6. **포트 닫기**:
    - `portHandler.closePort()`로 포트를 닫고 프로그램을 종료합니다.

## 추가 기능

- **SyncWrite**: 두 모터의 목표 위치를 동기화하여 동시에 설정할 수 있습니다.
- **SyncRead**: 두 모터의 현재 위치를 동기화하여 읽어올 수 있습니다.
- **동기화된 제어**: 두 모터를 동시에 제어하고, 목표 위치와 현재 위치를 비교하여 정확한 제어가 가능합니다.

이 코드는 두 개의 Dynamixel 모터를 동기화하여 제어하는 기본적인 예제로, 더 복잡한 제어 시스템을 위한 기초로 활용될 수 있습니다.
