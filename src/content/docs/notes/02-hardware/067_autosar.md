---
sidebar:
  order: 67
  label: "067. AUTOSAR 소프트웨어 플랫폼"
  badge:
    text: "기출 • 50%"
    variant: note
title: "AUTOSAR 소프트웨어 플랫폼"
date: "2026-08-13T12:00:06+09:00"
tags:
  - "notes-hardware"
weight: 67
extra:
  question_no: "067"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "Classic•Adaptive 구조의 단일 기출 핵심"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AUTOSAR(Automotive Open System Architecture)**: 글로벌 완성차(OEM) 및 부품사(Tier-1)가 공동 제정한 자동차 전자제어장치(ECU) 소프트웨어 개방형 표준 아키텍처.
- **ECU(Electronic Control Unit)**: 차량 내 각 기능(엔진, 섀시, ADAS 등)을 제어하는 임베디드 컴퓨터 단말.
- **소프트웨어 재사용(Software Reuse)**: 하드웨어 종속성이 제거된 표준화된 SWC(Software Component)를 타 칩셋/타 차량 플랫폼에 재배치하여 재활용하는 성질.

</details>

- 정의/개념: 차량용 전장 소프트웨어 계층(Application-RTE-BSW/ARA) 구조 및 인터페이스 메커니즘을 규격화한 **AUTOSAR** 플랫폼
- 배경/필요성: 벤더별 파편화된 전장 SW 구조로 인한 하드웨어/소프트웨어 강한 결합(Tight Coupling) 해소 및 SW 재사용성 극대화 요구

#### 한줄 요약

- AUTOSAR는 공급사 간 구조·인터페이스·개발 방법을 표준화한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **표준 인터페이스(Standardized Interface)**: 애플리케이션(SWC)과 기본 소프트웨어(BSW) 간 데이터 교환 및 함수 호출 규칙 규격.
- **ARXML(AUTOSAR XML)**: SWC 포트 사양, BSW 설정, CAN/Ethernet 통신 매핑 정보를 규정하는 AUTOSAR 전용 표준 XML 설명 파일.
- **Classic Platform**: MCU 기반 저전력, 하드 실시간 및 정적 스케줄링(Deep Embedded)을 전용 처리하는 아키텍처.
- **Adaptive Platform**: MPU/SoC 기반 고성능 컴퓨팅, 동적 SOA(Service-Oriented Architecture) 및 자율주행/연결성을 수용하는 아키텍처.

</details>

- 응용 SW와 하드웨어를 분리(Decoupling)하는 **표준 인터페이스** 도입
- 툴 체인 간 아키텍처 메타데이터를 상호 교환하는 표준 **ARXML** 지원
- 정적 제어 중심의 **Classic Platform**과 서비스 지향의 **Adaptive Platform** 구분

#### 한줄 요약

- ARXML로 설계 정보를 교환하더라도 차량별 생성 결과와 통합 동작은 별도로 검증해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SWC(Software Component)**: 차량 기능(예: 제동, 조향 등)을 구현하는 최상위 애플리케이션 소프트웨어 캡슐화 단원.
- **RTE(Runtime Environment)**: SWC 간 또는 SWC와 BSW 간의 포트 통신 및 함수 호출을 중개하는 추상화 미들웨어 계층.
- **BSW(Basic Software)**: OS, 메모리, 진단(DoIP/UDS), 통신(CAN/Eth) 및 칩셋 추상화(**MCAL**) 서비스를 제공하는 하단 인프라 SW.
- **MCAL(Microcontroller Abstraction Layer)**: 하드웨어 MCU 핀 및 온칩 주변장치를 표준 API로 추상화하는 BSW 최하위 레이어.
- **ARA(AUTOSAR Runtime for Adaptive Applications)**: Adaptive 응용에 서비스 인터페이스와 플랫폼 기능을 제공하는 API 집합.

</details>

```text
Classic 구조:  [응용 SWC] -- [RTE] -- [BSW•MCAL]

Adaptive 구조: [Adaptive 응용] -- [ARA•기능 클러스터]
```

선의 의미: Classic 및 Adaptive 아키텍처 상에서 상위 응용 레이어가 미들웨어(RTE/ARA)를 거쳐 하부 BSW/기능 클러스터로 연동되는 표준 스택.

| 구성요소 | 책임 |
|:---|:---|
| 응용 SWC | 포트(Port) 기반 차량 로직 수행 및 하드웨어 독립성 보유 |
| RTE | SWC 간 통신 및 BSW 서비스 호출에 대한 **RTE** 가상 버스 매핑 |
| BSW•MCAL | OS 타이머, CAN/LIN 통신, UDS 진단 및 **MCAL** 하드웨어 제어 |
| Adaptive 응용 | POSIX 기반 ADAS·자율주행 서비스 로직 실행 |
| ARA•기능 클러스터 | **ARA** 서비스 탐색, 실행 관리 및 갱신 기능 제공 |

#### 한줄 요약

- AUTOSAR는 Classic Platform의 정적 계층과 Adaptive Platform의 동적 서비스 구조를 용도에 따라 구분한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **플랫폼 할당(Platform Allocation)**: 차량 기능 속성(실시간 제어 vs 동적 서비스)에 따라 Classic 또는 Adaptive 노드로 SWC를 배분하는 공정.
- **러너블(Runnable)**: RTE가 수신 이벤트 또는 정속 주기에 맞춰 호출 실행하는 SWC 내부 코드 엔티티.
- **서비스 탐색(Service Discovery)**: SOME/IP SD 프로토콜을 통하여 Adaptive 인스턴스 간 연결을 런타임에 동적 매핑하는 절차.

</details>

```text
[차량 기능•ARXML 계약]
            │
            ▼
1. 기능•인터페이스 구성
            │
            ▼
2. 플랫폼 할당
      ┌──────┴────────┐
      │ 결정적 제어   │ 동적 서비스
      ▼               ▼
  [Classic]       [Adaptive]
      └──────┬────────┘
             ▼
3. 플랫폼 응용 실행
   ├─ Classic: SWC•RTE 러너블
   └─ Adaptive: 응용•ARA 서비스
             │
             ▼
4. 플랫폼 인프라 처리
   ├─ Classic: BSW•MCAL 제어
   └─ Adaptive: 기능 클러스터 관리
             │
             ▼
5. 종단 계약 검증
            │
            ▼
   [차량 제어•서비스 결과]
```

### 동작 원리

1. **기능·인터페이스 구성**: **ARXML** 기반 시스템 명세로 SWC 포트, 데이터 인터페이스와 매핑 정의.
2. **플랫폼 할당**: 제어 실시간성 여부에 따라 **Classic Platform** 또는 **Adaptive Platform**으로 노드 할당.
3. **플랫폼 응용 실행**: Classic의 **RTE 러너블** 스케줄링 또는 Adaptive의 SOME/IP **서비스 탐색** 기반 호출 전개.
4. **플랫폼 인프라 처리**: BSW/MCAL을 통한 MCU 제어 또는 ARA 기능 클러스터를 통한 서비스 갱신 관리.
5. **종단 계약 검증**: E2E 데이터 무결성과 시스템 마감시간 충족 여부 검증.

#### 한줄 요약

- 표준 인터페이스는 응용과 장치·플랫폼 사이의 결합을 줄이고 종단 검증 기준을 제공한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **정적 구성(Static Configuration)**: 빌드 시점에 태스크, RTE 매핑과 BSW 메모리 배치를 결정하는 아키텍처.
- **SOA(Service-Oriented Architecture)**: 서비스 바인딩 및 발견을 런타임에 동적으로 매핑하는 서비스 지향 아키텍처.

</details>

| AUTOSAR 플랫폼 | Classic Platform | Adaptive Platform |
|:---|:---|:---|
| 적용 기준 | MCU 기반 하드 실시간 섀시, 파워트레인 제어 시 | MPU 기반 ADAS, 인포테인먼트, 자율주행 서버 구축 시 |
| 핵심 특징 | **정적 구성**, C 기반, OSEK 계열 OS, **BSW/MCAL** 스택 | **SOA** 서비스 바인딩, POSIX OS, **ARA** API |
| 한계 | 동적 SW 업데이트 한계 및 고성능 컴퓨팅 수용 불가 | 결정적 하드 실시간 보장 복잡성 및 풋프린트 오버헤드 |

#### 한줄 요약

- 정적 주기 제어에는 Classic, 실행 중 변경되는 고성능 서비스에는 Adaptive가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **ARXML 스키마**: 툴 벤더 간 맵핑 불일치를 차단하기 위해 엄격히 동기화하는 메타모델 규격.
- **원자적 갱신(Atomic Update)**: 갱신 단위를 완전 적용하거나 이전 상태로 롤백하는 업데이트 기법.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 툴 벤더 간 **ARXML** 메타모델 스키마 버전 불일치 | 시스템 전반의 **ARXML 스키마** 버전에 대한 통일 및 검증 | 툴 체인 간 호환성 에러 차단 |
| RTE 래퍼 및 **BSW** 계층 적용으로 인한 메모리 오버헤드 | MCAL/BSW 미사용 모듈 가지치기 | 오버헤드 감소 및 스택 경량화 |
| Adaptive 모듈 갱신 중 시스템 장애 위험 | **원자적 갱신 및 롤백** 기반 OTA 적용 | 실패한 소프트웨어 갱신에서 복구 |

> 사례: **Classic** 기반 BSW 튜닝 및 **Adaptive** SOME/IP 연동 통합 플랫폼 구축

#### 한줄 요약

- Classic ECU에서는 주기 실행과 차량 신호 종단 지연을 함께 검증해야 제어 데드라인을 입증할 수 있다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **플랫폼 선택 기준(Platform Selection Criteria)**: 하드 실시간성, 컴퓨팅 파워, 동적 서비스 요구량에 기반한 아키텍처 결정 체계.

</details>

- 정적 실시간 제어는 **Classic Platform**, 동적 고성능 서비스는 **Adaptive Platform** 선택

#### 한줄 요약

- 정적 실시간 제어는 Classic, 동적 고성능 서비스는 Adaptive를 선택한다.
