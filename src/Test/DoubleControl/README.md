# SyncRead와 SyncWrite를 이용한 DYNAMIXEL 제어 예제

이 코드는 ROBOTIS의 DYNAMIXEL 모터를 SyncRead와 SyncWrite 방식으로 제어하는 예제입니다. 이 코드는 Protocol 2.0을 지원하는 DYNAMIXEL 시리즈(X, P, PRO, MX 등)에 맞춰 설계되었으며, 두 개의 DYNAMIXEL 모터의 목표 위치를 설정하고 현재 위치를 동기화하여 읽을 수 있습니다.

## 주요 기능

- **SyncWrite**: 두 개의 DYNAMIXEL 모터에 동기화된 목표 위치 명령을 전송하여 동시에 제어할 수 있습니다.
- **SyncRead**: 두 개의 DYNAMIXEL 모터에서 동기화된 현재 위치 정보를 읽어옵니다.
- **토크 제어**: 각 모터의 토크를 활성화하거나 비활성화할 수 있습니다.
- **목표 위치와 현재 위치 확인**: 모터가 설정된 목표 위치에 도달할 때까지 현재 위치를 확인하며, 목표 위치에 도달하면 다음 목표 위치로 전환됩니다.

## 사용 방법

1. DYNAMIXEL 모터의 모델을 선택하고, 제어할 모터의 ID와 포트를 설정합니다.
2. SyncWrite를 이용하여 두 모터의 목표 위치를 설정하고, 동시에 동작시킬 수 있습니다.
3. SyncRead를 이용하여 두 모터의 현재 위치를 읽어옵니다.
4. 코드는 목표 위치에 도달하면 자동으로 다음 위치로 전환됩니다.

## 환경 설정

- **DYNAMIXEL SDK**: 이 코드는 DYNAMIXEL SDK 라이브러리를 사용합니다.
- **포트 설정**: 실제 포트 번호를 사용자의 시스템 환경에 맞게 수정해야 합니다.
  - Windows: `COM*`
  - Linux: `/dev/ttyUSB*`
  - Mac: `/dev/tty.usbserial-*`

## 실행 예시

1. 두 DYNAMIXEL 모터를 연결하고, 포트와 통신 속도를 설정합니다.
2. 코드를 실행하면 각 모터가 목표 위치로 이동하고, 현재 위치가 출력됩니다.
3. 목표 위치와 현재 위치 간 차이가 적어지면 모터는 새로운 목표 위치로 전환됩니다.

이 코드는 DYNAMIXEL 모터의 동기화 제어와 상태 확인에 유용한 예제입니다. 자세한 내용은 각 모터의 eManual을 참조하세요.

## 참고 링크

- [DYNAMIXEL eManual](https://emanual.robotis.com/docs/ko/)
- [DYNAMIXEL SDK GitHub](https://github.com/ROBOTIS-GIT/DynamixelSDK)
