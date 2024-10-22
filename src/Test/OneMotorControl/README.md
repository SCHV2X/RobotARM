# Dynamixel 제어 및 프로파일 설정 프로그램 설명

이 Python 코드는 **Dynamixel SDK**를 사용하여 Dynamixel 모터의 속도, 가속도 프로파일을 설정하고, 목표 위치를 지정해 동작시키는 예제입니다. 이 코드는 모터의 목표 위치를 설정하고 현재 위치를 읽으며, 동작 모드 및 드라이브 모드 설정 등의 기능을 포함하고 있습니다.

## 주요 변수 및 상수

- **ADDR_TORQUE_ENABLE**: 모터의 토크를 활성화하기 위한 주소입니다.
- **ADDR_GOAL_POSITION**: 목표 위치를 설정하는 주소입니다.
- **ADDR_PRESENT_POSITION**: 현재 위치를 읽는 주소입니다.
- **ADDR_PROFILE_VELOCITY**: 속도 프로파일을 설정하는 주소입니다.
- **ADDR_PROFILE_ACCELERATION**: 가속도 프로파일을 설정하는 주소입니다.
- **ADDR_OPERATING_MODE**: 동작 모드를 설정하는 주소입니다.
- **ADDR_DRIVE_MODE**: 드라이브 모드를 설정하는 주소입니다.
- **ADDR_HOMING_OFFSET**: 홈 오프셋을 설정하는 주소입니다.
- **DXL_MINIMUM_POSITION_VALUE**: 모터의 최소 위치 값입니다.
- **DXL_MAXIMUM_POSITION_VALUE**: 모터의 최대 위치 값입니다.
- **DXL_REVERSE_MODE_VALUE**: 모터의 시계방향(정방향) 회전을 설정하는 값입니다.
- **DXL_HOMING_OFFSET_VALUE**: 홈 오프셋 설정 값입니다.
- **BAUDRATE**: 통신 속도를 정의하며, 이 코드에서는 `57600`으로 설정되어 있습니다.
- **PROTOCOL_VERSION**: Dynamixel 모터가 사용하는 프로토콜 버전입니다. 이 코드에서는 `2.0` 버전을 사용합니다.
- **DXL_ID**: 제어할 모터의 ID 값입니다. 기본적으로 `1`로 설정되어 있습니다.
- **DEVICENAME**: 모터가 연결된 시리얼 포트의 이름입니다.
- **TORQUE_ENABLE**: 토크를 활성화하기 위한 값입니다.
- **TORQUE_DISABLE**: 토크를 비활성화하기 위한 값입니다.
- **DXL_MOVING_STATUS_THRESHOLD**: 모터의 이동 상태를 확인하는 임계값입니다.

## 코드 실행 흐름

1. **포트 열기**:
    - `portHandler.openPort()`로 지정된 포트를 열어 Dynamixel 모터와의 통신을 시작합니다.
    - 포트를 열지 못할 경우 프로그램이 종료됩니다.

2. **보드레이트 설정**:
    - `portHandler.setBaudRate()`로 보드레이트(통신 속도)를 설정합니다. 여기서는 `57600`으로 설정되어 있습니다.

3. **프로파일 설정**:
    - `set_profile_velocity_acceleration()` 함수를 사용해 모터의 속도와 가속도를 설정합니다.
    - 설정된 값은 각각 `ADDR_PROFILE_VELOCITY`와 `ADDR_PROFILE_ACCELERATION`에 적용됩니다.

4. **동작 및 드라이브 모드 설정**:
    - 모터의 동작 모드는 `ADDR_OPERATING_MODE`에 설정됩니다. 여기서는 위치 제어 모드로 설정되었습니다.
    - `ADDR_DRIVE_MODE`는 모터의 드라이브 모드를 설정하는 데 사용됩니다.

5. **홈 오프셋 설정**:
    - `ADDR_HOMING_OFFSET`을 사용해 홈 오프셋을 설정합니다.

6. **토크 활성화**:
    - `packetHandler.write1ByteTxRx()`를 사용하여 모터의 토크를 활성화합니다. 성공 여부는 콘솔에 출력됩니다.

7. **목표 위치 설정 및 현재 위치 확인**:
    - 사용자가 키를 누르면, 목표 위치가 `ADDR_GOAL_POSITION`에 설정되고, 현재 위치는 `ADDR_PRESENT_POSITION`에서 읽어옵니다.
    - 목표 위치를 설정하고 일정 간격으로 증가시키며, 목표 위치와 현재 위치가 콘솔에 출력됩니다.

8. **토크 비활성화 및 포트 닫기**:
    - 모터 사용이 끝나면 토크를 비활성화하고 `portHandler.closePort()`로 포트를 닫아 프로그램을 종료합니다.

## 추가 기능

- **프로파일 설정**: 속도 및 가속도 프로파일을 설정하여 모터의 움직임을 제어합니다.
- **홈 오프셋 설정**: 홈 오프셋을 설정하여 모터의 기준점을 조정할 수 있습니다.
- **동작 모드 및 드라이브 모드 설정**: 다양한 제어 방식과 드라이브 모드를 설정할 수 있습니다.

이 코드는 속도와 가속도 프로파일을 설정하고, 홈 오프셋 및 동작 모드를 제어하는 기본적인 예제입니다. 이를 활용해 더 복잡한 로봇 제어 시스템을 구현할 수 있습니다.
