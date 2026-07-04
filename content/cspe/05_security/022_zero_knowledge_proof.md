---
title: "영지식 증명 ZKP (Zero-Knowledge Proof)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 22
---

# 📖 【암기용】 개념 완전 이해

> 목적: 영지식 증명을 처음 봐도 완전하게 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 비밀 자체를 공개하지 않고 어떤 명제가 참임을 증명하는 암호 프로토콜
- **왜 필요한가**: 신원·자격·거래 유효성을 확인할 때 주민번호, 잔액, 비밀키 같은 원본을 노출하면 유출 피해가 커진다. ZKP는 검증에 필요한 참·거짓만 전달한다.
- **핵심 직관**: 금고 비밀번호를 말하지 않고도 금고를 열 수 있음을 상대에게 납득시키는 방식이다.

## 깊이 이해
- **배경·문제의식**: 인증과 감사는 보통 원본 데이터 제출을 요구한다. 그러나 원본 제출은 개인정보 최소수집 원칙, 내부자 위협, 로그 유출과 충돌한다.
- **작동 원리**: 증명자(Prover)는 비밀 witness를 이용해 proof를 만들고, 검증자(Verifier)는 공개 입력과 proof만으로 명제 참 여부를 확인한다. 핵심 성질은 완전성, 건전성, 영지식성이다.
- **비유**: 미로의 정답 길을 아는 사람이 출구 중 하나로 매번 정확히 나와 지식을 입증하지만, 길 자체는 공개하지 않는 모습이다.
- **구체 예시**: 만 19세 이상 여부를 증명할 때 생년월일 전체를 제공하지 않고 "19세 이상" proof만 제출한다. zk-SNARK는 proof 크기가 수백 byte 수준일 수 있고, zk-STARK는 trusted setup 없이 투명성을 제공한다.
- **흔한 오해·주의점**: ZKP는 거짓 명제를 참으로 만드는 기술이 아니다. 회로 설계가 틀리거나 trusted setup 독성 폐기물이 유출되면 proof가 통과해도 시스템 보안이 깨질 수 있다.

## 연결 개념
- DID·VC — 선택적 공개와 자격 검증에 ZKP 적용
- 블록체인 — 거래 유효성 검증과 프라이버시 보호에 zk-SNARK/STARK 활용
- MPC — trusted setup, witness 생성, 분산 증명 생성과 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ZKP는 witness를 공개하지 않고 명제 참 여부만 검증하게 하는 증명 체계임.
> 2. **가치**: 인증·자격·거래 검증에서 개인정보·비밀키·거래 세부값 노출을 최소화함.
> 3. **판단 포인트**: completeness, soundness, zero-knowledge, trusted setup, proof size, verification time, 회로 취약점을 함께 봐야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| ZKP 성질 이해 | 완전성, 건전성, 영지식성 | "비밀을 숨김"만 쓰고 3성질 누락 금지 |
| 방식 비교 | zk-SNARK, zk-STARK, Bulletproof | trusted setup, proof size, 검증 비용 비교 누락 금지 |
| 적용 설계 | Prover, Verifier, public input, witness, circuit | 회로 버그·키 ceremony 리스크 누락 금지 |

> 요약: ZKP 답안은 3성질과 증명 구조를 먼저 고정하고, 방식별 비용과 신뢰 경계를 비교해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 비밀값 비공개 증명
- 배경: 디지털 신원·블록체인·금융 검증은 원본 데이터 제출을 줄이면서도 조건 충족 여부와 거래 정합성을 검증해야 함.
- 필요성: ZKP는 witness를 숨기고 proof와 public input만 제공해 최소공개, 검증가능성, 감사 대응 근거를 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
Statement/Public Input -> Circuit/Constraint -> Prover
Witness/Secret -> Prover -> Proof -> Verifier -> Accept/Reject
/ Setup -> Proving Key / Verification Key
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Statement | 증명할 명제 | 나이 조건, 잔액 범위, 거래 유효성 |
| Witness | 명제를 참으로 만드는 비밀 | 생년월일, 비밀키, 원장 세부값 |
| Prover/Proof | witness 기반 증명 생성 | proving time, proof size 관리 |
| Verifier | proof 검증 | verification time, public input 확인 |

> 요약: ZKP는 공개 명제와 비밀 witness를 분리하고 proof를 통해 검증자에게 참·거짓만 전달하는 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
명제 정의 -> 회로 변환 -> witness 입력 -> proof 생성
-> public input 전달 -> verifier 검증 -> accept/reject -> 감사로그
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 검증 명제를 산술 회로·constraint로 변환 | 회로 테스트 coverage 100% |
| 2 | witness와 public input 분리 | 비밀 필드 로그 노출 0건 |
| 3 | Prover가 proof 생성 | proving time, proof size |
| 4 | Verifier가 proof 검증 | soundness error, verification time |
| 5 | 결과와 키 버전 감사 | key ceremony, transcript 보관 |

> 요약: ZKP 품질은 proof 알고리즘보다 명제 회로가 올바르게 작성됐는지와 검증 입력이 조작되지 않았는지에 좌우됨.

---

## Ⅳ. 특징

| 구분 | zk-SNARK | zk-STARK | 판단 포인트 |
|:---|:---|:---|:---|
| 신뢰 설정 | trusted setup 필요 가능 | transparent setup | ceremony 운영 가능성 |
| Proof 크기 | 수백 byte~수 KB | 수십~수백 KB | 네트워크 비용 |
| 검증 비용 | 짧은 검증 시간 | proof 크기 대비 검증 비용 증가 | 온체인 gas, p95 검증 시간 |
| 암호 가정 | pairing, elliptic curve | hash, FRI | 양자내성 요구 여부 |

> 요약: SNARK는 작은 proof, STARK는 transparent setup과 hash 기반 구조가 강점이므로 적용 환경별 선택 기준이 다름.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 원본 제출·DB 조회 | proof 검증 | 개인정보 최소수집 요구 |
| 비용/성능 | 조회 ms 단위 | proving ms~분, verify ms~초 | 증명 빈도와 검증 비용 |
| 운영/위험 | 접근권한 중심 | 회로·키·proof lifecycle | 회로 감사와 setup 통제 역량 |

> 요약: ZKP는 원본 제출 위험을 줄이는 대신 회로 작성과 proving 비용을 운영 범위에 포함해야 함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 회로 오류 | 조건 누락·범위 검증 실패 | circuit audit, property test | 음성 테스트 통과율 100% |
| trusted setup 노출 | toxic waste 보관·유출 | multi-party ceremony, transcript 공개 | 참여자 수, 검증 로그 |
| 메타데이터 노출 | proof 제출 시점·주소 추적 | batching, relayer, unlinkable identifier | 상관분석 탐지 건수 |

> 요약: ZKP의 주요 위험은 암호 알고리즘보다 회로·setup·메타데이터에 있으며 감사 체계를 선행해야 함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 보안성 | soundness error 2^-80 이하, 회로 결함 0건 | 형식검증, audit report |
| 성능 | proof size, proving time, verification p95 | 벤치마크, 온체인 gas 측정 |
| 프라이버시 | witness 로그 노출 0건, linkability 점검 | DLP, privacy test |

> 요약: ZKP 도입은 soundness, proof size, 검증 지연, witness 노출 여부를 정량 점검해야 함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 검증 요구를 "성인 여부", "잔액 범위", "거래 합계 일치"처럼 명제로 고정하고 public input과 witness를 분리.
2. 모바일·온체인은 proof size가 작은 zk-SNARK, setup 신뢰 최소화가 요구되는 감사 환경은 zk-STARK를 우선 검토.
3. circuit audit, multi-party ceremony, proving/verification p95, witness 로그 DLP를 배포 전 승인 기준으로 설정.

**결론 (2줄):**
- 기술사 판단: 원본 제출을 줄여야 하는 신원·거래 검증은 ZKP, 단순 내부 시스템 조회는 RBAC·토큰화를 우선 적용함.
- 향후 방향: DID·VC, zk-rollup, 개인정보 최소공개 서비스에서 회로 감사와 표준화된 proof 검증 API가 중요해질 것임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ZKP를 설명하시오" | 3성질, Prover/Verifier, witness 흐름 | SNARK/STARK 차이와 적용 사례 |
| 요구사항 명시형 | "비교하시오", "설계하시오" | 회로·setup·검증 API 설계 | proof size, trusted setup, privacy risk 선택 기준 |

> 요약: 설명형은 3성질과 구조, 설계형은 회로·키 ceremony·검증 지표를 중심으로 전개함.
