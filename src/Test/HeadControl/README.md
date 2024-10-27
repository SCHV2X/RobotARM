# Dynamixel 모터 제어 프로그램

이 Python 스크립트는 **Dynamixel SDK**를 사용하여 여러 Dynamixel 모터를 제어하는 방법을 보여줍니다. 이 프로그램은 모터의 위치를 설정하고 현재 위치를 읽어오는 기능을 포함하고 있으며, `X_SERIES` 및 `MX_SERIES` 모델을 지원합니다.

## 요구 사항

- Python 3.x
- Dynamixel SDK (`dynamixel_sdk`)
- Dynamixel 모터 (예: `X_SERIES`, `MX_SERIES`)
- USB2Dynamixel 또는 U2D2 (통신 장치)
- 적절한 하드웨어 설정 (모터를 컨트롤러에 연결)

## 주요 기능

- 여러 Dynamixel 모터(`DXL1_ID`, `DXL2_ID`) 제어
- 모터의 프로파일 속도 및 가속도 설정
- 모터의 현재 위치 읽기 및 출력
- 모터 토크 활성화 및 비활성화
- 키보드 입력에 따라 여러 동작 수행

## 실행 방법

1. 필요한 라이브러리를 설치합니다:
    ```bash
    pip install dynamixel_sdk
    ```

2. Dynamixel 모터를 컨트롤러에 연결하고, 올바른 포트(`DEVICENAME`)를 설정합니다.

3. 스크립트를 실행합니다:
    ```bash
    python motor_control.py
    ```

## 주요 구성 요소

### 1. **상수 및 주소**
   - **MY_DXL**: 모터 시리즈를 정의 (`X_SERIES` 등).
   - **ADDR_TORQUE_ENABLE**: 모터 토크 활성화 주소.
   - **ADDR_GOAL_POSITION**: 목표 위치 설정 주소.
   - **ADDR_PRESENT_POSITION**: 현재 위치 읽기 주소.
   - **ADDR_PROFILE_VELOCITY / ACCELERATION**: 모터 속도와 가속도 설정 주소.
   - **DXL_MINIMUM_POSITION_VALUE / DXL_MAXIMUM_POSITION_VALUE**: 모터 이동 범위 설정.
   - **DXL_MOVING_STATUS_THRESHOLD**: 모터가 이동 중인지 확인하는 임계값.

### 2. **함수**
   - `set_profile_velocity_acceleration(velocity, acceleration)`: 주어진 모터의 속도와 가속도를 설정합니다.
   - `getch()`: 플랫폼 독립적인 방식으로 키보드 입력을 받습니다.
   
### 3. **모터 제어 흐름**
   - **포트 및 보드레이트 설정**: 통신 포트를 열고, 보드레이트를 설정하여 모터와의 통신을 준비합니다.
   - **토크 제어**: 모터의 토크를 활성화하거나 비활성화합니다.
   - **위치 제어**: 모터의 목표 위치를 설정하고, 현재 위치를 읽습니다.
   - **키 입력에 따른 모터 동작**: 키보드 입력에 따라 모터의 회전 방향, 위치 조정 등을 수행합니다.
   - **위치 피드백**: 목표 위치와 현재 위치를 실시간으로 모니터링하고 출력합니다.

## 코드 흐름

1. **포트 열기 및 보드레이트 설정**: 통신 포트를 열고, 모터와의 통신을 위한 보드레이트를 설정합니다.
2. **프로파일 속도/가속도 설정**: 각 모터의 속도와 가속도를 설정합니다.
3. **모터 제어**: 
    - 현재 위치가 목표 위치에 도달할 때까지 모니터링합니다.
4. **토크 비활성화 및 포트 닫기**: 모터의 사용이 끝나면 토크를 비활성화하고 통신 포트를 닫습니다.

## 실행 예시
```
포트 열기 성공 보드레이트 변경 성공
Dynamixel#1 연결 성공
Dynamixel#2 연결 성공
아무 키나 누르면 계속 진행! (ESC를 누르면 종료)
[ID:001] GoalPos:000 PresPos:005 [ID:002] GoalPos:000 PresPos:005
[ID:001] GoalPos:500 PresPos:495 [ID:002] GoalPos:500 PresPos:495 ...
```


## 참고 사항

- 운영 체제에 맞는 `DEVICENAME` (예: `/dev/ttyUSB0`, `/dev/tty.usbserial-*`, `COM*`)을 설정해야 합니다.
- 사용 중인 모터의 ID에 맞게 `DXL1_ID`, `DXL2_ID`를 조정해야 합니다.
- 프로젝트 요구 사항에 맞게 모터의 프로파일 가속도 및 속도를 조정할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.

---

이 코드는 여러 Dynamixel 모터를 제어하는 기본적인 기능을 제공하며, 로봇 시스템의 더 복잡한 제어로 확장할 수 있습니다.
