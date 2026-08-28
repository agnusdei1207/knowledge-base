---
sidebar:
  order: 67
  label: "067. AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "AUTOSAR 전장 소프트웨어 구조 (AUTOSAR)"
date: "2026-08-26T12:45:17+09:00"
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
- 배경/필요성: ECU마다 독자 펌웨어를 쓰면 응용이 특정 칩에 묶여 **전장 기능 복잡도 급증**에 맞춰 기능을 늘릴 때마다 이식 비용을 다시 치르므로, RTE를 사이에 두어 응용과 기본 소프트웨어를 분리하고 MCAL로 칩 차이를 흡수하는 표준 계층의 필요

#### 한줄 요약
- AUTOSAR는 하드웨어와 응용 소프트웨어를 계층적으로 분리하여 전장 소프트웨어의 재사용성과 부품사 간 상호운용성을 극대화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **가상 기능 버스(Virtual Function Bus, VFB)**: 소프트웨어 컴포넌트가 동일 ECU 내에 있는지 다른 ECU에 있는지와 무관하게 표준 포트를 통해 통신하도록 추상화한 가상 버스 개념.
- **ARXML(AUTOSAR XML)**: 시스템 토폴로지, CAN/이더넷 통신 매트릭스, SWC 인터페이스 명세를 기술하여 툴체인 간에 교환하는 표준 XML 포맷.

</details>

- 하드웨어 종속성 완화: **가상 기능 버스(VFB)**로 SWC 통신을 추상화
- 이원화된 플랫폼 체계: 엄격한 실시간 제어용 **Classic Platform**과 고성능 자율주행용 **Adaptive Platform**으로 분화 발전
- 모델 주도 개발(MDD): 표준 **ARXML 명세서**를 기반으로 RTE 및 BSW 소스 코드를 자동 생성하여 개발 생산성 극대화

#### 한줄 요약
- VFB 추상화로 하드웨어 종속성을 제거하고, Classic/Adaptive 이원화와 ARXML 표준 명세로 전장 개발을 표준화한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **소프트웨어 컴포넌트(Software Component, SWC)**: 차량의 특정 제어 로직(제동, 조향, 와이퍼 등)을 구현한 최상위 독립 모듈.
- **기본 소프트웨어(Basic Software, BSW)**: OS, 메모리 관리, 통신, 진단 등 공통 서비스를 제공하는 표준 플랫폼 계층.
- **마이크로컨트롤러 추상화 계층(Microcontroller Abstraction Layer, MCAL)**: MCU 레지스터를 제어하는 최하위 하드웨어 드라이버 계층.

</details>

```text
[AUTOSAR Classic 계층형 아키텍처]
 ├─ 응용 소프트웨어 계층 ─── SWC와 포트 인터페이스
 ├─ 런타임 환경(RTE) ─────── VFB 기반 통신 중계
 ├─ 기본 소프트웨어(BSW)
 │   ├─ 서비스 계층 ───────── OS·통신·메모리·진단
 │   ├─ ECU 추상화 계층 ───── 외장 장치 통합 드라이버
 │   └─ MCAL ──────────────── MCU 주변장치 드라이버
 └─ 마이크로컨트롤러 ──────── 물리 실리콘 칩셋
```

선의 의미: 가지(`├─`, `└─`)는 계층의 포함 관계

| 구성요소 | 책임 |
|:---|:---|
| 애플리케이션 SWC | 포트 기반 **차량 제어 로직** 구현 |
| RTE | VFB 설계를 **ECU 통신**에 매핑 |
| 서비스 계층 | OS·통신·메모리·진단 서비스 제공 |
| ECU 추상화 계층 | 외장 장치를 공통 인터페이스로 추상화 |
| MCAL 드라이버 | MCU 주변장치 **레지스터 제어** |

#### 한줄 요약
- SWC, RTE, BSW, MCAL 계층 분리로 칩셋 변경 영향을 차단한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **러너블(Runnable Entity)**: 타이머 틱이나 데이터 수신 이벤트에 의해 RTE로부터 트리거되어 실제 연산을 수행하는 SWC 내부의 최소 C 함수 단위.

</details>

```text
[전장 시스템 아키텍처 설계]
          │
1. 통신 매트릭스 정의 및 ARXML 모델링
          │
2. 타깃 MCU와 ECU 파라미터 설정
          │
3. RTE 및 BSW 소스 코드 자동 생성
          │
4. 생성 코드와 SWC 알고리즘 통합 빌드
          │
5. ECU 플래싱과 Runnable 주기 호출
          │
[RTE 수신 → 제어 연산 → MCAL 출력]
```

동작 원리:

1. 통신 매트릭스 정의 및 ARXML 모델링: 통신 관계 명세
2. 타깃 MCU와 ECU 파라미터 설정: 실행 환경 구성
3. RTE 및 BSW 소스 코드 자동 생성: 표준 계층 구현
4. 생성 코드와 SWC 알고리즘 통합 빌드: 실행물 생성
5. ECU 플래싱과 Runnable 주기 호출: 제어 기능 실행

#### 한줄 요약
- 계층화는 하드웨어 교체 비용을 RTE 재생성으로 흡수하는 대신 ARXML 설정과 툴체인 복잡도를 새로 떠안으므로, 재사용할 ECU 자산이 많을수록 그 고정 비용이 회수된다.

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
| BSW 오버헤드로 인한 MCU 메모리 부족 | **미사용 BSW 모듈 비활성화** 및 CDD 최적화 | 바이너리 크기와 메모리 비용 절감 |
| 차량 네트워크 데이터 변조/유실 결함 | **AUTOSAR E2E 보호 프로토콜** 적용 | ISO 26262 ASIL-D 데이터 무결성 달성 |
| OEM과 협력사 간 ARXML 버전 불일치 | **AUTOSAR 메타모델 버전 동기화** | 통합 빌드 오류와 재작업 감소 |

#### 한줄 요약
- 실무에서는 미사용 BSW 최적화로 메모리를 아끼고, E2E 보호로 기능 안전을 지키며, ARXML 형상 관리로 호환성을 확보한다.

## Ⅶ. 결론

- 정적 ECU 제어는 **Classic**, 동적 서비스는 **Adaptive** 선택

- AUTOSAR는 SDV 전장 소프트웨어 표준의 핵심이며, Classic과 Adaptive의 상호 보완적 융합을 통해 완성된다.
