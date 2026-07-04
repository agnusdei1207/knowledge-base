---
title: "영지식 증명 ZKP (Zero-Knowledge Proof)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-security"
weight: 22
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: ZKP는 **암호 프로토콜**의 하나로, 증명자(Prover)가 비밀 자체를 공개하지 않고 어떤 명제가 참임을 검증자(Verifier)에게 증명하는 기술임.
- **왜 필요한가**: 신원·자격·거래 유효성을 확인할 때 주민번호·잔액·비밀키 같은 원본을 제출하면 유출 피해가 커짐. ZKP는 원본 노출 없이 "참/거짓"만 전달하여 개인정보 최소수집 원칙과 내부자 위협 문제를 동시에 해결함.
- **핵심 직관**: 금고 비밀번호를 말하지 않고도 금고를 열 수 있음을 상대에게 납득시키는 방식임.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 암호 프로토콜 (상위 키워드) | 비밀 보호를 위해 당사자 간 교환하는 메시지 절차 | 금고를 열고 닫는 규칙서 |
| Prover | 비밀을 알고 있음을 증명하는 측 | 금고 비번을 아는 사람 |
| Verifier | proof를 검증하는 측 | 금고가 열렸는지 확인하는 사람 |
| Witness | 명제를 참으로 만드는 비밀 입력값 | 금고 비밀번호 자체 |
| Statement / Public Input | 증명할 명제와 공개 입력값 | "이 사람은 19세 이상이다" |
| Proof | Prover가 생성하는 증명 데이터 | 금고 열림을 보여주는 영상 |
| Completeness (완전성) | 참인 명제는 반드시 검증을 통과함 | 진짜 비번이면 항상 열림 |
| Soundness (건전성) | 거짓 명제는 검증을 통과할 수 없음(확률 무시) | 가짜 비번은 절대 안 열림 |
| Zero-knowledge (영지식성) | 검증 과정에서 witness 외 정보가 유출되지 않음 | 비번 자체는 전혀 안 보임 |
| Circuit | 명제를 산술·논리 회로로 변환한 것 | 계산 순서를 회로도로 표현 |
| zk-SNARK | Succinct Non-interactive Argument of Knowledge — 짧은 proof, 비대화형 | 작은 증명서, trusted setup 필요 |
| zk-STARK | Scalable Transparent Argument of Knowledge — 투명 setup, 해시 기반 | 큰 증명서, setup 신뢰 불필요 |
| Trusted Setup | SNARK에서 증명·검증 키를 생성하는 초기 의식(ceremony) | 금고 틀을 만드는 공동 작업 |
| Toxic Waste | trusted setup에서 생성되는 비밀값 — 유출 시 위조 proof 생성 가능 | 금고 틀의 마스터키 조각 |

## 깊이 이해
- **배경·문제의식**: 인증·감사는 보통 원본 데이터 제출을 요구하지만, 원본 제출은 개인정보 최소수집 원칙, 내부자 위협, 로그 유출과 충돌함. 동형 암호(021)가 "암호문 상태에서 계산"이라면, ZKP는 "비밀을 공개하지 않고 명제의 참·거짓만 증명"하는 접근으로 목적이 다름.
- **작동 원리**: (1) 증명할 조건(예: "잔액 ≥ 100만 원")을 산술 회로(circuit)로 변환함. (2) Prover가 비밀 witness(실제 잔액)와 public input(기준 금액)을 회로에 입력해 proof를 생성함. (3) Verifier가 proof와 public input만으로 명제 참 여부를 검증함 — witness는 전달되지 않음. 핵심 3성질(completeness·soundness·zero-knowledge)이 모두 만족해야 유효한 ZKP임.
- **zk-SNARK vs zk-STARK**: SNARK는 proof 크기가 수백 byte~수 KB로 작고 검증이 빠르지만, 타원곡선 기반이라 trusted setup이 필요하고 양자 취약성이 있음. STARK는 해시 기반으로 transparent setup(신뢰 불필요)이고 양자내성이 있지만, proof 크기가 수십~수백 KB로 큼.
- **비유**: 미로의 정답 길을 아는 사람이 검증자가 지정하는 출구로 매번 정확히 나옴 — 100번 연속 성공하면 "이 사람은 정답 길을 안다"고 납득하지만, 정답 길 자체는 공개되지 않음.
- **구체 예시**: 만 19세 이상 여부를 증명할 때 생년월일 전체를 제공하지 않고 "19세 이상" proof만 제출함. 블록체인에서는 Zcash(zk-SNARK)가 거래 금액·송수신자를 숨기면서 이중지불 없음을 증명함. zk-rollup은 수천 건의 거래를 하나의 proof로 압축해 온체인 검증 비용을 줄임.
- **흔한 오해·주의점**: (1) ZKP는 거짓 명제를 참으로 만드는 기술이 아님 — soundness가 이를 보장함. (2) 회로 설계가 틀리면(조건 누락·범위 오류) proof가 통과해도 시스템 보안이 깨짐 — circuit audit이 필수임. (3) trusted setup의 toxic waste가 유출되면 위조 proof 생성이 가능하므로 multi-party ceremony와 transcript 공개가 필요함.

## 연결 개념
- **DID·VC(110~112)**: 선택적 공개(selective disclosure)에 ZKP를 적용해 자격 검증 시 원본 노출을 최소화
- **동형 암호(021)**: 암호문 연산 기반 PET — ZKP는 증명, HE는 연산으로 목적이 다름
- **MPC(023)**: trusted setup의 multi-party ceremony, 분산 witness 생성 등에서 연결

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ZKP는 witness를 공개하지 않고 명제의 참 여부만 검증하게 하는 증명 체계임.
> 2. **가치**: 인증·자격·거래 검증에서 개인정보·비밀키·거래 세부값 노출을 최소화함.
> 3. **판단 포인트**: 3성질(completeness·soundness·zero-knowledge)·trusted setup·proof size·verification time·회로 취약점을 함께 평가해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ZKP 3성질 이해 | completeness·soundness·zero-knowledge 정의 | "비밀을 숨긴다" 한 줄로 끝내고 3성질 누락 |
| 방식 비교 | zk-SNARK·zk-STARK·Bulletproof | trusted setup·proof size·검증 비용 비교 누락 |
| 적용 설계 | Prover·Verifier·public input·witness·circuit | 회로 버그·키 ceremony 리스크 누락 |

> 요약: ZKP 답안은 3성질과 증명 구조를 먼저 고정하고, 방식별 비용·신뢰 경계를 비교해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 비밀 입력(witness)을 공개하지 않고 명제의 참 여부만 증명하는 암호 프로토콜임.
- 배경: 디지털 신원·블록체인·금융 검증에서 원본 데이터 제출은 유출·내부자 위협·최소수집 원칙과 충돌함.
- 필요성: ZKP는 witness를 숨기고 proof와 public input만 제공해 최소공개·검증가능성·감사 대응 근거를 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Statement/Public Input -> Circuit/Constraint 변환 -> Prover
Witness(비밀) -> Prover -> Proof 생성 -> Verifier -> Accept/Reject
  / Setup -> Proving Key / Verification Key (SNARK 시)
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Statement | 증명할 명제(공개 입력) | "잔액 ≥ 100만 원", 거래 유효성 등 |
| Witness | 명제를 참으로 만드는 비밀 값 | 생년월일, 비밀키, 원장 세부값 |
| Circuit | 명제를 산술·논리 회로로 변환한 것 | R1CS, Plonk, AIR 등 표현 방식 |
| Prover/Proof | witness 기반 증명 생성 | proving time·proof size 관리 |
| Verifier | proof와 public input으로 검증 | verification time·soundness error 확인 |

> 요약: ZKP는 공개 명제와 비밀 witness를 분리하고, proof를 통해 검증자에게 참·거짓만 전달하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
명제 정의 -> 산술 회로 변환 -> Witness 입력
  -> Proof 생성 -> Public Input 전달
  -> Verifier 검증 -> Accept/Reject -> 감사로그
```

1. 회로 변환: 검증 명제를 산술 회로(R1CS/Plonk)·constraint로 변환하고 회로 테스트 coverage 100%를 확보함.
2. Witness 분리: witness(비밀)와 public input(공개)을 분리하고, 비밀 필드가 로그에 노출되지 않도록 통제함.
3. Proof 생성·검증: Prover가 witness를 이용해 proof를 생성하고, Verifier가 proof·public input만으로 검증함 — soundness error 2^-80 이하를 보장함.
4. 감사 기록: 결과(accept/reject)·키 버전·proof hash를 감사로그에 남기고, trusted setup ceremony transcript를 보관함.

> 요약: ZKP 품질은 proof 알고리즘보다 명제 회로의 정확성과 검증 입력의 무결성에 좌우됨.

---

## Ⅳ. 특징

- 최소 공개: witness를 전혀 공개하지 않고 명제의 참·거짓만 전달해 개인정보 노출을 원천 차단함.
- SNARK vs STARK 트레이드오프: SNARK는 proof 수백 byte·검증 ms 단위이나 trusted setup과 양자 취약성이 있고, STARK는 transparent setup·양자내성이나 proof 수십~수백 KB로 큼.
- 회로 의존성: 모든 검증 조건을 산술 회로로 변환해야 하며, 회로 설계 오류(조건 누락·범위 오류)는 proof 통과 시에도 보안을 깨뜨림.
- 비대화형 전환: Fiat-Shamir 변환으로 대화형 프로토콜을 비대화형으로 전환해 블록체인·API 검증에 적용 가능함.
- 결과 보안: proof 제출 시점·주소 등 메타데이터에서 Prover 정체가 추론될 수 있어 batching·relayer 등 추가 통제가 필요함.

---

## Ⅴ. 심화 비교 및 적용 판단

zk-SNARK와 zk-STARK를 신뢰 설정·크기·검증 비용·양자내성 축으로 비교함.

| 구분 | zk-SNARK | zk-STARK | 선택 기준 |
|:---|:---|:---|:---|
| 신뢰 설정 | trusted setup 필요(multi-party ceremony) | transparent setup(해시 기반) | ceremony 운영 가능성 |
| Proof 크기 | 수백 byte~수 KB | 수십~수백 KB | 온체인 gas·네트워크 비용 |
| 검증 비용 | ms 단위(pairing 연산) | proof 크기에 비례해 증가 | p95 검증 시간 요구 |
| 양자내성 | 타원곡선 의존 — 양자 취약 | 해시·FRI 기반 — 양자내성 | PQC 전환 요구 여부 |

> 요약: 온체인·모바일은 작은 proof의 SNARK를, setup 신뢰 최소화·양자내성이 요구되는 환경은 STARK를 선택함.

**리스크·대응:**
- 회로 오류: 조건 누락·범위 검증 실패 → circuit audit·property test·음성 테스트 통과율 100% (지표: audit 결함 0건)
- Trusted setup 노출: toxic waste 유출 시 위조 proof 생성 가능 → multi-party ceremony·transcript 공개·참여자 5인 이상 (지표: ceremony 검증 로그)
- 메타데이터 노출: proof 제출 시점·주소 추적 → batching·relayer·unlinkable identifier (지표: 상관분석 탐지 건수)

**도입 후 점검 지표:**
- 보안성: soundness error 2^-80 이하·회로 결함 0건 — 형식검증·audit report
- 성능: proof size·proving time·verification p95 — 벤치마크·온체인 gas 측정
- 프라이버시: witness 로그 노출 0건·linkability 점검 — DLP·privacy test

---

## Ⅵ. 실무 적용 및 결론

**적용 방안:**
1. 검증 요구를 "성인 여부"·"잔액 범위"·"거래 합계 일치"처럼 명제로 고정하고 public input과 witness를 분리함.
2. 모바일·온체인은 proof size가 작은 zk-SNARK를, setup 신뢰 최소화가 요구되는 감사 환경은 zk-STARK를 우선 검토함.
3. Circuit audit·multi-party ceremony·proving/verification p95·witness 로그 DLP를 배포 전 승인 기준으로 설정함.

**결론:**
- 기술사 판단: 원본 제출을 줄여야 하는 신원·거래 검증은 ZKP를, 단순 내부 시스템 조회는 RBAC·토큰화를 우선 적용함.
- 향후 방향: DID·VC 선택적 공개, zk-rollup 확장성, 개인정보 최소공개 서비스에서 회로 감사와 표준화된 proof 검증 API가 핵심이 될 것임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ZKP를 설명하시오" | 3성질·Prover/Verifier·회로 변환 흐름 | SNARK/STARK 비교·적용 사례 |
| 요구사항 명시형 | "비교하시오", "설계하시오" | 회로·setup·검증 API 설계 | proof size·trusted setup·privacy risk 선택 기준 |

> 요약: 설명형은 3성질과 증명 구조를, 설계형은 회로·키 ceremony·검증 지표를 중심으로 전개함.
