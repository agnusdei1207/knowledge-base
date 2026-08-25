---
sidebar:
  order: 67
  label: "067. AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
date: "2026-08-25T10:25:00+09:00"
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

- **AUTOSAR(AUTomotive Open System ARchitecture)**: 글로벌 자동차 제조사(OEM)와 부품사(Tier-1)가 공동 개발한 개방형 자동차 전장 소프트웨어 표준 플랫폼.
- **RTE(Runtime Environment)**: 애플리케이션 소프트웨어 컴포넌트(SWC)와 하부 기본 소프트웨어(BSW) 간의 통신을 중계하는 미들웨어 계층.

</details>

- 정의/개념: 응용, **RTE**, 기본 소프트웨어(BSW), 하드웨어 추상화 계층을 표준화한 개방형 전장 플랫폼 **AUTOSAR**
- 배경/필요성: 제어기별 독자 펌웨어 구조로는 **전장 소프트웨어 재사용 및 공급사 간 통합 불가**

#### 한줄 요약
- 하드웨어와 응용 소프트웨어를 계층적으로 분리하여 전장 부품의 재사용성과 공급망 간 상호운용성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **VFB(Virtual Function Bus)**: 하드웨어 물리 배치와 무관하게 소프트웨어 컴포넌트 간의 가상 통신을 정의하는 추상화 버스.
- **ARXML(AUTOSAR XML)**: 시스템 토폴로지, 통신 매트릭스, 컴포넌트 인터페이스 명세를 기술하는 표준 교환 포맷.

</details>

- 계층 분리로 **SWC(Software Component)**의 칩셋 독립적 재사용성 확보
- 제어용 Classic Platform과 고성능 서비스 지향 Adaptive Platform으로 이원화
- **ARXML** 명세서 기반 모델 주도 개발(MDD) 및 소스 코드 자동 생성 지원

#### 한줄 요약
- VFB 추상화를 통해 하드웨어 종속성을 제거하고 ARXML 표준 명세로 OEM-티어1 간 협업을 정형화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SWC(Software Component)**: 차량의 특정 제어 기능을 구현한 최상위 독립 소프트웨어 모듈.
- **BSW(Basic Software)**: OS, 메모리 관리, 통신 스택, 진단(UDS) 등 공통 필수 서비스를 제공하는 계층.
- **MCAL(Microcontroller Abstraction Layer)**: 특정 반도체 칩의 레지스터를 직접 제어하는 최하위 하드웨어 드라이버 계층.

</details>

```text
[AUTOSAR Classic 계층 구조]
|-- 응용 소프트웨어 컴포넌트 (SWC - 기능별 제어 알고리즘)
|-- 런타임 환경 (RTE - VFB 가상 통신 구현 미들웨어)
|-- 기본 소프트웨어 (BSW)
|   |-- 서비스 계층 (OS·시스템 서비스·통신·메모리·진단 스택)
|   |-- ECU 추상화 계층 (외장 칩 및 온보드 디바이스 추상화)
|   `-- 마이크로컨트롤러 추상화 계층 (MCAL - 칩 레지스터 드라이버)
`-- 마이크로컨트롤러 하드웨어 (MCU)
```

선의 의미: 계층 및 인터페이스 결합 구조

| 구성요소 | 책임 |
|:---|:---|
| 애플리케이션 SWC | 포트(Port)와 인터페이스로 정의된 차량 기능 비즈니스 로직 수행 |
| **RTE** | **VFB** 설계를 실제 하드웨어 배치에 맞춰 자동 생성한 통신 미들웨어 |
| 서비스 계층 | 실시간 OS, 통신 관리자(ComM), 진단(DCM), 메모리 스택(NvM) 제공 |
| ECU 추상화 계층 | 온보드 외장 드라이버를 통합하여 상위에 일관된 I/O 인터페이스 제공 |
| **MCAL** | MCU 내부 주변장치(ADC, PWM, CAN, SPI) 레지스터 직접 제어 |

#### 한줄 요약
- SWC, RTE, BSW(서비스·ECU 추상화·MCAL) 계층으로 명확히 구분되어 하드웨어 교체 시 MCAL만 변경하면 된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Runnable**: 특정 이벤트(주기 타이머, 데이터 수신 등)에 의해 RTE에 의해 트리거되어 실행되는 SWC 내부의 최소 함수 단위.

</details>

```text
시스템 요구사항 및 통신 매트릭스 정의
        │
   ARXML로 SWC 인터페이스 및 신호 매핑 모델링
        │
   타깃 칩 클록·통신 속도·메모리 섹션 구성 (ECU Config)
        │
   코드 생성기가 RTE 및 BSW 소스 코드 자동 생성
        │
   생성 코드가 MCU 메모리 예산(Flash/RAM)을 충족하는가?
   ┌────┴─────┐
아니오          예
   │             │
미사용 모듈     SWC 알고리즘 코드와 링크 후 통합 빌드
최적화 비활성화   │
   │        OS 타이머 틱에 맞춰 Runnable 엔티티 주기 호출
   └────┬────────┘
        │
   CAN 통신 및 제어 루프 정상 실행
```

#### 한줄 요약
- ARXML 모델링 → RTE/BSW 코드 자동 생성 → 메모리 검증 및 빌드 → OS 스케줄러 기반 Runnable 주기 실행 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **AUTOSAR Classic**: OSEK/VDX 기반 정적 실시간 OS와 CAN/LIN 중심의 확정적 제어 플랫폼.
- **AUTOSAR Adaptive**: POSIX OS(Linux/QNX)와 서비스 지향 통신(SOME/IP) 기반의 고성능 자율주행 플랫폼.

</details>

| AUTOSAR 플랫폼 범주 | AUTOSAR Classic | AUTOSAR Adaptive | Non-AUTOSAR 레거시 | ROS 2 / AP-Linux |
|:---|:---|:---|:---|:---|
| 적용 기준 | 제동·조향·엔진 등 실시간 결정론적 ECU | 자율주행·인포테인먼트·도메인 제어기 | 초저가 단일 목적 단순 센서 노드 | 자율주행 로보틱스 연구 및 시제품 |
| 핵심 특징 | 정적 구성과 신호·서비스 기반 ECU 통신 | POSIX 기반 서비스 지향 애플리케이션 | 제품별 최소 전용 구성 | DDS 기반 노드·토픽 통신 |
| 한계 | 동적 서비스와 고성능 애플리케이션에 제약 | 복잡한 배포·서비스 관리와 큰 자원 요구 | 표준 인터페이스·도구 재사용 범위 제한 | 차량 양산 플랫폼 통합·안전 증거 별도 필요 |

#### 한줄 요약
- 딥 임베디드 실시간 제어에는 Classic Platform, 자율주행 및 SDV 중앙 집중형 도메인 제어기에는 Adaptive Platform을 적용한다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **E2E(End-to-End) 보호**: 차량 네트워크 통신 중 데이터 변조, 유실, 순서 바뀜을 감지하기 위해 CRC와 시퀀스 카운터를 부착하는 기능 안전(ISO 26262) 프로토콜.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 툴체인 버전 불일치로 통합 빌드 에러 | ARXML 스키마 및 메타모델 버전 엄격 동기화 | OEM-티어1 간 설정 충돌 및 빌드 오류 방지 |
| BSW 계층 오버헤드로 인한 ROM/RAM 부족 | 미사용 BSW 모듈 비활성화 및 복합 드라이버(CDD) 최적화 | 바이너리 크기 축소 및 마이크로컨트롤러 원가 절감 |
| 차량 네트워크 전송 중 데이터 결함 위험 | **E2E 보호** 프로토콜(CRC+Alive Counter) 적용 | ASIL-D 수준의 데이터 무결성 및 기능 안전 보장 |
| 제어기 OTA 펌웨어 업데이트 실패 위험 | UDS 진단 플래싱 및 A/B 듀얼 뱅크 부트로더 연동 | 소프트웨어 업데이트 실패 시 자동 롤백 보장 |

#### 한줄 요약
- 메타모델 형상 관리, 미사용 BSW 가지치기, E2E 보호 프로토콜, A/B 롤백 메커니즘을 통해 안정성을 확보한다.

## Ⅶ. 결론

- 실시간 결정론적 제어는 **AUTOSAR Classic**, 고성능 SDV 컴퓨팅은 **AUTOSAR Adaptive**를 구축하고, **E2E 안전 프로토콜**을 적용하여 기능 안전(ISO 26262) 달성

#### 한줄 요약
- AUTOSAR는 소프트웨어 중심 자동차(SDV) 전환의 기반 표준이며, Classic과 Adaptive의 상호 보완적 통합이 핵심이다.