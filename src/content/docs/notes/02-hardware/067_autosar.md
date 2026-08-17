---
sidebar:
  order: 67
  label: "067. AUTOSAR 소프트웨어 플랫폼"
  badge:
    text: "기출 • 50%"
    variant: note
title: "AUTOSAR 소프트웨어 플랫폼"
date: "2026-08-17T09:25:00+09:00"
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

- **AUTOSAR(Automotive Open System Architecture)**: 완성차(OEM) 및 부품사(Tier-1)가 주도하여 차량용 ECU 소프트웨어의 재사용성과 상호운용성을 위해 제정한 개방형 표준 아키텍처.
- **ECU(Electronic Control Unit)**: 차량 내 엔진, 제동, 조향 등을 개별 제어하는 마이크로컨트롤러 기반 전장 모듈.
- **Software Reuse(소프트웨어 재사용성)**: 하드웨어 마이크로컨트롤러(MCU) 벤더가 변경되어도 응용 소프트웨어 로직의 수정 없이 재사용할 수 있는 특성.

</details>

- 정의/개념: 차량용 전장 소프트웨어의 재사용성(Reuse)과 이식성(Portability)을 극대화하기 위해 응용 계층(SWC), 가상 버스(RTE), 기본 소프트웨어(BSW/ARA) 및 하드웨어 추상화 계층을 표준화한 개방형 자동차 소프트웨어 아키텍처
- 배경/필요성: 차량 ECU 수 증가 및 전장 복잡도 급증에 따른 **하드웨어 칩 종속성을 탈피하고, 완성차(OEM)와 전장 부품사(Tier 1) 간의 협업 및 SDV(Software-Defined Vehicle) 전환 가속**

#### 한줄 요약

- 하드웨어 추상화(MCAL) 및 미들웨어(RTE) 기반으로 **차량용 소프트웨어 재사용성과 표준화 실현**

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **ARXML(AUTOSAR XML)**: SWC 인터페이스, BSW 설정, 통신 매트릭스를 기술하여 이종 개발 툴체인 간에 교환 가능한 표준 메타모델 포맷.
- **Classic Platform(CP)**: OSEK OS 기반으로 $\mu\text{s}$ 단위의 하드 실시간 제어를 수행하는 정적(Static) 아키텍처.
- **Adaptive Platform(AP)**: POSIX OS(Linux/QNX) 기반으로 자율주행, V2X, OTA 등 고성능 서비스 지향(SOA)을 지원하는 동적 아키텍처.

</details>

- 하드웨어 변경 시에도 응용 코드를 보호하는 **가상 함수 버스(VFB) 및 표준화된 인터페이스**
- 완성차와 협력사 간 협업 개발 및 자동 코드 생성을 지원하는 **ARXML 표준 메타모델 교환 체계**
- 안전 필수 실시간 제어용 **Classic Platform**과 고성능 연산/SOA용 **Adaptive Platform**의 투트랙 분할

#### 한줄 요약

- **계층 분리 및 표준 인터페이스(VFB)·ARXML 기반 협업 체계·Classic/Adaptive 플랫폼 투트랙 전개**

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **SWC(Software Component)**: 차량 기능을 모듈화한 응용 컴포넌트로 포트(Port)를 통해서만 타 SWC 및 BSW와 통신.
- **RTE(Runtime Environment)**: SWC 간 통신 및 SWC-BSW 간 인터페이스를 중계하는 가상 버스 미들웨어.
- **BSW(Basic Software)**: 시스템 서비스, 메모리 관리, 통신 스택, I/O 드라이버를 제공하는 하부 인프라.
- **MCAL(Microcontroller Abstraction Layer)**: 칩셋 레지스터에 직접 접근하는 최하위 하드웨어 추상화 드라이버.
- **ARA(AUTOSAR Runtime for Adaptive Applications)**: Adaptive 플랫폼에서 서비스 지향 통신(ara::com)과 실행 관리(ara::exec)를 제공하는 C++ API.

</details>

```text
[ AUTOSAR Classic 및 Adaptive 플랫폼 스택 아키텍처 ]
 
 ┌── Classic Platform (하드 실시간 제어) ──┐  ┌── Adaptive Platform (고성능 자율주행/SOA) ──┐
 │  [ Application SWC (응용 컴포넌트) ]    │  │  [ Adaptive Applications (C++ 응용) ]       │
 ├─────────────────────────────────────────┤  ├─────────────────────────────────────────────┤
 │  [ Runtime Environment (RTE 미들웨어) ] │  │  [ ARA (AUTOSAR Runtime for Adaptive Apps) ]│
 ├─────────────────────────────────────────┤  ├─────────────────────────────────────────────┤
 │  [ Basic Software (BSW) 계층 ]          │  │  [ Functional Clusters (SOME/IP, UCM, IAM) ]│
 │   ├─ System, Memory, Comm Services      │  ├─────────────────────────────────────────────┤
 │   └─ MCAL (Microcontroller 추상화)      │  │  [ POSIX OS (Linux / QNX) + Hypervisor ]    │
 ├─────────────────────────────────────────┤  ├─────────────────────────────────────────────┤
 │  [ 마이크로컨트롤러 (MCU Hardware) ]    │  │  [ 고성능 SoC (MPU / GPU 가속기) ]          │
 └─────────────────────────────────────────┘  └─────────────────────────────────────────────┘
```

선의 의미: 응용 계층(SWC/Adaptive App), 미들웨어(RTE/ARA), 인프라 계층(BSW/MCAL 및 POSIX OS) 간의 AUTOSAR Classic 및 Adaptive 스택 구조도.

| 구성요소 | 책임 |
|:---|:---|
| 응용 소프트웨어 컴포넌트 | 브레이크 밟기, 에어백 터뜨리기처럼 하드웨어 칩이 뭔지 신경 안 쓰고 순수 로직만 짜놓은 최상위 캡슐 |
| 런타임 환경 미들웨어 | 윗동네(응용 앱)와 아랫동네(하드웨어)가 직접 삿대질 못 하게 중간에서 통신과 호출을 엮어주는 가상 버스 우체국 |
| 기본 소프트웨어 및 MCAL | OS 타이머, CAN 통신, 진단 기능을 제공하며, 가장 밑바닥(**마이크로컨트롤러 추상화 계층**)에서 하드웨어 칩 핀을 직접 쑤심 |
| 어댑티브 응용 및 아라 | 리눅스(POSIX) 기반으로 자율주행 영상 처리 같은 빡센 서비스를 돌리며, 앱들에게 **아라** API를 통해 동적 통신망을 깔아줌 |

#### 한줄 요약

- **응용 소프트웨어(SWC/App)·가상 버스 런타임(RTE/ARA)·기본 소프트웨어(BSW)·하드웨어 추상화(MCAL)**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Runnable**: SWC 내부에서 특정 주기(10ms) 또는 이벤트 발생 시 RTE에 의해 호출되는 C 함수 실행 단위.
- **SOME/IP**: Adaptive 플랫폼에서 이더넷 기반 서비스 지향 통신(SOA)을 구현하기 위한 차량용 미들웨어 프로토콜.

</details>

```text
[ ARXML 시스템 명세 및 Classic/Adaptive 실행 흐름 ]
                         │
                         ▼
   [ 1. ARXML 기반 시스템 설계 (SWC 인터페이스 및 통신 매트릭스 정의) ]
                         │
                         ▼
   [ 2. 플랫폼 분할 할당 (하드 실시간 제어 ──> CP, 고성능 연산/SOA ──> AP) ]
        /                                               \
   [ Classic Platform ]                            [ Adaptive Platform ]
        │                                               │
   3. RTE가 10ms 주기 Runnable 디스패치             3. ara::com 기반 서비스 탐색(SOME/IP)
        │                                               │
   4. BSW/MCAL 통해 하드웨어 핀/CAN 제어          4. POSIX OS 위에서 기가비트 이더넷 전송
        \                                               /
         +──────────────────────┬──────────────────────+
                                │
                                ▼
   [ 5. E2E(End-to-End) 데이터 무결성 검증 및 마감시간 충족 확인 ]
```

**동작 원리**

1. **ARXML 설계**: 시스템 아키텍트가 포트, 데이터 타입, 통신 인터페이스를 표준 XML 파일로 정의
2. **플랫폼 할당**: 브레이크/조향은 Classic으로, ADAS 비전/OTA는 Adaptive 플랫폼으로 노드 매핑
3. **런타임 디스패치**: Classic은 RTE가 정적 주기로 Runnable을 실행하고, Adaptive는 SOME/IP 서비스 탐색으로 동적 바인딩
4. **하부 인프라 제어**: Classic은 MCAL 드라이버를 통해 MCU 핀을 제어하고, Adaptive는 POSIX 소켓을 통해 고속 통신
5. **E2E 검증**: E2E Protection 라이브러리를 통해 데이터 변조 및 시퀀스 누락을 최종 검증

#### 한줄 요약

- ARXML 시스템 명세 $\to$ **플랫폼 할당(Classic vs Adaptive) $\to$ RTE Runnable 주기 실행 / ARA 서비스 동적 탐색 $\to$ MCAL/POSIX I/O $\to$ E2E 마감시간 검증**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Classic vs Adaptive Platform**:
  - Classic: OSEK OS, C 언어, 신호 기반(Signal), 정적 컴파일, 파워트레인/섀시
  - Adaptive: POSIX OS, C++14, 서비스 지향(SOA), 동적 런타임, 자율주행/인포테인먼트

</details>

| 비교 항목 | AUTOSAR Classic Platform (CP) | AUTOSAR Adaptive Platform (AP) |
|:---|:---|:---|
| 아키텍처 및 OS 기반 | OSEK/VDX 기반 정적 실시간 RTOS, C 언어 | POSIX 호환 OS (Linux/QNX), C++14/17 |
| 통신 및 스케줄링 모델 | 신호 기반(Signal-based), 정적 시간 구동(Time-Triggered) | 서비스 지향(SOA: SOME/IP), 동적 이벤트 구동 |
| 한계 및 주 적용 분야 | 고성능 연산 및 OTA 제약 (파워트레인/섀시/에어백) | 하드 실시간성 보장 난제 (자율주행 ADAS/인포테인먼트) |

#### 한줄 요약

- 하드 실시간 제어는 **Classic(CP)**, 고성능 자율주행/SOA는 **Adaptive(AP)**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **UCM(Update and Configuration Management)**: Adaptive 플랫폼에서 개별 앱과 서비스를 무중단으로 설치, 갱신 및 롤백하는 표준 OTA 관리 모듈.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 보쉬(Bosch) 툴로 짠 ARXML 설계도를 타 벤더 툴에서 열었더니 에러 뿜고 다 깨지는 툴 체인 호환성 붕괴 사태 | 오토사 표준 위원회에서 시스템 전반의 **에이알엑스엠엘 스키마** 버전을 뼛속까지 통일하고 강제 동기화 | 벤더 간 밥그릇 싸움으로 인한 설계도(메타모델) 맵핑 붕괴 및 호환성 에러 100% 원천 차단 |
| 윗동네(응용)와 아랫동네(하드웨어)를 찢어놓느라, 중간 미들웨어(RTE)가 칩셋의 귀한 메모리를 잡아먹는 오버헤드 | 코드를 굽기 전에, 당장 안 쓰는 MCAL이나 BSW 모듈들을 가위로 난도질해 잘라내는 무자비한 가지치기 최적화 수행 | 제한된 칩셋 메모리가 터져나가는 끔찍한 오버헤드 압박을 해소하고 극강의 스택 경량화 달성 |
| 차가 달리면서 어댑티브 무선 업데이트(OTA) 하다가 중간에 끊겨서 차가 쇳덩이(벽돌)가 되는 끔찍한 위험 발발 | 업데이트가 100% 완벽히 안 끝나면 아예 예전 코드로 통째로 되돌려버리는 얄짤없는 **원자적 갱신** 및 롤백 적용 | 실패한 소프트웨어 갱신 때문에 시스템 전체가 먹통이 되는 A/S 복구 불능 사태를 완벽 방어 |

#### 한줄 요약

- **ARXML 스키마 버전 동기화·BSW 미사용 모듈 가지치기(Pruning)·UCM 기반 원자적 무중단 OTA 롤백**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **SDV(Software-Defined Vehicle) Zonal 아키텍처**: 4~6개의 Zone 제어기(Classic)가 액추에이터를 담당하고, 중앙 고성능 컴퓨터(Adaptive)가 모든 주행 판단과 클라우드 연동을 전담.

</details>

- 차세대 SDV 및 중앙 집중형 Zonal E/E 아키텍처에서 **Zone ECU는 Classic Platform, Central HPC는 Adaptive Platform을 융합한 하이브리드 표준 채택**

#### 한줄 요약

- **실시간 결정론(Classic)과 고성능 연산/SOA 확장성(Adaptive)**의 최적 플랫폼 배치
