# Dynamixel 모터 제어 프로그램 (마스터-슬레이브 설정)

이 Python 스크립트는 **Dynamixel SDK**를 사용하여 여러 Dynamixel 모터를 제어하는 방법을 보여줍니다. 이 프로그램은 1번 모터를 마스터, 2번 모터를 마스터로 설정하고 3번 모터를 슬레이브로 설정하여 마스터의 PWM에 따라 슬레이브가 동일하게 동작하도록 구성되어 있습니다.

## 요구 사항

- Python 3.x
- Dynamixel SDK (`dynamixel_sdk`)
- Dynamixel 모터 (예: `X_SERIES`, `MX_SERIES`)
- USB2Dynamixel 또는 U2D2 (통신 장치)
- 적절한 하드웨어 설정 (모터를 컨트롤러에 연결)

## 주요 기능

- 여러 Dynamixel 모터(`DXL1_ID`, `DXL2_ID`, `DXL3_ID`) 제어
- 마스터-슬레이브 설정: 1번과 2번 모터는 마스터, 3번 모터는 슬레이브로 설정
- 모터의 프로파일 속도 및 가속도 설정
- 모터의 현재 위치 읽기 및 출력
- 모터 토크 활성화 및 비활성화
- SyncWrite와 SyncRead를 사용하여 여러 모터와 효율적으로 통신

## 실행 방법

1. 필요한 라이브러리를 설치합니다:
    ```bash
    pip install dynamixel_sdk
    ```

2. Dynamixel 모터를 컨트롤러에 연결하고, 올바른 포트(`DEVICENAME`)를 설정합니다.

3. 스크립트를 실행합니다:
    ```bash
    python dynamixel_control.py
    ```

## 주요 구성 요소

### 1. **상수 및 주소**
   - **MY_DXL**: 제어할 모터 시리즈 (`X_SERIES` 등).
   - **ADDR_TORQUE_ENABLE**: 모터 토크 활성화 주소.
   - **ADDR_GOAL_POSITION**: 목표 위치 설정 주소.
   - **ADDR_PRESENT_POSITION**: 현재 위치 읽기 주소.
   - **ADDR_DRIVE_MODE**: 드라이브 모드 설정 주소.
   - **ADDR_OPERATING_MODE**: 작동 모드 설정 주소.
   - **DXL_MINIMUM_POSITION_VALUE / DXL_MAXIMUM_POSITION_VALUE**: 모터 이동 범위 설정.
   - **DXL_MOVING_STATUS_THRESHOLD**: 모터가 이동 중인지 확인하는 임계값.

### 2. **함수**
   - `getch()`: 플랫폼 독립적인 방식으로 키보드 입력을 받습니다.
   - `set_profile_velocity_acceleration(velocity, acceleration, dxl_id)`: 모터의 속도와 가속도를 설정합니다.

### 3. **모터 제어 흐름**
   - **포트 및 보드레이트 설정**: 통신 포트를 열고, 보드레이트를 설정하여 모터와의 통신을 준비합니다.
   - **토크 활성화**: 모터의 토크를 활성화하여 제어가 가능하도록 설정합니다.
   - **드라이브 모드 설정**: 마스터-슬레이브 구성을 설정하고 각 모터의 회전 방향을 지정합니다.
   - **위치 제어**: SyncWrite를 사용하여 목표 위치를 설정하고, SyncRead를 사용하여 현재 위치를 읽습니다.
   - **위치 피드백**: 목표 위치와 현재 위치를 실시간으로 모니터링하며 출력합니다.

## 코드 흐름

1. **포트 열기 및 보드레이트 설정**: 통신 포트를 열고, 보드레이트를 설정하여 모터와 통신할 준비를 마칩니다.
2. **드라이브 모드 설정**: 2번 모터를 마스터로 설정하고, 3번 모터를 슬레이브로 설정하여 동기화된 동작을 구현합니다.
3. **모터 제어**: 
    - SyncWrite를 통해 각 모터의 목표 위치를 설정하고, SyncRead를 사용하여 현재 위치를 읽습니다.
    - 목표 위치에 도달할 때까지 현재 위치를 모니터링합니다.
4. **토크 비활성화 및 포트 닫기**: 작업이 완료되면 토크를 비활성화하고 통신 포트를 닫아 프로그램을 종료합니다.

## 실행 예시

```
포트 열기 성공 보드레이트 변경 성공
Dynamixel#1 연결 성공 Dynamixel#2 연결 성공 Dynamixel#3 연결 성공
아무 키나 누르면 계속 진행! (ESC를 누르면 종료)
[ID:001] GoalPos:000 PresPos:005 [ID:002] GoalPos:000 PresPos:005 [ID:003] GoalPos:000 PresPos:005 
```


## 참고 사항

- 운영 체제에 맞는 `DEVICENAME` (예: `/dev/ttyUSB0`, `/dev/tty.usbserial-*`, `COM*`)을 설정해야 합니다.
- 모터 ID (`DXL1_ID`, `DXL2_ID`, `DXL3_ID`)를 맞춰야 합니다.
- 필요에 따라 모터의 프로파일 속도 및 가속도 값을 조정할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.

---

이 코드는 마스터-슬레이브 구조의 Dynamixel 모터 제어 기본 기능을 제공하며, 로봇 시스템의 더 복잡한 제어로 확장할 수 있습니다.
