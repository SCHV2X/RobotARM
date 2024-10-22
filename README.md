# 엘리베이터 로봇팔 제어 프로젝트

## 개요

이 프로젝트는 **다이나믹셀 XH540-V270-R** 모터를 사용하여 엘리베이터를 위/아래로 호출하고, 사용자가 원하는 층을 선택할 수 있도록 제어하는 시스템을 구현하는 것입니다. 로봇팔은 **마스터-슬레이브 듀얼 모드**로 설정된 두 개의 모터를 사용하여 동작하며, 마스터 모터의 동작에 따라 슬레이브 모터가 동일한 힘과 방향으로 움직이도록 설계되었습니다.

## 주요 기능

- 엘리베이터의 위/아래 호출
- 사용자가 원하는 층 선택
- **다이나믹셀 XH540-V270-R** 모터 제어 (마스터-슬레이브 듀얼 모드)

## 사용된 기술

- **다이나믹셀 SDK**: 로봇 모터를 제어하기 위한 SDK. [Dynamixel SDK](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)를 사용하여 모터를 제어합니다.
- **다이나믹셀 XH540-V270-R**: 본 프로젝트에 사용된 주요 모터. 마스터-슬레이브 듀얼 모드로 연결되어 동작합니다. 모터 상세 정보는 [여기](https://www.robotis.com/shop/item.php?it_id=902-0143-000)에서 확인할 수 있습니다.
- **다이나믹셀 위자드**: 모터의 설정 및 테스트를 위한 도구. [Dynamixel Wizard](https://emanual.robotis.com/docs/kr/software/dynamixel/dynamixel_wizard2/)를 사용하여 모터의 초기 설정을 구성하였습니다.

## 프로젝트 설정

### 1. 다이나믹셀 모터 설정
- **마스터-슬레이브 모드**로 두 개의 XH540-V270-R 모터를 연결합니다.
  - **마스터 모터**: 엘리베이터 호출 및 층 선택의 주 제어 모터.
  - **슬레이브 모터**: 마스터 모터의 동작을 따라 동일한 힘과 방향으로 동작.

### 2. 다이나믹셀 SDK 설치
다이나믹셀 SDK는 모터 제어에 사용됩니다. 설치 방법은 아래의 [Dynamixel SDK 설치 가이드](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)를 참고하세요.

### 3. 엘리베이터 제어 로직
엘리베이터 제어는 마스터 모터의 명령에 따라 슬레이브 모터가 동기화되도록 설계됩니다. 사용자가 버튼을 눌러 엘리베이터를 호출하고, 층을 선택하면 로봇팔이 해당 층으로 이동합니다.

## 참고 자료

- [Dynamixel XH540-V270-R 구매 및 상세 정보](https://www.robotis.com/shop/item.php?it_id=902-0143-000)
- [Dynamixel XH540-V270-R e-Manual](https://emanual.robotis.com/docs/kr/dxl/x/xh540-v270/?_gl=1*1x4xhpk*_gcl_au*OTY4NDI3MDQxLjE3MjU0OTQzNjg)
- [Dynamixel SDK 설치 가이드](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)
- [Dynamixel Wizard 사용법](https://emanual.robotis.com/docs/kr/software/dynamixel/dynamixel_wizard2/)
- [Dynamixel Wizard 퀵 가이드](https://www.youtube.com/watch?v=JRRZW_l1V-U)

## 라이센스

본 프로젝트는 [MIT 라이센스](./LICENSE)를 따릅니다.
