---
sidebar:
  order: 67
  label: "067. AUTOSAR 소프트웨어 플랫폼"
  badge:
    text: "기출 · 50%"
    variant: note
title: "AUTOSAR 소프트웨어 플랫폼"
date: "2026-07-25T10:38:00+09:00"
tags:
  - "notes-hardware"
weight: 67
extra:
  question_no: "067"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "Classic·Adaptive 구조의 단일 기출 핵심"
---

## 미리 알고가기

- **자동차 개방형 시스템 아키텍처(Automotive Open System Architecture, AUTOSAR)**: ‘오토사’로 읽고 영문 핵심 글자를 단어처럼 만든 약어이며, 차량 소프트웨어 구조·인터페이스·방법론을 표준화
- **전자제어장치(Electronic Control Unit, ECU)**: ‘이시유’로 읽고 영문 머리글자를 딴 약어이며, 차량 기능을 실행하는 내장 제어 컴퓨터
- **Classic Platform**: 정적 구성과 결정적 제어 중심의 플랫폼
- **Adaptive Platform**: 서비스 지향 고성능 응용 중심의 플랫폼
- **소프트웨어 구성요소(Software Component, SWC)**: ‘에스더블유시’로 읽고 영문 머리글자를 딴 약어이며, 포트와 러너블로 차량 기능을 분리
- **포트·러너블(Port·Runnable)**: 포트는 SWC의 통신 접점이고 러너블은 이벤트에 따라 실행되는 내부 코드 단위
- **서비스 지향 아키텍처(Service-Oriented Architecture, SOA)**: ‘에스오에이’로 읽고 영문 머리글자를 딴 약어이며, 기능을 독립 서비스로 탐색·호출
- **런타임 환경(Runtime Environment, RTE)**: ‘알티이’로 읽고 영문 머리글자를 딴 약어이며, Classic SWC와 하부 서비스를 중개
- **기본 소프트웨어(Basic Software, BSW)**: ‘비에스더블유’로 읽고 영문 머리글자를 딴 약어이며, 운영체제·통신·진단·하드웨어 추상화를 제공
- **마이크로컨트롤러 추상화 계층(Microcontroller Abstraction Layer, MCAL)**: ‘엠캘’로 읽고 영문 머리글자를 단어처럼 만든 약어이며, BSW에서 하드웨어를 추상화
- **AUTOSAR XML(ARXML)**: ‘에이알엑스엠엘’로 읽고 AUTOSAR와 XML을 결합한 공식 약어이며, 설계 정보를 교환
- **확장 가능 마크업 언어(Extensible Markup Language, XML)**: ‘엑스엠엘’로 읽고 영문 머리글자를 딴 약어이며, 태그로 구조화한 데이터를 교환
- **기능 클러스터(Function Cluster)**: Adaptive 응용에 통신·실행·진단 같은 플랫폼 서비스를 제공하는 모듈 집합
- **적응형 응용 런타임(AUTOSAR Runtime for Adaptive Applications, ARA)**: ‘에이라’로 읽고 영문 핵심 글자를 딴 약어이며, 기능 클러스터를 호출하는 표준 인터페이스
- **이식형 운영체제 인터페이스(Portable Operating System Interface, POSIX)**: ‘파직스’로 읽고 영문 핵심 글자를 결합한 표준명이며, Adaptive 운영체제 기반 규격
- **실행 매니페스트(Execution Manifest)**: 프로세스 시작·수명주기 설정

## Ⅰ. 개요

- **정의/개념**: 차량 소프트웨어 구조·인터페이스 표준이다
- **배경/필요성**: 공급사 간 통합과 재개발 비용을 줄인다

### 쉽게 이해하기 (학습용)

- 여러 회사의 차량 소프트웨어를 공통 설계도와 연결 규칙으로 조립하게 하는 표준이다.

## Ⅱ. 특징

- 표준 인터페이스가 응용과 하드웨어·서비스의 결합을 낮춘다.
- ARXML 계약으로 공급사와 도구 간 설계 정보를 교환한다.
- 구성 가능한 플랫폼으로 ECU별 자원 요구에 맞춘다.
- 표준 적용 후에도 시간·자원·안전·보안을 통합 검증한다.

### 쉽게 이해하기 (학습용)

- 공통 규격을 써도 차량마다 기능 배치, 통신 지연, 안전 경계를 다시 맞춰야 한다.

## Ⅲ. 아키텍처 및 구성요소

```mermaid
flowchart LR
    X(["ARXML 구성"])
    M(["실행 매니페스트"])
    H1(["마이크로컨트롤러"])
    H2(["POSIX 운영체제"])
    subgraph CP["Classic Platform"]
        C1["Classic 응용(SWC)"]
        C2["런타임 환경(RTE)"]
        C3["기본 소프트웨어(BSW)"]
        C1 -->|"포트 호출"| C2
        C2 -->|"표준 서비스"| C3
    end
    subgraph AP["Adaptive Platform"]
        A1["Adaptive 응용"]
        A2["ARA 인터페이스·기능 클러스터"]
        A1 -->|"ARA 호출"| A2
    end
    X -->|"계약·배치 구성"| C2
    M -->|"실행·서비스 구성"| A2
    C3 -->|"MCAL"| H1
    A2 -->|"POSIX 호출"| H2
```

| 설계 요소 | 설명 |
|:---|:---|
| Classic 응용(SWC) | 포트·러너블로 차량 기능 구현 |
| 런타임 환경(RTE) | SWC 간·SWC-BSW 호출 중개 |
| 기본 소프트웨어(BSW) | 운영체제·통신·진단·MCAL 제공 |
| Adaptive 응용 | 서비스 지향 고성능 차량 기능 |
| ARA 인터페이스·기능 클러스터 | 탐색·통신·실행 관리 서비스 제공 |

> 요약: 구성 산출물로 두 플랫폼의 계층을 설정한다.

### 쉽게 이해하기 (학습용)

- 공통 설계도를 바탕으로 정적 제어 층과 동적 서비스 층을 각각 쌓는 구조다.

## Ⅳ. 원리 및 절차 흐름도

- Classic은 SWC 호출을 RTE·BSW로 전달해 장치를 제어한다
- Adaptive는 ARA로 서비스를 찾아 기능 클러스터를 호출한다

> 요약: Classic은 계층 호출, Adaptive는 서비스를 호출한다

### 쉽게 이해하기 (학습용)

- 요구에 맞는 플랫폼을 선택하고 계약과 배치를 구성한 뒤 차량에서 확인한다.

## Ⅴ. 종류 및 비교

| 판단 기준 | AUTOSAR Classic | AUTOSAR Adaptive |
|:---|:---|:---|
| 핵심 특징 | 정적 SWC·RTE·BSW 계층 | 동적 응용·ARA 서비스 구조 |
| 적용 기준 | 하드 실시간·주기 제어 | 고성능·동적 업데이트 |
| 주요 위험 | 정적 설정·통합 복잡성 | 수명주기·자원·업데이트 복잡성 |

> 요약: Classic은 실시간 제어, Adaptive는 동적 서비스다.

### 쉽게 이해하기 (학습용)

- Classic은 정해진 시간표의 제어반이고 Adaptive는 서비스를 바꿔 싣는 컴퓨터다.

## Ⅵ. 실무 사례

1. 차체 ECU는 Classic 주기 제어를 통합한다
2. 중앙 컴퓨터는 Adaptive 서비스 복구를 검증한다

### 쉽게 이해하기 (학습용)

- 차체 ECU는 주기 실행과 차량 신호 전달 시점을 함께 시험한다.
- 중앙 컴퓨터는 서비스를 찾아 실행하고 실패한 프로세스를 복구하는지 확인한다.

## Ⅶ. 결론

- 실시간은 Classic, 동적 서비스는 Adaptive를 택한다

### 쉽게 이해하기 (학습용)

- 시간표가 고정된 제어는 Classic, 실행 중 바뀌는 서비스는 Adaptive를 선택한다.
