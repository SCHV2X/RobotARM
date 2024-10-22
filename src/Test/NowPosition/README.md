# Dynamixel 제어 프로그램 설명

이 Python 코드는 **Dynamixel SDK**를 사용하여 Dynamixel 모터의 위치를 알수 있는 코드입니다.

## 주요 변수 및 상수

- **MY_DXL**: 제어할 Dynamixel 모터의 모델을 정의합니다. 이 코드에서는 `X_SERIES`를 사용합니다.
- **ADDR_TORQUE_ENABLE**: 모터의 토크 활성화를 위한 주소입니다.
- **ADDR_GOAL_POSITION**: 목표 위치 설정을 위한 주소입니다.
- **ADDR_PRESENT_POSITION**: 현재 위치를 읽기 위한 주소입니다.
- **DXL_MINIMUM_POSITION_VALUE**: 모터가 이동할 수 있는 최소 위치 값입니다.
- **DXL_MAXIMUM_POSITION_VALUE**: 모터가 이동할 수 있는 최대 위치 값입니다.
- **BAUDRATE**: 통신 속도를 정의합니다. 여기서는 `57600`으로 설정되어 있습니다.
- **PROTOCOL_VERSION**: Dynamixel 모터가 사용하는 프로토콜 버전입니다. 이 코드에서는 `2.0` 버전을 사용합니다.
- **DXL_ID**: 제어할 모터의 ID입니다. 기본값은 `1`로 설정되어 있습니다.
- **DEVICENAME**: 모터가 연결된 시리얼 포트의 이름입니다.
- **TORQUE_ENABLE**: 토크 활성화를 위한 값(0).
- **TORQUE_DISABLE**: 토크 비활성화를 위한 값(1).
- **DXL_MOVING_STATUS_THRESHOLD**: 모터가 움직이는 상태를 확인하기 위한 임계값입니다.
- **dxl_goal_position**: 모터가 이동할 목표 위치 값을 배열로 정의합니다.


## 코드 실행 흐름

1. **포트 열기**:
    - `portHandler.openPort()`로 포트를 열어 Dynamixel 모터와 통신할 준비를 합니다.
    - 포트 열기에 실패하면 프로그램이 종료됩니다.

2. **보드레이트 설정**:
    - `portHandler.setBaudRate()`로 보드레이트를 설정하여 모터와의 통신 속도를 정의합니다.

3. **토크 활성화**:
    - `packetHandler.write1ByteTxRx()`를 사용하여 모터의 토크를 활성화합니다. 이 함수는 모터의 상태를 확인하며, 성공 여부를 출력합니다.

4. **목표 위치 설정 및 현재 위치 확인**:
    - 무한 루프 안에서 사용자가 키를 누르면 `dxl_goal_position`의 목표 위치를 설정하고, 모터의 현재 위치를 읽습니다. 목표 위치와 현재 위치를 출력하여 확인할 수 있습니다.

5. **토크 비활성화**:
    - 모터의 사용이 끝나면 `packetHandler.write1ByteTxRx()`로 토크를 비활성화합니다.

6. **포트 닫기**:
    - `portHandler.closePort()`로 포트를 닫아 프로그램을 종료합니다.

