# 로봇팔 제어 프로젝트

## 개요

- 이 프로젝트는 **다이나믹셀 XH540-V270-R** 모터를 사용하여 엘리베이터 제어로 층간 이동에 사용하거나 물건을 집거나, 버튼을 누르는 등의 행동을 제어하는 시스템을 구현하는 것입니다. 
- 로봇팔은 **마스터-슬레이브 듀얼 모드**로 설정된 두 개의 모터 또는 단일 모터를 사용하여 동작하며, 듀얼 모터를 사용하는 경우 마스터 모터의 동작에 따라 슬레이브 모터가 동일한 힘과 방향으로 움직이도록 설계되었습니다.
<br>

## 주요 기능

- 엘리베이터의 위/아래 호출
- 사용자가 원하는 층 선택
- 물건을 집는 행위
- 버튼을 누르는 행위
- **다이나믹셀 XH540-V270-R** 모터 제어 (마스터-슬레이브 듀얼 모드)
<br>

## 사용된 기술

- **다이나믹셀 SDK**: 로봇 모터를 제어하기 위한 SDK. [Dynamixel SDK](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)를 사용하여 모터를 제어합니다.
- **다이나믹셀 XH540-V270-R**: 본 프로젝트에 사용된 주요 모터. 마스터-슬레이브 듀얼 모드로 연결되어 동작합니다. 모터 상세 정보는 [여기](https://www.robotis.com/shop/item.php?it_id=902-0143-000)에서 확인할 수 있습니다.
- **다이나믹셀 위자드**: 모터의 설정 및 테스트를 위한 도구. [Dynamixel Wizard](https://emanual.robotis.com/docs/kr/software/dynamixel/dynamixel_wizard2/)를 사용하여 모터의 초기 설정을 구성하였습니다.
<br>

## 프로젝트 설정

### 1. 다이나믹셀 모터 설정
- 관절 부분의 경우 많은 힘을 내기 위해 **마스터-슬레이브 모드**로 두 개의 XH540-V270-R 모터를 연결합니다.
  - **마스터 모터**: 엘리베이터 호출 및 층 선택 등의 주 제어 모터.
  - **슬레이브 모터**: 마스터 모터의 동작을 따라 동일한 힘과 방향으로 동작.
![image](https://github.com/user-attachments/assets/b010c609-cac6-42af-919b-39d6911f29a2)


### 2. 다이나믹셀 SDK 설치
다이나믹셀 SDK는 모터 제어에 사용됩니다. 설치 방법은 아래의 [Dynamixel SDK 설치 가이드](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)를 참고하세요.

### 3. 엘리베이터 제어 로직
엘리베이터 제어는 마스터 모터의 명령에 따라 슬레이브 모터가 동기화되도록 설계됩니다. 사용자가 버튼을 눌러 엘리베이터를 호출하고, 층을 선택하면 로봇팔이 해당 층으로 이동합니다.
<br>

## 이용 시 주의 사항

- **위자드로 사용 후 제어 문제 발생**: Dynamixel Wizard로 설정 후 모터 제어가 제대로 되지 않을 수 있습니다. 이 경우, **공장 초기화** 후 Python 코드로 제어하는 것이 좋습니다.
- **ID 검색 문제**: 여러 모터를 동기화하여 사용 시, **모터 ID가 검색되지 않을 경우 배선**을 확인하세요. 선이 끊겼을 가능성도 있습니다.
- **Operating Mode 확인**: 여러 모터를 제어할 때, **Operating Mode**가 올바르게 설정되어 있는지 확인하세요. 예를 들어, 속도 제어 모드로 설정한 상태에서 위치 제어를 시도하면 제대로 작동하지 않습니다.

<br>

## 참고 자료

- [Dynamixel XH540-V270-R 구매 및 상세 정보](https://www.robotis.com/shop/item.php?it_id=902-0143-000)
- [Dynamixel XH540-V270-R e-Manual](https://emanual.robotis.com/docs/kr/dxl/x/xh540-v270/?_gl=1*1x4xhpk*_gcl_au*OTY4NDI3MDQxLjE3MjU0OTQzNjg)
- [Dynamixel SDK 설치 가이드](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/)
- [Dynamixel Wizard 사용법](https://emanual.robotis.com/docs/kr/software/dynamixel/dynamixel_wizard2/)
- [Dynamixel Wizard 퀵 가이드](https://www.youtube.com/watch?v=JRRZW_l1V-U)

## 라이센스

본 프로젝트는 [MIT 라이센스](./LICENSE)를 따릅니다.
