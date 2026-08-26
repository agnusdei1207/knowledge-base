---
sidebar:
  order: 16
  label: "016. 영지식 증명 ZKP"
  badge:
    text: "기출 · 50%"
    variant: note
title: "정보 비노출 자격 검증 프로토콜 : 영지식 증명"
date: "2026-08-26T14:31:31+09:00"
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

- 정의/개념: Witness 없이 **제약식 만족 사실만 증명하는 프라이버시 기술**
- 배경/필요성: 신원 검증의 원문 제출로 **개인정보 과다 노출 위험** 발생

#### 한줄 요약
- 원본 비밀의 노출 없이 자격이나 연산 결과가 참임을 수학적으로 증명한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **Completeness (완전성)**: 명제가 참이면 정직한 증명자는 정직한 검증자를 반드시 납득시킬 수 있음.
- **Soundness (건전성)**: 명제가 거짓이면 부정직한 증명자가 검증자를 속일 수 있는 확률이 0에 수렴함.
- **Zero-Knowledge (영지식성)**: 명제가 참이라는 사실 외에는 비밀 정보에 대한 어떠한 추가 지식도 검증자에게 노출되지 않음.

</details>

- **3대 속성**: 완전성·건전성·영지식성 보장
- **zk-SNARKs**: Fiat-Shamir 기반 소형 비대화형 증명
- **최소 정보 공개**: DID 자격의 임계치 충족 여부만 증명

#### 한줄 요약
- 3대 속성(완전성/건전성/영지식성) 보증, 256B 초경량 비대화형 증명, DID 최소 공개를 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **CRS (Common Reference String)**: zk-SNARKs에서 증명자와 검증자가 공유하는 공개 암호 파라미터(증명 키 $pk$ 및 검증 키 $vk$).

</details>

```text
[영지식 증명 정적 구성]
|-- 산술 회로
|-- 비밀 증거
|-- 증명자
|-- 검증자
`-- 신뢰 설정
```

선의 의미: 산술 회로로부터 생성된 키를 바탕으로 증명자가 비밀 증거를 주입해 증명($\pi$)을 생성하고 검증자가 비밀 노출 없이 수식 일치 여부를 판정하는 구조

| 구성요소 | 핵심 엔지니어링 책임 | 주요 특징 |
|:---|:---|:---|
| 산술 회로 | **R1CS·QAP 제약식 변환** | Circom / Halo2 |
| 비밀 증거 | **로컬 비공개 원본** | Private Input |
| 증명자 | **압축 증명 생성** | Prover Engine |
| 검증자 | **공개 입력·증명 판정** | Verifier Contract |
| 신뢰 설정 | **CRS 생성·Toxic Waste 소거** | Powers of Tau |

#### 한줄 요약
- 산술 회로, 비밀 증거(Witness), 증명자(Prover), 검증자(Verifier), 신뢰 설정(CRS)이 결합한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Fiat-Shamir Heuristic (피아트-샤미르 변환)**: 대화형 영지식 증명의 무작위 챌린지를 해시 함수로 대체하여 단 1회의 전송으로 검증을 완료하는 비대화형 변환 기법.

</details>

```text
자격 증명 요청
    |
1. 회로 컴파일·키 배포
    |
2. 로컬 Witness 주입
    |
3. 비대화형 증명 계산
    |
4. 공개 입력·증명 전송
    |
5. 페어링 검증
    |
참·거짓 결과
```

- 1. 회로 컴파일·키 배포
- 2. 로컬 Witness 주입
- 3. 비대화형 증명 계산
- 4. 공개 입력·증명 전송
- 5. 페어링 검증

#### 한줄 요약
- 회로 컴파일 → 로컬 Witness 주입 → 비대화형 증명 생성 → 공개 입력/증명 전송 → 페어링 검증 판정 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **zk-SNARKs** vs **zk-STARKs** vs **Bulletproofs**.

</details>

| 비교 항목 | zk-SNARKs (Groth16 / Plonk) | zk-STARKs (StarkNet 표준) | Bulletproofs (범위 증명 전용) |
|:---|:---|:---|:---|
| 수학적 기반 | **KZG 페어링** | **해시·FRI** | **IPA** |
| 신뢰 설정 | **필수** | **불필요** | **불필요** |
| 증명 크기 | **128~256B** | **40~100KB** | 1~2KB |
| 검증 속도 | **2~5ms** | 10~20ms | 선형 증가 |
| 양자 공격 저항성 | **취약** | **해시 기반 저항** | 취약 |
| 주요 적용 영역 | **ZK-Rollup·Zcash** | **Starknet·L2** | **범위 증명** |

#### 한줄 요약
- zk-SNARKs는 초소형 크기와 초고속 검증 표준, zk-STARKs는 신뢰 설정이 없고 양자 안전한 차세대 표준이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Toxic Waste (독성 폐기물)**: zk-SNARKs 신뢰 설정 시 생성되는 비밀 난수로, 유출 시 공격자가 가짜 증명을 무한 위조할 수 있는 결함.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| Toxic Waste 유출로 증명 위조 | **MPC 세레모니·STARK 전환** | 위조 위험 제거 |
| 증명의 세션 간 Replay | **Nonce·시간·수신자 바인딩** | 컨텍스트 고정 |
| 위조 데이터를 Witness로 주입 | **발급기관 서명 검증 회로** | 데이터 진본성 확보 |
| Prover의 CPU·메모리 부담 | **GPU·FPGA MSM 가속** | 증명 시간 단축 |

#### 한줄 요약
- MPC 세레모니로 Toxic Waste를 소거하고, Nonce 바인딩으로 Replay를 막으며, 서명 검증 회로로 데이터 진본성을 보증한다.

## Ⅶ. 결론

- 소형·고속 검증은 **zk-SNARKs**, 투명·양자 저항은 **zk-STARKs** 선택

#### 한줄 요약
- 영지식 증명은 완전성/건전성/영지식성 3대 속성과 비대화형 SNARK/STARK 기술을 통해 데이터 노출 없는 무결점 자격 검증을 실현하는 암호 기술이다.
