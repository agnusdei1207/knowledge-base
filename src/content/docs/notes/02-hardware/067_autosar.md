---
sidebar:
  order: 67
  label: "067. AUTOSAR 소프트웨어 플랫폼"
  badge:
    text: "기출 • 50%"
    variant: note
title: "AUTOSAR 소프트웨어 플랫폼"
date: "2026-08-06T23:27:50+09:00"
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

<details><summary>핵심 용어</summary>

- **자동차 개방형 시스템 아키텍처(Automotive Open System Architecture, AUTOSAR)**: 차량 소프트웨어 구조와 인터페이스를 표준화한 플랫폼이다.
- **전자제어장치(Electronic Control Unit, ECU)**: 센서 입력과 제어 소프트웨어에 따라 차량 기능을 실행하는 내장 컴퓨터이다.
- **소프트웨어 재사용(Software Reuse)**: 표준 인터페이스를 지킨 기능을 여러 차량과 하드웨어 구성에서 반복 활용하는 방식이다.

</details>

- 정의/개념: 차량 소프트웨어의 **구조•인터페이스•개발 방법**을 표준화하여 응용과 하드웨어의 결합을 줄이는 플랫폼이다.
- 배경/필요성: 공급사마다 독자 인터페이스를 사용하면 ECU 통합과 차량별 소프트웨어 재사용이 어려워지므로 공통 계약이 필요하다.

#### 한줄 요약

- AUTOSAR는 공급사 간 **구조•인터페이스•개발 방법**을 표준화한다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **표준 인터페이스(Standard Interface)**: 공급사와 하드웨어가 달라도 데이터 형식과 호출 규칙을 일관되게 유지하는 접점이다.
- **확장 가능 마크업 언어(Extensible Markup Language, XML)**: 구조화된 데이터 교환 형식이다.
- **AUTOSAR XML(ARXML)**: 시스템•소프트웨어•통신 설계 정보 교환 형식이다.
- **Classic Platform**: 정적 구성과 결정적인 주기 제어를 중심으로 하는 AUTOSAR 플랫폼이다.
- **Adaptive Platform**: 서비스 지향 구조와 고성능 동적 응용을 중심으로 하는 AUTOSAR 플랫폼이다.

</details>

- **표준 인터페이스**는 응용이 특정 하드웨어와 공급사 구현에 직접 의존하지 않게 한다.
- **ARXML 계약**은 공급사와 개발 도구 사이에서 동일한 시스템•통신 설계 정보를 교환하게 한다.
- **Classic•Adaptive** 플랫폼은 결정적 제어와 동적 고성능 서비스에 서로 다른 실행 구조를 제공한다.

#### 한줄 요약

- **ARXML 계약**으로 설계 정보를 교환하더라도 차량별 생성 결과와 통합 동작은 별도로 검증해야 한다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **소프트웨어 구성요소(Software Component, SWC)**: 차량 기능을 포트와 러너블 단위로 캡슐화한 AUTOSAR 응용 구성요소이다.
- **런타임 환경(Runtime Environment, RTE)**: Classic SWC와 기본 소프트웨어 사이의 포트 통신과 호출을 중개하는 계층이다.
- **기본 소프트웨어(Basic Software, BSW)**: 운영체제•통신•진단 서비스를 제공하는 계층이다.
- **마이크로컨트롤러 추상화 계층(Microcontroller Abstraction Layer, MCAL)**: MCU 장치 접근을 표준화하는 BSW 하위 계층이다.
- **Adaptive 응용(Adaptive Application)**: 고성능 운영체제 위에서 동적 차량 서비스를 실행하는 응용이다.
- **Adaptive 응용 런타임(AUTOSAR Runtime for Adaptive Applications, ARA)**: Adaptive 표준 API와 기능 클러스터를 제공하는 실행 기반이다.

</details>

```text
Classic 구조:  [응용 SWC] -- [RTE] -- [BSW•MCAL]

Adaptive 구조: [Adaptive 응용] -- [ARA•기능 클러스터]
```

선의 의미: 각 선은 Classic 또는 Adaptive 플랫폼 내부 계층의 정적 결합이며, 두 플랫폼 사이의 직접 연결을 뜻하지 않는다.

| 구성요소 | 책임 |
|:---|:---|
| 응용 SWC | **차량 제어 기능 실행** |
| RTE | **포트•호출 중개** |
| BSW•MCAL | **서비스•장치 추상화** |
| Adaptive 응용 | **고성능 서비스 실행** |
| ARA•기능 클러스터 | **탐색•수명주기 관리** |

#### 한줄 요약

- AUTOSAR는 **Classic 정적 계층**과 Adaptive 동적 서비스 구조를 용도에 따라 구분한다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **플랫폼 할당(Platform Allocation)**: 시간 요구와 변경성에 따라 기능을 Classic 또는 Adaptive에 배치하는 과정이다.
- **러너블(Runnable)**: 입력 이벤트나 주기에 따라 RTE가 호출하는 SWC 내부 실행 단위이다.
- **서비스 탐색(Service Discovery)**: Adaptive 응용이 실행 중 필요한 서비스 인스턴스를 찾는 기능이다.
- **종단 검증(End-to-end Validation)**: 입력부터 응용•통신•출력까지 시간과 인터페이스 계약을 확인하는 검증이다.

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

**동작 원리**

1. **기능•인터페이스 구성**: ARXML로 포트와 서비스의 데이터•호출 계약을 정의한다.
2. **플랫폼 할당**: 기능의 실시간 요구와 실행 중 변경 필요성에 따라 Classic 또는 Adaptive를 선택한다.
3. **플랫폼 응용 실행**: Classic은 RTE가 러너블을 호출하고, Adaptive는 ARA를 통해 서비스를 탐색•호출한다.
4. **플랫폼 인프라 처리**: Classic의 BSW•MCAL은 장치를 제어하고, Adaptive 기능 클러스터는 응용 수명주기를 관리한다.
5. **종단 계약 검증**: 두 플랫폼을 통과하는 지연과 데이터 및 격리 요구의 충족 여부를 확인한다.

#### 한줄 요약

- **표준 인터페이스**는 응용과 장치•플랫폼 사이의 결합을 줄이고 종단 검증 기준을 제공한다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **정적 구성(Static Configuration)**: 빌드와 배포 전에 태스크와 통신 및 메모리 배치를 확정하는 방식이다.
- **서비스 지향 아키텍처(Service-oriented Architecture, SOA)**: 기능을 독립 서비스로 제공하고 실행 중 탐색하여 호출하는 구조이다.
- **동적 업데이트(Dynamic Update)**: 시스템 운용 중 응용이나 서비스를 교체하고 수명주기를 관리하는 기능이다.

</details>

| AUTOSAR 플랫폼 | Classic | Adaptive |
|:---|:---|:---|
| 적용 기준 | 하드 실시간•**주기 제어** | 고성능•**동적 업데이트** |
| 핵심 특징 | 정적 **SWC•RTE•BSW 계층** | 동적 응용•**ARA 서비스** |
| 한계 | 정적 설정•**통합 복잡성** | 수명주기•자원•**업데이트 복잡성** |

#### 한줄 요약

- **결정적 주기 제어**에는 Classic, 실행 중 변경되는 고성능 서비스에는 Adaptive가 적합하다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>

- **ARXML 스키마**: 허용 요소와 데이터 형식을 정의한 계약이다.
- **ARXML 프로파일**: 프로젝트가 사용할 규칙 범위를 고정한 계약이다.
- **종단 최악 지연(End-to-end Worst-case Latency)**: 센서 입력부터 태스크와 통신을 거쳐 제어 출력 완료까지 걸리는 최대 시간이다.
- **원자적 갱신(Atomic Update)**: 전체 변경을 한 단위로 반영하는 방식이다.
- **롤백(Rollback)**: 실패하면 이전 정상 버전으로 복귀하는 방식이다.
- **인터페이스 계약(Interface Contract)**: 서비스의 데이터 형식과 호출 조건 및 오류 응답을 합의한 규칙이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 도구별 ARXML 스키마 버전 불일치 | **ARXML 스키마•프로파일 고정** | **도구 간 통합 오류** 감소 |
| 태스크•통신 지연으로 제어 마감시간 초과 | **종단 최악 지연 분석** | **Classic 데드라인** 충족 입증 |
| Adaptive 업데이트 중 서비스 상태 불일치 | **원자적 갱신•롤백** | **서비스 상태** 정상 버전 복구 |
| Classic•Adaptive 경계의 인터페이스•격리 불일치 | **인터페이스 계약•격리 시험** | **플랫폼 경계 위반** 검출 |

#### 한줄 요약

- Classic ECU에서는 **주기 실행•차량 신호 종단 지연**을 함께 검증해야 제어 데드라인을 입증할 수 있다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **결정적 제어(Deterministic Control)**: 최악 조건에서도 정해진 주기와 데드라인 안에 센서 처리와 출력을 완료하는 제어이다.
- **동적 서비스(Dynamic Service)**: 실행 중 탐색•시작•중지•업데이트가 가능한 독립 소프트웨어 기능이다.
- **플랫폼 선택(Platform Selection)**: 차량 기능의 시간 요구와 변경성 및 자원 규모에 따라 Classic 또는 Adaptive를 정하는 판단이다.

</details>

- 결정적 제어에는 **Classic**, 고성능 동적 서비스에는 **Adaptive**를 선택한다.

#### 한줄 요약

- **결정적 제어**에는 Classic, 실행 중 탐색•변경되는 서비스에는 Adaptive를 선택한다.
