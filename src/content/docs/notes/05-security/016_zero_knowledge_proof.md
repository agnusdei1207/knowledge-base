---
sidebar:
  order: 16
  label: "016. 영지식 증명 ZKP"
  badge:
    text: "기출 · 50%"
    variant: note
title: "정보 비노출 자격 검증 프로토콜 : 영지식 증명"
date: "2026-08-25T13:00:00+09:00"
tags:
  - "notes-security"
weight: 16
extra:
  question_no: "16"
  source_status: "기출"
  source_history: "132회"
  priority: 50
  priority_note: "3대 기본 속성(완전성, 건전성, 영지식성), zk-SNARKs vs zk-STARKs, Trusted Setup 및 DID/블록체인"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **ZKP (Zero-Knowledge Proof, 영지식 증명)**: 비밀 정보를 일절 노출하지 않고 그 정보가 참이라는 사실만을 검증자에게 수학적으로 증명하는 기술.
- **Witness (비밀 증거)**: 증명자가 검증 회로에 주입하는 비공개 원본 데이터(예: 주민등록번호, 소득액, 개인키).

</details>

- 정의/개념: 비공개 입력값(Witness)을 외부에 일절 노출하지 않고 **연산 제약식을 만족한다는 사실만을 수학적으로 증명하는 프라이버시 보존형 신뢰 기술**
- 배경/필요성: 신원/자격 증명 시의 **원문 데이터 평문 노출에 따른 개인정보 침해 위험, 과다 정보 수집 및 정보 비노출 검증 불가**

#### 한줄 요약
- 원본 비밀의 노출 없이 자격이나 연산 결과가 참임을 수학적으로 증명한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Completeness (완전성)**: 명제가 참이면 정직한 증명자는 정직한 검증자를 반드시 납득시킬 수 있음.
- **Soundness (건전성)**: 명제가 거짓이면 부정직한 증명자가 검증자를 속일 수 있는 확률이 0에 수렴함.
- **Zero-Knowledge (영지식성)**: 명제가 참이라는 사실 외에는 비밀 정보에 대한 어떠한 추가 지식도 검증자에게 노출되지 않음.

</details>

- **3대 암호학적 수학 속성 만족**: 완전성(Completeness), **건전성(Soundness), 영지식성(Zero-Knowledge)의 엄격한 보증**
- **비대화형 증명 압축(zk-SNARKs)**: 피아트-샤미르 변환을 통해 **단 1회의 256바이트 초소형 증명값($\pi$)으로 수 밀리초 내 검증 완결**
- **데이터 주권 및 최소 정보 공개(DID 연계)**: 나이, 소득 등 **임계치 만족 여부(예: 성인 여부 참/거짓)만 선별 증명 가능**

#### 한줄 요약
- 3대 속성(완전성/건전성/영지식성) 보증, 256B 초경량 비대화형 증명, DID 최소 공개를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CRS (Common Reference String)**: zk-SNARKs에서 증명자와 검증자가 공유하는 공개 암호 파라미터(증명 키 $pk$ 및 검증 키 $vk$).

</details>

```text
[영지식 증명 생성 및 검증 아키텍처]
|-- Arithmetic Circuit (검증 조건 f(x, w) = 1 -> R1CS / QAP 다항식 컴파일)
`-- Trusted Setup / CRS (공개 파라미터 생성: Prover Key pk & Verifier Key vk)
`-- Prover (증명자: 비밀 입력 w + 공개 입력 x -> 산술 회로 -> 증명값 pi 생성)
`-- Verifier (검증자: 공개 입력 x + vk + pi 수신 -> 타원곡선 페어링 연산 -> Pass/Fail 판정)
```

선의 의미: 산술 회로로부터 생성된 키를 바탕으로 증명자가 비밀 증거를 주입해 증명($\pi$)을 생성하고 검증자가 비밀 노출 없이 수식 일치 여부를 판정하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| **산술 회로 (Circuit)** | 검증 조건을 **R1CS/QAP 다항식 행렬 제약식으로 컴파일 변환** | Circom / Halo2 |
| **비밀 증거 (Witness)**| 로컬 기기에만 격리 보관되는 **비공개 원본 데이터(비밀키, 주민번호)** | Private Input |
| **증명자 (Prover)** | $pk$, 공개 입력 $x$, Witness $w$를 결합하여 **압축된 영지식 증명($\pi$) 생성** | Prover Engine |
| **검증자 (Verifier)** | $vk$, 공개 입력 $x$, 증명 $\pi$를 입력받아 **$O(1)$ 시간 내에 진위 판정** | Verifier Contract |
| **신뢰 설정 (Trusted Setup)**| MPC(다자간 연산)를 통해 **CRS를 생성하고 독성 폐기물(Toxic Waste) 소거** | Powers of Tau |

#### 한줄 요약
- 산술 회로, 비밀 증거(Witness), 증명자(Prover), 검증자(Verifier), 신뢰 설정(CRS)이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Fiat-Shamir Heuristic (피아트-샤미르 변환)**: 대화형 영지식 증명의 무작위 챌린지를 해시 함수로 대체하여 단 1회의 전송으로 검증을 완료하는 비대화형 변환 기법.

</details>

```text
회로 컴파일, Witness 주입, 비대화형 증명 생성 및 페어링 검증 파이프라인
        │
   1. [회로 컴파일 및 키 배포] 산술 회로를 컴파일하고 MPC 다자간 연산으로 증명 키($pk$)와 검증 키($vk$) 배포
        │
   2. [로컬 Witness 주입] 사용자가 로컬 기기에서 비밀 증거($w$: 실제 소득)를 회로에 주입
        │
   3. [비대화형 증명 계산] Prover 엔진이 피아트-샤미르 변환을 적용하여 256바이트 증명값($\pi$) 생성
        │
   4. [공개 조건 및 증명 전송] 검증자 서버로 [공개 입력 $x$ + 증명값 $\pi$] 전송 (원본 $w$ 미전송)
        │
   ▼
5. [타원곡선 페어링 검증] 검증자가 $vk$를 사용하여 타원곡선 페어링 연산 수행 ➔ 3ms 내 참/거짓 판정
```

#### 한줄 요약
- 회로 컴파일 → 로컬 Witness 주입 → 비대화형 증명 생성 → 공개 입력/증명 전송 → 페어링 검증 판정 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **zk-SNARKs** vs **zk-STARKs** vs **Bulletproofs**.

</details>

| 비교 항목 | zk-SNARKs (Groth16 / Plonk) | zk-STARKs (StarkNet 표준) | Bulletproofs (범위 증명 전용) |
|:---|:---|:---|:---|
| **수학적 기반** | **타원곡선 페어링 (KZG 다항식)** | **해시 함수 + FRI (Reed-Solomon)** | **타원곡선 이산대수 (IPA)** |
| **신뢰 설정 (Trusted Setup)**| **필수 (MPC 세레모니 필요)** | **불필요 (완전 투명성: Transparent)**| **불필요 (Transparent)** |
| **증명 크기 (Proof Size)** | **초경량 ($\approx 128 \sim 256\text{ Bytes}$)**| **큼 ($\approx 40 \sim 100\text{ KB}$)** | 중간 ($\approx 1 \sim 2\text{ KB}$) |
| **검증 속도** | **극도로 빠름 ($\approx 2 \sim 5\text{ms}$)** | 빠름 ($\approx 10 \sim 20\text{ms}$) | 느림 (연산 수에 선형 비례) |
| **양자 공격 저항성** | **취약 (타원곡선 이산대수 기반)** | **영구적 안전 (해시 함수 기반 PQC)**| 취약 |
| **주요 적용 영역** | **ZK-Rollup, 프라이버시 코인(Zcash)** | **대규모 블록체인(Starknet), L2 롤업**| **모네로(Monero), 금융 잔액 범위 증명**|

#### 한줄 요약
- zk-SNARKs는 초소형 크기와 초고속 검증 표준, zk-STARKs는 신뢰 설정이 없고 양자 안전한 차세대 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Toxic Waste (독성 폐기물)**: zk-SNARKs 신뢰 설정 시 생성되는 비밀 난수로, 유출 시 공격자가 가짜 증명을 무한 위조할 수 있는 결함.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| zk-SNARKs 신뢰 설정 난수(Toxic Waste) 유출로 인한 **가짜 증명 무한 위조 사고** | **수천 명이 참여하는 `MPC 세레모니(Powers of Tau) 적용 또는 STARK 전환`** | 1명만 정직해도 비밀 복구 불가 보증 및 위조 원천 차단 |
| 정상 증명값($\pi$)을 가로채 다른 세션에 재전송하는 **Replay 공격** | **공개 입력($x$)에 `세션 Nonce, 타임스탬프, 수신자 식별자 바인딩`** 강제 | 증명의 유효 컨텍스트 고정 및 재전송 공격 100% 차단 |
| 조작된 가짜 신분증 데이터를 Witness로 주입하여 **합법적 자격을 획득하는 위장** | 산술 회로 내부에서 **`공인 기관의 전자서명 검증 로직을 제약식으로 결합`** | 위조 데이터 투입 방어 및 증명 진본성 확보 |
| 증명 생성(Prover) 시 극심한 CPU/메모리 자원 소모로 인한 클라이언트 랙 | **`GPU/FPGA 기반 MSM(Multi-Scalar Multiplication) 하드웨어 가속`** | 모바일 증명 생성 시간 1초 이내 단축 및 사용자 경험 개선 |

#### 한줄 요약
- MPC 세레모니로 Toxic Waste를 소거하고, Nonce 바인딩으로 Replay를 막으며, 서명 검증 회로로 데이터 진본성을 보증한다.

## Ⅶ. 결론

- 데이터 활용과 개인정보 보호라는 상충된 요구를 수학적으로 완벽히 해결하는 **영지식 증명(ZKP) 아키텍처는 차세대 분산 신원 증명(DID), 블록체인 ZK-Rollup, AI 모델 소유권 검증의 핵심 기반 기술**이며, 실무 구현 시 **zk-SNARKs와 zk-STARKs의 요구조건별 최적 선정, MPC 기반 안전한 신뢰 설정(Trusted Setup) 거버넌스, 컨텍스트 바인딩 및 서명 검증 회로 결합**을 통합 구현하여 완결성 높은 프라이버시 보존형 신뢰 인프라 완성

#### 한줄 요약
- 영지식 증명은 완전성/건전성/영지식성 3대 속성과 비대화형 SNARK/STARK 기술을 통해 데이터 노출 없는 무결점 자격 검증을 실현하는 암호 기술이다.