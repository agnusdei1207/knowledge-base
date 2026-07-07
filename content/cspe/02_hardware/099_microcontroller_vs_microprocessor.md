---
title: "마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)"
date: "2026-07-06"
tags:
  - "cspe-hardware"
weight: 99
---

# 마이크로컨트롤러 vs 마이크로프로세서 (Microcontroller vs Microprocessor)

## 미리 알고가기

- MCU(Microcontroller Unit): CPU(Central Processing Unit), 메모리, 주변장치를 단일 칩에 통합한 제어용 반도체임
- MPU(Microprocessor Unit): CPU 연산 기능을 중심으로 외부 메모리와 주변장치를 연결해 쓰는 프로세서임
- 주변장치: GPIO(General-Purpose Input/Output), ADC(Analog-to-Digital Converter), PWM(Pulse Width Modulation), UART(Universal Asynchronous Receiver/Transmitter), timer처럼 제어 기능을 담당하는 블록임
- RTOS(Real-Time Operating System): 제한 시간 안에 태스크를 처리하도록 설계된 실시간 운영체제임
- 실시간성: 정해진 시간 안에 입력을 처리하고 출력을 내야 하는 성질임

## Ⅰ. 개요

- **정의/개념**: 마이크로컨트롤러는 제어 업무에 필요한 CPU·메모리·주변장치를 단일 칩에 통합한 장치이고, 마이크로프로세서는 고성능 연산 CPU를 중심으로 외부 메모리·I/O(Input/Output)와 결합해 시스템을 구성하는 장치임. 임베디드 시스템에서 비용, 전력, 성능, 실시간성 기준으로 선택함.
- **배경/필요성**: 센서 제어, 모터 구동, 가전처럼 단순 제어는 낮은 전력과 즉시 응답이 중요하고, 게이트웨이·멀티미디어·범용 OS(Operating System) 업무는 높은 연산 성능과 메모리 확장이 중요함. MCU와 MPU를 구분해야 시스템 비용과 복잡도를 줄일 수 있음.
- **비유**: MCU는 주방과 도구가 포함된 작은 작업실이고, MPU는 큰 공장의 핵심 엔진에 주변 설비를 붙여 운영하는 방식임.

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 임베디드 하드웨어 선택 기준 | 집적도, 성능, 전력, OS, 실시간성, 비용 | 성능 우열만으로 비교 |

> 요약: MCU와 MPU는 고저 성능의 문제가 아니라 제어 통합형과 연산 확장형의 선택 문제임.

## Ⅱ. 특징 및 비교

| 판단 기준 | 마이크로컨트롤러 | 마이크로프로세서 |
|:---|:---|:---|
| 집적 구조 | CPU, SRAM(Static Random-Access Memory)/Flash, 주변장치 내장 | CPU 중심, 외부 DRAM(Dynamic Random-Access Memory)/Flash/I/O 필요 |
| 성능·전력 | 낮은 전력과 예측 가능한 응답 | 높은 연산 성능과 풍부한 메모리 |
| 소프트웨어 | bare-metal 또는 RTOS 중심 | Linux, Android, 범용 OS 가능 |
| 적용 업무 | 센서, 모터, 계측, 저전력 제어 | UI(User Interface), 네트워크, AI(Artificial Intelligence), 멀티미디어 처리 |

> 요약: MCU는 제어성과 비용, MPU는 성능과 확장성을 기준으로 선택함.

## Ⅲ. 구성요소/구조

```text
+-------------+      +-------------+      +-------------+
| MCU chip    | ---> | CPU core    | ---> | GPIO/ADC    |
+-------------+      +-------------+      +-------------+
       |                    |
       v                    v
+-------------+      +-------------+      +-------------+
| Flash/SRAM  |      | Timer/PWM   |      | Control out |
+-------------+      +-------------+      +-------------+

+-------------+      +-------------+      +-------------+
| MPU core    | ---> | DRAM/Flash  | ---> | External I/O|
+-------------+      +-------------+      +-------------+
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| CPU 코어 | 명령 실행과 제어 로직을 수행하는 공통 핵심임 | 작업자 |
| 내장/외부 메모리 | MCU는 내장 메모리, MPU는 외부 DRAM과 저장장치를 주로 사용함 | 책상 서랍과 외부 창고 |
| 주변장치 | 센서·모터·통신 인터페이스와 직접 연결되는 제어 블록임 | 작업 도구 |
| 소프트웨어 스택 | bare-metal, RTOS, Linux 등 시스템 기능과 복잡도를 결정함 | 운영 규칙 |

> 요약: MCU와 MPU의 구조 차이는 CPU보다 메모리·주변장치·소프트웨어 스택의 통합 수준에서 드러남.

### 원리/흐름도

```text
+----------+      +----------+      +----------+      +----------+
| Req def  | ---> | Select   | ---> | Board    | ---> | Verify   |
+----------+      +----------+      +----------+      +----------+
```

1. **요구 정의** — 처리량, 응답시간, 전력, 인터페이스, BOM(Bill of Materials) 비용, OS 필요성을 정리함
2. **후보 선정** — 단순 제어와 저전력은 MCU, 고성능·고메모리는 MPU를 우선 검토함
3. **보드 설계** — 전원, 클럭, 메모리, 주변장치, 디버깅 인터페이스를 구성함
4. **검증 운영** — 실시간 응답, 발열, 소비전력, 펌웨어 업데이트, 생산 테스트를 검증함

> 요약: MCU/MPU 선택은 요구 지표를 하드웨어 구조와 소프트웨어 복잡도에 매핑하는 과정임.

## Ⅳ. 문제점 및 개선방안

- **P1 과소·과대 선정**: MCU로 복잡한 UI와 네트워크를 처리하거나 MPU를 단순 센서 제어에 쓰면 비용과 품질 문제가 생김
- **P1 대응**: workload profile과 BOM target을 기준으로 MCU, MPU, hybrid SoC(System on Chip) 후보를 정량 비교함 (확인: cost-performance fit)
- **P2 실시간성 저하**: MPU와 범용 OS는 인터럽트 지연과 스케줄링 변동으로 hard real-time 제어가 어려울 수 있음
- **P2 대응**: real-time 요구는 RTOS MCU, MPU+real-time core, 실시간 Linux 커널 옵션 조합으로 분리 설계함 (확인: worst-case latency)
- **P3 보드 복잡도 증가**: MPU는 외부 DRAM, PMIC(Power Management Integrated Circuit), 고속 배선이 필요해 설계·검증 비용이 커짐
- **P3 대응**: reference design, SI(Signal Integrity)/PI(Power Integrity) 검증, production test point를 초기 설계에 포함함 (확인: board bring-up defect rate)

> 요약: 선택 리스크는 요구 분석과 실시간 분리, 보드 검증 표준화로 낮출 수 있음.

## Ⅴ. 실무 적용 사례

| 적용 영역 | 적용 방식 | 확인 지표 |
|:---|:---|:---|
| 배터리 센서 노드 | 저전력 MCU와 RTOS(Real-Time Operating System)를 선택해 sleep current, 인터럽트 지연, BOM 비용을 최적화함 | sleep current, worst-case latency, BOM cost |
| 산업용 게이트웨이 | Linux 기반 MPU로 네트워크, UI, 보안 업데이트를 처리하고 실시간 제어는 별도 MCU에 분리함 | update success rate, control latency, board defect rate |
| 제품군 플랫폼화 | MCU/MPU reference design과 펌웨어 SDK를 표준화해 파생 제품의 인증·검증 비용을 낮춤 | reuse rate, certification effort, bring-up time |

> 요약: 실무에서는 최고 성능보다 실시간성, 전력, 보드 복잡도, 수명주기 비용으로 MCU와 MPU를 선택해야 함.

## Ⅵ. 결론

- **발전 방향**: MCU에도 AI(Artificial Intelligence) accelerator, 보안 enclave, 무선 통신이 통합되고 MPU는 저전력 SoC로 확장되며 경계가 일부 흐려짐
- **기술사적 판단**: 최종 선택은 최고 성능보다 수명주기 비용, 전력 예산, 소프트웨어 유지보수, 공급망 안정성을 기준으로 해야 함
- **기술사 제언**: 제품군별 표준 MCU/MPU 플랫폼을 정해 펌웨어 재사용성과 인증 비용을 관리해야 함
