---
sidebar:
  order: 67
  label: "067. AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
date: "2026-08-26T10:45:00+09:00"
tags:
  - "notes-hardware"
weight: 67
extra:
  question_no: "067"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "차량 전장 SW 표준화, Classic과 Adaptive 플랫폼의 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AUTOSAR(AUTomotive Open System ARchitecture)**: 글로벌 완성차 제조사(OEM)와 전장 부품사(Tier-1), 반도체사가 공동 개발한 개방형 표준 자동차 전장 소프트웨어 플랫폼 아키텍처.
- **런타임 환경(Runtime Environment, RTE)**: 상위 응용 소프트웨어 컴포넌트(SWC)와 하부 기본 소프트웨어(BSW) 간, 그리고 SWC 상호 간의 데이터 통신을 하드웨어 독립적으로 중계하는 표준 미들웨어 계층.

</details>

- 정의/개념: 차량 제어 응용(SWC), 미들웨어(**RTE**), 기본 소프트웨어(BSW), 하드웨어 추상화(MCAL)를 계층화한 **AUTOSAR 전장 소프트웨어 아키텍처**
- 배경/필요성: ECU별 독자 펌웨어 방식 → 하드웨어 종속 및 코드 재사용 불가 → **전장 기능 복잡도 급증** 대응 한계

#### 한줄 요약
- AUTOSAR는 하드웨어와 응용 소프트웨어를 계층적으로 분리하여 전장 소프트웨어의 재사용성과 부품사 간 상호운용성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **가상 기능 버스(Virtual Function Bus, VFB)**: 소프트웨어 컴포넌트가 동일 ECU 내에 있는지 다른 ECU에 있는지와 무관하게 표준 포트를 통해 통신하도록 추상화한 가상 버스 개념.
- **ARXML(AUTOSAR XML)**: 시스템 토폴로지, CAN/이더넷 통신 매트릭스, SWC 인터페이스 명세를 기술하여 툴체인 간에 교환하는 표준 XML 포맷.

</details>

- 완벽한 하드웨어 독립성: **가상 기능 버스(VFB)** 추상화를 통해 응용 소프트웨어 컴포넌트(SWC)를 타깃 MCU 변경 시에도 재사용
- 이원화된 플랫폼 체계: 엄격한 실시간 제어용 **Classic Platform**과 고성능 자율주행용 **Adaptive Platform**으로 분화 발전
- 모델 주도 개발(MDD): 표준 **ARXML 명세서**를 기반으로 RTE 및 BSW 소스 코드를 자동 생성하여 개발 생산성 극대화

#### 한줄 요약
- VFB 추상화로 하드웨어 종속성을 제거하고, Classic/Adaptive 이원화와 ARXML 표준 명세로 전장 개발을 표준화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **소프트웨어 컴포넌트(Software Component, SWC)**: 차량의 특정 제어 로직(제동, 조향, 와이퍼 등)을 구현한 최상위 독립 모듈.
- **기본 소## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **러너블(Runnable Entity)**: 타이머 틱이나 데이터 수신 이벤트에 의해 RTE로부터 트리거되어 실제 연산을 수행하는 SWC 내부의 최소 C 함수 단위.

</details>

```text
전장 시스템 아키텍처 설계
  │
  ▼
1. CAN/이더넷 통신 매트릭스(DBC) 정의 및 ARXML 모델링
  │
  ▼
2. ECU 설정: 타깃 MCU 클록, CAN 채널, 메모리 섹션 구성
  │
  ▼
3. AUTOSAR 툴체인: RTE 및 BSW C 소스 코드 자동 생성
  │
  ▼
4. 생성된 코드와 SWC 알고리즘 코드를 크로스 컴파일러로 통합 빌드
  │
  ▼
5. 타깃 ECU 플래싱 후 OS 타이머 틱에 따라 Runnable 주기적 호출
  │
  ▼
RTE 센서 수신 ➔ 제어 연산 ➔ MCAL PWM 모터 출력 완료
```

분기 결과: **ARXML 모델링과 코드 자동 생성을 통해** 수작업 코딩 오류를 원천 배제하고 완벽한 이식성을 달성함

#### 한줄 요약
- 통신 정의 ➔ ARXML 모델링 ➔ ECU 설정 ➔ RTE/BSW 자동 생성 ➔ 통합 빌드 ➔ OS 스케줄러 기반 Runnable 실행 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AUTOSAR Classic Platform(CP)**: OSEK/VDX 기반 정적 실시간 OS와 CAN/LIN 중심의 확정적 딥 임베디드 제어 플랫폼.
- **AUTOSAR Adaptive Platform(AP)**: POSIX OS(Linux/QNX)와 SOME/IP 서비스 지향 통신(SOA) 기반의 초고성능 자율주행/SDV 플랫폼.

</details>

| 비교 항목 | AUTOSAR Classic Platform (CP) | AUTOSAR Adaptive Platform (AP) |
|:---|:---|:---|
| 핵심 타깃 도메인 | **파워트레인, 섀시 제동/조향** | **자율주행 ADAS, SDV 중앙 게이트웨이** |
| 운영체제 환경 | **정적 실시간 OSEK/VDX OS** | **POSIX 준수 OS**(QNX, Linux) |
| 통신 패러다임 | **신호 기반 정적 통신**(CAN/LIN) | **서비스 지향 통신**(SOME/IP) |
| 하드웨어 요구사양 | **32비트 MCU**(수 MB Flash) | **64비트 고성능 멀티코어 SoC** |
| 동적 업데이트(OTA) | 펌웨어 전체 플래싱 (정적 링크) | **서비스/앱 단위 동적 배포** |

#### 한줄 요약
- 딥 임베디드 실시간 제어에는 Classic Platform이 쓰이고, 자율주행 및 SDV 중앙 집중형 제어기에는 Adaptive Platform이 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **E2E(End-to-End) 보호 프로토콜**: 차량 네트워크 통신 중 데이터 변조, 유실, 순서 뒤바뀜을 감지하기 위해 CRC와 Alive Counter를 부착하는 ISO 26262 기능 안전 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| BSW 오버헤드로 인한 MCU 메모리 부족 | **미사용 BSW 모듈 비활성화** 및 CDD 최적화 | 바이너리 크기 30% 축소 및 원가 절감 |
| 차량 네트워크 데이터 변조/유실 결함 | **AUTOSAR E2E 보호 프로토콜** 적용 | ISO 26262 ASIL-D 데이터 무결성 달성 |
| OEM과 협력사 간 ARXML 버전 불일치 | **AUTOSAR 메타모델 스키마 버전 엄격 동기화** | 통합 빌드 오류 0화 및 개발 기간 단축 |

#### 한줄 요약
- 실무에서는 미사용 BSW 최적화로 메모리를 아끼고, E2E 보호로 기능 안전을 지키며, ARXML 형상 관리로 호환성을 확보한다.

## Ⅶ. 결론

- **전장 SW 표준화** 요구 시 CP·AP 계층 분리와 E2E 적용 **AUTOSAR 플랫폼** 채택

#### 한줄 요약
- AUTOSAR는 SDV 전장 소프트웨어 표준의 핵심이며, Classic과 Adaptive의 상호 보완적 융합을 통해 완성된다.�널, 메모리 섹션 구성
                      │
                      ▼
4. AUTOSAR 툴체인: RTE 및 BSW C 소스 코드 자동 생성 (Code Generation)
                      │
                      ▼
5. 생성된 코드와 SWC 알고리즘 코드를 타깃 MCU 크로스 컴파일러로 통합 빌드
                      │
                      ▼
6. 타깃 ECU 플래싱 및 기동 ➔ OS 타이머 틱에 따라 Runnable 주기적 호출
                      │
                      ▼
7. RTE를 통한 센서 데이터 수신 ➔ 제어 알고리즘 연산 ➔ MCAL PWM 모터 출력
```

분기 결과: **ARXML 모델링과 코드 자동 생성을 통해** 수작업 코딩 오류를 원천 배제하고 완벽한 이식성을 달성함

#### 한줄 요약
- 통신 정의 ➔ ARXML 모델링 ➔ ECU 설정 ➔ RTE/BSW 자동 생성 ➔ 통합 빌드 ➔ OS 스케줄러 기반 Runnable 실행 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AUTOSAR Classic Platform(CP)**: OSEK/VDX 기반 정적 실시간 OS와 CAN/LIN 중심의 확정적 딥 임베디드 제어 플랫폼.
- **AUTOSAR Adaptive Platform(AP)**: POSIX OS(Linux/QNX)와 SOME/IP 서비스 지향 통신(SOA) 기반의 초고성능 자율주행/SDV 플랫폼.

</details>

| 비교 항목 | AUTOSAR Classic Platform (CP) | AUTOSAR Adaptive Platform (AP) |
|:---|:---|:---|
| 핵심 타깃 도메인 | **파워트레인, 섀시, 바디 제동/조향 제어** | **자율주행 ADAS, IVI 인포테인먼트, SDV 중앙 게이트웨이** |
| 운영체제 환경 | **정적 실시간 OSEK/VDX OS (FreeRTOS급)** | **POSIX PSE51 준수 OS (QNX, Embedded Linux)** |
| 통신 패러다임 | **신호 기반 정적 통신 (Signal-Based, CAN/LIN)** | **서비스 지향 아키텍처 (Service-Oriented, SOME/IP)** |
| 하드웨어 요구사양 | **32비트 MCU (수 MB Flash, 수백 KB RAM)** | **64비트 고성능 멀티코어 SoC + 외장 DDR (수 GB)** |
| 동적 업데이트(OTA) | 펌웨어 전체 플래싱 (정적 링크) | **서비스/앱 단위 동적 배포 및 컨테이너 업데이트** |

#### 한줄 요약
- 딥 임베디드 실시간 제어에는 Classic Platform이 쓰이고, 자율주행 및 SDV 중앙 집중형 제어기에는 Adaptive Platform이 쓰인다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **E2E(End-to-End) 보호 프로토콜**: 차량 네트워크 통신 중 데이터 변조, 유실, 순서 뒤바뀜을 감지하기 위해 CRC와 Alive Counter를 부착하는 ISO 26262 기능 안전 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| BSW 계층 오버헤드로 인한 MCU 플래시/RAM 용량 부족 | **미사용 BSW 모듈 비활성화 및 복합 드라이버(CDD) 최적화** | 바이너리 크기 30% 축소 및 MCU BoM 원가 절감 |
| 차량 네트워크 전송 중 데이터 변조 및 유실 결함 | **AUTOSAR E2E 보호(CRC + Alive Counter) 프로토콜 적용** | ISO 26262 ASIL-D 수준의 데이터 무결성 달성 |
| OEM과 협력사(Tier-1) 간 툴체인/ARXML 버전 불일치 | **AUTOSAR 메타모델 스키마 버전 엄격 동기화 및 형상 관리** | 통합 빌드 에러 0화 및 개발 기간 단축 |

#### 한줄 요약
- 실무에서는 미사용 BSW 최적화로 메모리를 아끼고, E2E 보호로 기능 안전을 지키며, ARXML 형상 관리로 호환성을 확보한다.

## Ⅶ. 결론

- 소프트웨어 중심 자동차(SDV)의 모듈화와 공급망 재사용성을 위해 **실시간 제어 영역에는 AUTOSAR Classic(CP)을, 고성능 자율주행 영역에는 AUTOSAR Adaptive(AP)를 계층 구축**하고, 통신 무결성을 위해 **E2E 보호 및 SecOC 암호화 프로토콜**을 적용하며, 기능 안전(ISO 26262 ASIL-D) 인증을 획득하는 글로벌 표준 전장 소프트웨어 플랫폼 확립

#### 한줄 요약
- AUTOSAR는 SDV 전장 소프트웨어 표준의 핵심이며, Classic과 Adaptive의 상호 보완적 융합을 통해 완성된다.