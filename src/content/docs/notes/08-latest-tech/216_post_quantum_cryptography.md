---
sidebar:
  order: 216
  label: "216. 양자내성암호 (Post-Quantum Cryptography)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "양자내성암호 (Post-Quantum Cryptography, PQC)"
date: "2026-08-03T08:48:47+09:00"
tags:
  - "notes-latest-tech"
weight: 216
extra:
  question_no: "216"
  source_status: "기출"
  source_history: "126회, 129회, 135회"
  priority: 85
  priority_note: "양자내성암호 전환•알고리즘이 지속 반복됨"
---

## Ⅰ. 개요

<details>
<summary>핵심 용어</summary>

- **양자내성암호(Post-Quantum Cryptography, PQC)**: 양자컴퓨터의 공격에도 안전하도록 설계하면서 고전 컴퓨터와 통신망에서 실행하는 공개키 암호 체계다.

</details>

- 정의/개념: **양자내성암호(Post-Quantum Cryptography, PQC)** 는 양자 공격에 안전하도록 설계한 고전 컴퓨터용 공개키 암호
- 배경/필요성: **RSA(Rivest-Shamir-Adleman)•타원 곡선 암호(Elliptic Curve Cryptography, ECC)** 는 쇼어 알고리즘으로 **선취 후 복호화 위험** 노출

#### 한줄 요약

- 양자 공격에 취약한 공개키 암호를 표준 양자내성암호로 단계적으로 교체한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **모듈 격자 기반 키 캡슐화 메커니즘(ML-KEM)**: 모듈 격자 문제를 기반으로 공유 비밀을 캡슐화•복원하는 표준 양자내성 키 설정 방식이다.

</details>

- 키 설정용 **모듈 격자 기반 키 캡슐화 메커니즘(Module-Lattice-Based Key-Encapsulation Mechanism, ML-KEM)** 과 서명용 **모듈 격자 기반 디지털 서명 알고리즘(Module-Lattice-Based Digital Signature Algorithm, ML-DSA)•무상태 해시 기반 디지털 서명 알고리즘(Stateless Hash-Based Digital Signature Algorithm, SLH-DSA)**
- 기존 공개키 암호와 다른 **큰 키•서명•연산 특성**
- 자산 목록•하이브리드 운용•암호 민첩성 기반 **점진적 전환**
#### 한줄 요약

- 알고리즘뿐 아니라 시스템 전체의 호환성과 배포 절차까지 검증한다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **키 캡슐화 메커니즘(KEM)**: 공유 비밀키를 직접 전송하지 않고 공개키로 캡슐화하고 개인키로 복원하는 키 설정 방식이다.
- **양자내성 전자서명**: 양자 공격을 고려한 수학적 난제에 기반해 메시지의 진위와 무결성을 검증하는 방식이다.
- **암호 자산 목록(Crypto Inventory)**: 알고리즘•키•인증서•프로토콜•라이브러리의 위치와 의존성을 추적한 전환 기준선이다.
- **하이브리드 운영**: 기존 암호와 양자내성 암호를 함께 적용해 전환기 상호운용성과 방어 심도를 확보하는 방식이다.
- **암호 민첩성(Crypto Agility)**: 알고리즘과 키 규격을 정책에 따라 발견•교체•검증할 수 있는 설계 역량이다.

</details>

**키 캡슐화 메커니즘(Key-Encapsulation Mechanism, KEM)** 을 적용할 암호 자산과 **하드웨어 보안 모듈(Hardware Security Module, HSM)** 호환성을 목록화한다.

```mermaid
block-beta
  columns 3
  N0["Crypto Inventory"]
  N1["Algorithm Profile"]
  N2["Hybrid 운영"]
  N3["Governance"]
  N0 --- N1 --- N2
  N2 --- N3
```

| 구성요소 | 책임 |
|:---|:---|
| Crypto Inventory | **암호 자산•라이브러리•HSM** 식별 |
| Algorithm Profile | **표준 알고리즘•파라미터** 선택 |
| Hybrid 운영 | 기존 암호 병행과 **downgrade 방지** |
| Governance | **상호운용성•성능•수명주기** 관리 |

#### 한줄 요약

- 중요 자료부터 새 자물쇠를 맞추고 단계적으로 교체함

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **하이브리드 전환**: 기존 암호와 양자내성암호를 함께 사용하여 이행 중 호환성과 보안을 유지하는 방식이다.

</details>

```mermaid
sequenceDiagram
  participant I as 암호 자산 목록
  participant P as PQC 알고리즘 정책
  participant H as 하이브리드 암호
  participant S as 프로토콜•HSM•인증서
  participant G as 전환 거버넌스
  I->>P: 1. 자산•위험 우선순위
  P->>H: 2. 표준 알고리즘 선택
  H->>S: 3. 병행 구성•통합
  S->>G: 4. 상호운용•성능 검증
  G-->>I: 5. 기존 암호 폐기
```

**동작 원리**

- **1. 자산•위험 우선순위**: 데이터 수명•노출도•암호 위치 평가
- **2. 표준 알고리즘 선택**: 용도•파라미터•구현 적합성 결정
- **3. 병행 구성•통합**: 기존 암호와 **양자내성암호(Post-Quantum Cryptography, PQC) 키 캡슐화 메커니즘(Key-Encapsulation Mechanism, KEM)** •서명 결합
- **4. 상호운용•성능 검증**: 프로토콜•**하드웨어 보안 모듈(Hardware Security Module, HSM)** •인증서 크기와 지연 시험
- **5. 기존 암호 폐기**: 단계 배포 후 downgrade 경로 제거

#### 한줄 요약

- 중요 보안 자산부터 문제없는 것을 확인하고 옛 방식 폐기함

## Ⅴ. 종류 및 비교

<details>
<summary>핵심 용어</summary>

- **모듈 격자 기반 디지털 서명 알고리즘(ML-DSA)**: 모듈 격자 문제를 기반으로 메시지의 출처와 무결성을 증명하는 표준 양자내성 전자서명 방식이다.

</details>

| 판단 기준 | 고전 공개키(Classical Public Key, Classical PK) | 양자내성암호(Post-Quantum Cryptography, PQC) | 양자 키 분배(Quantum Key Distribution, QKD) |
|:---|:---|:---|:---|
| 적용 기준 | 기존 **키 설정•전자서명** | 양자내성 **키 설정•전자서명** | 전용망 **대칭키 분배** |
| 핵심 특징 | **인수분해•이산로그 난제** | **격자•해시 난제** | **양자 측정 교란** 기반 |
| 한계 | 대규모 **양자 공격 취약** | **큰 키•서명•전환 호환성** | **전용 광장비•거리 제약** |

#### 한줄 요약

- 양자내성암호는 수학 알고리즘 교체이고 양자 키 분배는 전용 통신 장비 도입이다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **암호 민첩성**: 알고리즘•키•라이브러리를 서비스 중단과 대규모 재설계 없이 교체할 수 있는 능력이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 긴 데이터 수명의 **선취 후 해독** 위험 | **암호 자산 목록•우선순위 전환** | **장기 기밀성** 보호 |
| **큰 키•서명**으로 프로토콜 초과 | **최대 전송 단위(Maximum Transmission Unit, MTU)•인증서•하드웨어 보안 모듈(Hardware Security Module, HSM) 성능 시험** | **운영 호환성** 확보 |
| 하이브리드 **downgrade** | **조합 협상 고정•로그•폐기 기준** | 전환기 **보안 약화 방지** |

#### 한줄 요약

- 금융 게이트웨이는 표준 **양자내성암호(Post-Quantum Cryptography, PQC) 키 캡슐화 메커니즘(Key-Encapsulation Mechanism, KEM)** 을 기존 키 합의와 병행해 단말 호환성•핸드셰이크 크기•지연•실패 복구를 검증한 뒤 단계 배포한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **선취 후 복호화(HNDL)**: 현재 수집한 암호문을 보관했다가 미래의 양자컴퓨터로 복호화하려는 선취 위협이다.

</details>

- **선취 후 복호화(Harvest Now, Decrypt Later, HNDL)** 위험이 큰 자산부터 **모듈 격자 기반 키 캡슐화 메커니즘(Module-Lattice-Based Key-Encapsulation Mechanism, ML-KEM)•모듈 격자 기반 디지털 서명 알고리즘(Module-Lattice-Based Digital Signature Algorithm, ML-DSA)** 으로 **단계 전환**

#### 한줄 요약

- 표준 알고리즘을 선택하고 프로토콜•장비•인증서•폐기 절차를 함께 검증한다.
