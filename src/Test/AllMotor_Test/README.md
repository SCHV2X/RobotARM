# Dynamixel 모터 제어 프로그램

- 이 코드는 Dynamixel 모터를 키보드 입력으로 제어할 수 있는 프로그램입니다. 
- 사용자가 입력하는 숫자에 따라 해당 모터의 특정 동작을 수행합니다.

```
- ESC 키: 프로그램 종료 및 모든 모터를 초기 위치로 이동
- 모터 제어: 1~9 키 입력을 통해 각각의 모터 제어
- 모터 진입: 숫자 키(1~9)로 특정 모터의 제어 모드로 진입
- 이동 제어:
- . (온도/클럭 상위): 각 모터의 목표 위치를 +step씩 증가하여 시계 방향으로 이동합니다.
- / (온도/클럭 하위): 각 모터의 목표 위치를 -step씩 감소하여 반시계 방향으로 이동합니다.
- 각 모터의 범위를 초과하면 최대/최소 위치에 도달했다는 메시지를 출력
```

## 요구 사항

- Python 3.x
- Dynamixel SDK (`dynamixel_sdk`)
- Dynamixel 모터 (예: `X_SERIES`, `MX_SERIES`)
- USB2Dynamixel 또는 U2D2 (통신 장치)
- 통신 장치와 모터가 물리적으로 연결된 상태

## 주요 기능

- Dynamixel 모터 ID 설정 (`DXL1_ID` ~ `DXL9_ID`)
- 각 모터의 속도와 가속도 프로파일 설정
- 각 모터의 위치 범위 지정 및 현재 위치 읽기 기능
- 키보드 입력을 통해 모터의 특정 각도 및 위치 조절
- 드라이브 모드(master-slave 설정) 제어 가능

## 실행 방법

1. 필요한 라이브러리를 설치합니다:
    ```bash
    pip install dynamixel_sdk
    ```

2. 모터와 컨트롤러를 연결하고, `DEVICENAME`을 시스템에 맞게 설정합니다.

3. 스크립트를 실행합니다:
    ```bash
    sudo python AllTestMotor.py
    ```

## 주요 구성 요소

### 1. **상수 및 주소 설정**
   - **ADDR_TORQUE_ENABLE**: 모터 토크 활성화 주소
   - **ADDR_GOAL_POSITION**: 목표 위치 주소
   - **ADDR_PRESENT_POSITION**: 현재 위치 주소
   - **ADDR_PROFILE_VELOCITY / ACCELERATION**: 모터 속도와 가속도 설정 주소
   - **DXL_MINIMUM_POSITION_VALUE_X / DXL_MAXIMUM_POSITION_VALUE_X**: 각 모터의 최소/최대 위치 값

### 2. **주요 함수**
   - `set_profile_velocity_acceleration(velocity, acceleration, ID)`: 특정 모터의 속도와 가속도를 설정합니다.
   - `set_init_position(ID, minPosition)`: 특정 모터를 초기 위치로 설정합니다.
   - `Enable_Torque(T_ENABLE, ID)`: 특정 모터의 토크를 활성화합니다.
   - `Disable_Torque(T_ENABLE, ID)`: 특정 모터의 토크를 비활성화합니다.
   - `durl_mode(ID)`: 특정 모터를 듀얼모드(슬레이브)로 설정합니다.

### 3. **모터 제어 흐름**
   - **포트 및 보드레이트 설정**: 포트를 열고 보드레이트를 설정합니다.
   - **모터 초기화**: 각 모터의 프로파일 속도와 가속도를 설정하고 초기 위치로 이동시킵니다.
   - **키보드 입력에 따른 모터 동작 제어**: 사용자 입력에 따라 모터의 이동 각도를 조정합니다.
   - **위치 피드백**: 모터의 현재 위치를 실시간으로 출력하고, 최대/최소 위치 도달 시 알림을 표시합니다.
   - **토크 비활성화 및 포트 닫기**: 사용이 끝나면 모든 모터의 토크를 비활성화하고 통신 포트를 닫습니다.

## 코드 흐름

1. **포트 열기 및 보드레이트 설정**: 통신 포트를 열고 보드레이트를 설정하여 모터와의 통신을 준비합니다.
2. **프로파일 속도/가속도 설정**: 각 모터의 속도와 가속도를 설정합니다.
3. **모터 초기 위치 설정**: 각 모터의 초기 위치를 설정합니다.
4. **모터 제어**: 
    - 키보드 입력을 통해 각 모터의 위치를 조절할 수 있습니다.
    - 모터의 현재 위치를 출력하며, 각도 범위를 초과할 경우 경고 메시지를 출력합니다.
5. **토크 비활성화 및 포트 닫기**: 모든 모터의 토크를 비활성화하고 통신 포트를 닫습니다.

## 실행 예시
```
포트 열기에 성공했습니다.
보드레이트 변경 성공 Dynamixel 연결 성공
Press any key to continue! (or press ESC to quit!)
모터1에 들어왔습니다.
종료하려면 0을 누르세요.
움직이려면 .와 /으로 움직이세요
```


## 참고 사항

- 시스템 환경에 맞게 `DEVICENAME`을 `/dev/ttyUSB0`, `/dev/tty.usbserial-*` 또는 `COM*`과 같이 설정해야 합니다.
- 사용하려는 모터 ID에 맞게 `DXL1_ID` ~ `DXL9_ID`를 설정하고 키 입력에 맞는 동작을 구성하세요.

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.


