---
sidebar:
  order: 206
  label: "206. AUTOSAR Adaptive Platform"
  badge:
    text: "기출 · 70%"
    variant: note
title: "AUTOSAR Adaptive Platform"
date: "2026-09-07T16:00:00+09:00"
tags:
  - "notes-latest-tech"
weight: 206
extra:
  question_no: "206"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "AUTOSAR Adaptive 서비스 구조가 최근 출제됨"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **AUTOSAR Adaptive Platform(Automotive Open System Architecture Adaptive Platform)**: 고성능 ECU 애플리케이션을 POSIX 프로세스와 동적 서비스로 실행•관리하는 차량 소프트웨어 플랫폼이다.
- **전자제어장치(Electronic Control Unit, ECU)**: 차량 기능의 센서 입력•연산•제어 출력을 담당하는 컴퓨터이다.
- **이식 가능 운영체제 인터페이스(Portable Operating System Interface, POSIX)**: 운영체제 간 호환 가능한 프로세스•파일•통신 인터페이스 표준이다.

</details>

- 정의: 고성능 ECU 앱을 POSIX 프로세스•동적 서비스로 실행하는 **Adaptive Platform**
- 배경/필요성: 전통적인 AUTOSAR Classic Platform은 OSEK 기반 정적 스케줄링과 C 언어 기반 컴파일 시점 고정 구조를 취하여 마이크로컨트롤러(MCU) 단위의 엄격한 실시간성(Hard Real-time)은 보장하지만, 자율주행(AD/ADAS), 고성능 인포테인먼트(IVI), V2X, AI 딥러닝 연산에 요구되는 64비트 멀티코어 고성능 프로세서(HPC), 대용량 기가비트 이더넷 통신, 런타임 동적 프로세스 생성 및 무선 소프트웨어 업데이트(OTA)를 수용할 수 없는 근본적 한계에 직면함에 따라, 고성능 차량용 컴퓨팅 환경을 위한 서비스 지향 차량용 소프트웨어 표준 플랫폼인 AUTOSAR Adaptive Platform(POSIX PSE51 Compliant OS / C++14 Language Standard / Service-Oriented Architecture: SOA, SOME/IP, REST / ARA: AUTOSAR Runtime for Adaptive Applications / Execution Management, Platform Health Management: PHM, Update & Configuration Management: UCM, Identity & Access Management: IAM, Cryptography)을 도입하여 **POSIX 기반 독립 가상 주소 공간 및 멀티스레드 프로세스 격리를 통한 결함 격리성(Fault Isolation) 확보, `ara::com` 서비스 지향 통신(SOA)을 통한 분산 서비스의 동적 탐색/바인딩 및 이기종 이더넷 통신 지원, UCM(Update & Configuration Management)을 통한 차량 출고 후 개별 애플리케이션 단위의 안전한 무중단 무선(OTA) 배포/업데이트**를 달성할 필요

#### 한줄 요약

- 정해진 제어를 반복하는 Classic과 달리, Adaptive는 고성능 컴퓨터에서 여러 앱과 서비스를 동적으로 연결•갱신한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Adaptive 애플리케이션용 AUTOSAR 런타임(AUTOSAR Runtime for Adaptive Applications, ARA)**: Adaptive 애플리케이션이 통신•실행•진단 등 플랫폼 기능을 사용하는 표준 C++ 인터페이스이다.

</details>

- **POSIX** 기반 독립 프로세스 실행•자원 격리
- `ara::com` 기반 **동적 서비스 탐색•통신**
- 실행•건강•설정•갱신의 **플랫폼 생명주기 통합**
#### 한줄 요약

- 고성능 차량 앱을 독립 프로세스로 실행하고 표준 서비스로 통신•상태•갱신을 관리한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **실행 관리(Execution Management)**: 의존성과 실행 상태에 따라 Adaptive 프로세스의 시작•중지•상태를 관리하는 서비스이다.
- **ara::com**: ARA에서 서비스 탐색과 이벤트•메서드•필드 통신을 제공하는 인터페이스이다.
- **응용 프로그래밍 인터페이스(Application Programming Interface, API)**: 소프트웨어 간 기능•데이터 교환 규칙을 정의한 접점이다.
- **업데이트•구성 관리(Update and Configuration Management, UCM)**: 소프트웨어 패키지와 차량 구성을 검증•설치•활성화•롤백하는 서비스이다.
- **플랫폼 건강 관리(Platform Health Management, PHM)**: 애플리케이션과 플랫폼의 생존•기한•논리 상태를 감시하는 서비스이다.

</details>

```text
[AUTOSAR Adaptive 아키텍처]
├── [애플리케이션 인터페이스]
│   └── [ARA•ara::com]
├── [플랫폼 관리 서비스]
│   ├── [Execution Management]
│   ├── [UCM]
│   └── [PHM]
└── [기반 운영체제]
    └── [POSIX 운영체제]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| ARA•ara::com | 플랫폼 기능 접근과 **서비스 탐색•통신** |
| Execution Management | 프로세스 **시작•중지•상태 관리** |
| UCM | 패키지 **검증•활성화**와 설치•롤백 |
| PHM | 애플리케이션•플랫폼의 **건강 상태 감시** |
| POSIX 운영체제 | **프로세스•자원 기반**과 격리 제공 |

#### 한줄 요약

- ARA의 앱 연결과 **실행•통신 서비스 추상화**

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **매니페스트(Manifest)**: 애플리케이션•서비스•실행•배포 구성을 기계 판독 형식으로 선언한 명세이다.

</details>

UCM•PHM•ARA의 **배포•통신 상태 관리**

```text
[UCM]
  │ 1. 검증 패키지•Manifest
  ▼
[실행 관리자]
  │ 2. 프로세스 시작
  ▼
[Adaptive App] ── 3. 서비스 탐색 요청 ──▶ [ara::com]
[Adaptive App] ◀──── 서비스 인스턴스 ───── [ara::com]
  │ 4. 건강 체크포인트
  ▼
[PHM] ── 5. 오류 대응 지시 ──▶ [실행 관리자]
```

### 동작 원리

1. 검증 패키지•Manifest: 서명•호환성 확인 후 구성 설치
2. 프로세스 시작: 의존성과 실행 상태에 따라 애플리케이션 기동
3. 서비스 탐색 요청: 런타임 위치와 제공 인스턴스 탐색
4. 건강 체크포인트: 생존•기한•논리 상태 주기적 보고
5. 오류 대응 지시: 재시작•기능 저하•안전 상태 전환 결정

#### 한줄 요약

- 앱 기동•서비스 탐색과 **건강 감시•안전 재시작**

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Classic Platform**: MCU 기반의 정적 구성과 결정적 실시간 제어에 적합한 AUTOSAR 플랫폼이다.
- **마이크로컨트롤러 유닛(Microcontroller Unit, MCU)**: 프로세서•메모리•입출력을 단일 칩에 통합한 제어용 컴퓨터이다.

</details>

Classic•Adaptive의 **제어 특성•실행 기반** 비교

| AUTOSAR 구성 | Classic Platform | Adaptive Platform | 혼합 아키텍처 |
|:---|:---|:---|:---|
| 적용 기준 | **결정적 MCU 제어** | **고성능•동적 서비스** | 제어와 **고성능 기능 공존** |
| 핵심 특징 | **정적 구성•실시간 실행** | **POSIX•서비스•프로세스** | 플랫폼 간 **역할 분리** |
| 한계 | **동적 기능•연산 확장 제한** | 엄격한 **실시간 제어 부적합** | **게이트웨이•안전 통합** 필요 |

#### 한줄 요약

- 두 플랫폼은 차량 소프트웨어를 결정성과 유연성 중 무엇에 맞출지로 갈리므로 택일이 아니라, 주기 제어는 Classic에 남기고 **고성능 동적 앱**만 Adaptive로 올리는 분담이 된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **시간 예산**: 기능이 입력부터 출력까지 완료해야 하는 최대 허용 시간이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 실시간 경계 미검증 시 일반 프로세스의 **결정성 부족** | 엄격 제어의 Classic 분리와 **시간 예산 검증** | 플랫폼 **결정성 경계** 보존 |
| 서비스 계약 미검증 시 버전•인터페이스의 **호환성 실패** | 매니페스트•API 버전•**통합 시험** | 서비스 **버전 호환성** 확보 |
| 동적 갱신 미검증 시 불완전 패키지의 **기능•안전 영향** | 서명•원자 설치•롤백•**재시작 전략** | 갱신 실패 **안전 영향** 제한 |

#### 한줄 요약

- 시간•안전 책임 분리와 **서비스 계약•갱신 복구 검증**

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **혼합 아키텍처**: 결정적 제어를 Classic에, 고성능 동적 서비스를 Adaptive에 배치해 역할을 분리하는 구조이다.

</details>

- SDV(소프트웨어 정의 차량) 및 자율주행 고성능 중앙 집중형 컴퓨팅(HPC)의 핵심 소프트웨어 인프라로 확립된 **차세대 고성능 차량용 개방형 소프트웨어 플랫폼 및 서비스 지향 아키텍처(SOA)의 최고 표준(AUTOSAR Adaptive Platform / POSIX OS & C++14 Standard / ARA Service Interface / SOME/IP & DDS Communication / UCM OTA Standard)의 확고한 표준**으로 확고히 자리 잡았으며, ROS2 및 차량용 리눅스(AGL)와의 하이브리드 미들웨어 통합으로 진화하는 가운데, 실무 차량 E/E 아키텍처 구축 시에는 **밀리초(ms) 단위 하드 실시간 제어(파워트레인, 섀시)는 Classic에 유지하고, 인공지능/자율주행/OTA 서비스는 Adaptive에 배치하는 최적의 Classic-Adaptive 상호운용성(SOME/IP Gateway) 및 ISO 26262 ASIL-D 기능안전**을 결합하여 완벽한 차량 컴퓨팅 성능과 주행 안전성을 완성

#### 한줄 요약

- **통신•시간 책임**과 안전 책임을 Classic•Adaptive 사이에 분리
