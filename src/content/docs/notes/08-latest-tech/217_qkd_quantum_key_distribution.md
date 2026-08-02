---
sidebar:
  order: 217
  label: "217. QKD 양자키분배 (Quantum Key Distribution)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "양자키분배 (Quantum Key Distribution, QKD)"
date: "2026-07-31T09:05:11+09:00"
tags:
  - "notes-latest-tech"
weight: 217
extra:
  question_no: "217"
  source_status: "기출"
  source_history: "126회"
  priority: 50
  priority_note: "양자 키 분배의 채널·키 관리 비교가 유효함"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **양자 키 분배(Quantum Key Distribution, QKD)**: 양자 상태를 전송하고 측정 교란을 검사하여 도청 가능성을 탐지하면서 대칭키 재료를 분배하는 기술이다.

</details>

- 정의/개념: **양자 키 분배(Quantum Key Distribution, QKD)** 는 양자 상태의 측정 교란으로 도청을 탐지하며 대칭키를 분배하는 기술
- 배경/필요성: 기존 키 교환은 통신 중 **도청 여부 직접 확인 불가**

#### 한줄 요약

- 양자 신호의 오류율로 도청 가능성을 확인하고 공유 비밀키를 정제한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **이중 채널**: 양자 상태를 보내는 양자 채널과 신원 확인·키 정제를 수행하는 인증된 고전 채널을 함께 사용한다.

</details>

- 양자 상태 전송과 인증·후처리를 분리한 **이중 채널**
- **양자 비트 오류율(Quantum Bit Error Rate, QBER)** 임계값 초과 시 세션을 폐기하는 **도청 탐지**
- 기저 선별·오류 정정·프라이버시 증폭 기반 **키 정제**
#### 한줄 요약

- 상대를 인증하고 양자 비트 오류율을 검사해 비밀키를 정제한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **양자 비트 오류율(QBER)**: 수신한 양자 비트 중 오류의 비율로, 잡음과 도청 수준 및 세션 폐기 여부를 판단하는 지표다.

</details>

프로토콜은 **양자 키 분배(Quantum Key Distribution, QKD)** 의 보안 파라미터와 **양자 비트 오류율(Quantum Bit Error Rate, QBER)** 임계값을 정의한다.

```mermaid
block-beta
  columns 3
  N0["Protocol/Model"]
  N1["양자 모듈"]
  N2["고전 채널"]
  N3["관리/응용"]
  N0 --- N1 --- N2
  N2 --- N3
```

| 구성요소 | 책임 |
|:---|:---|
| Protocol/Model | **QKD 프로토콜·보안 파라미터** 정의 |
| 양자 모듈 | **광원·채널·측정기** 구성 |
| 고전 채널 | 인증 기반 **후처리 통신** |
| 관리/응용 | 최종 키의 **저장·암호 장비 전달** |

#### 한줄 요약

- 양자 신호로 키 재료를 만들고 인증된 고전 채널을 거쳐 암호 장비에 전달한다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **프라이버시 증폭**: 공격자에게 노출되었을 가능성이 있는 정보를 줄이도록 정정된 키를 더 짧은 비밀키로 압축한다.

</details>

```mermaid
sequenceDiagram
  participant A as Alice 양자 모듈
  participant Q as 양자 채널
  participant B as Bob 양자 모듈
  participant C as 인증 고전 채널·후처리
  participant K as 키 관리·암호 장비
  A->>Q: 1. 양자 상태 전송
  Q->>B: 2. 기저 선택·측정
  B->>C: 3. 기저 대조·QBER 검사
  C->>K: 4. 오류 정정·프라이버시 증폭
  K-->>A: 5. 최종 키 공급
```

**동작 원리**

- **1. 양자 상태 전송**: Alice가 무작위 기저의 양자 신호 생성
- **2. 기저 선택·측정**: Bob이 무작위 기저로 신호 측정
- **3. 기저 대조·양자 비트 오류율 검사**: 인증 채널에서 일치 비트와 **양자 비트 오류율(Quantum Bit Error Rate, QBER)** 확인
- **4. 오류 정정·프라이버시 증폭**: 정보 누출을 제거해 키 정제
- **5. 최종 키 공급**: 확인된 키를 암호 장비에 전달

#### 한줄 요약

- 양자 비트 오류율이 임계값보다 낮을 때만 키를 정제한다.

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **베넷-브라사드 1984(BB84)**: 서로 다른 두 기저로 양자 상태를 준비·측정하고 일치한 기저의 비트로 키를 만드는 양자 키 분배 프로토콜이다.

</details>

| 판단 기준 | 양자 키 분배(Quantum Key Distribution, QKD) | 양자내성암호 키 캡슐화 메커니즘(Post-Quantum Cryptography Key-Encapsulation Mechanism, PQC KEM) | 공개키 교환 |
|:---|:---|:---|:---|
| 적용 기준 | **전용 광인프라** 구간 | **기존 디지털망** 활용 | 기존 **공개키 인프라** 활용 |
| 핵심 특징 | 양자 교란 기반 **도청 탐지** | 양자내성 난제 기반 **KEM** | **인수분해·이산로그** 기반 |
| 한계 | **거리·키율·전용 장비** 제약 | **큰 키·캡슐·전환 부담** | **양자 알고리즘 취약성** |

#### 한줄 요약

- 양자 키 분배는 전용 광선로, 양자내성암호는 기존 디지털망을 사용한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **고전 채널 인증**: 중간자 공격을 막기 위해 양자 키 분배 후처리 메시지의 송신자와 무결성을 검증하는 절차다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 거리·손실의 **키 생성률 저하** | 링크 예산·중계 구조·키 버퍼 | 암호 장비의 **키 공급 안정화** |
| 장비 **측면 채널·구현 결함** | 장비 인증·탐지기 감시·패치 | 구현 보안의 **간극 축소** |
| 고전 채널의 **인증 부재** | 사전 공유키·**양자내성암호(Post-Quantum Cryptography, PQC) 인증** 결합 | **중간자 공격 방지** |

#### 한줄 요약

- 두 데이터센터의 전용 광선로에서 **양자 키 분배(Quantum Key Distribution, QKD)** 키를 생성하고 **양자 비트 오류율(Quantum Bit Error Rate, QBER)** 과 키 생성률을 확인한 뒤 데이터 암호 장비의 대칭키로 공급한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **키 정제**: 기저 선별·오류 정정·프라이버시 증폭을 거쳐 공유 비밀키를 생성하는 후처리 과정이다.

</details>

- 거리·**양자 비트 오류율(Quantum Bit Error Rate, QBER)** ·키율을 충족하는 **고가치 전용 구간**에만 **양자 키 분배(Quantum Key Distribution, QKD)** 적용

#### 한줄 요약

- 장비 도입보다 인증·오류 검사·키 정제·공급의 전 과정을 관리해야 한다.
