---
sidebar:
  order: 89
  label: "089. AI 레드팀 (AI Red Teaming)"
  badge:
    text: "기출 • 85%"
    variant: note
title: "AI 레드팀 (AI Red Teaming)"
date: "2026-08-13T21:00:00+09:00"
tags:
  - "notes-security"
weight: 89
extra:
  question_no: "089"
  source_status: "기출"
  source_history: "135회, 137회, 138회"
  priority: 85
  priority_note: "135•137•138회 반복된 AI 검증 방법론 핵심임"
---

## Ⅰ. 개요

<details><summary>핵심 용어</summary>

- **AI(Artificial Intelligence) 레드팀(AI Red Teaming)**: 적대적(Adversarial) 공격자의 시각에서 AI 시스템(LLM, RAG, 에이전트)의 프롬프트 인젝션, 탈옥, PII 유출, 백도어, 비인가 시스템 조작 취약점을 전 능동적으로 탐색 및 재현 평가하는 모의침투 방어 방법론이다.
- **위협 모델링(Threat Modeling)**: AI 시스템의 보호 자산(모델 가중치, DB), 공격면(Prompt, RAG, API), 공격자 역량을 구조적으로 도면화하는 사전 분석 활동이다.

</details>

- 정의/개념: 공격자 관점에서 AI 취약점을 재현하는
  **AI 레드팀** 평가 체계
- 배경/필요성: 기존 취약점 분석으로 찾기 어려운
  **자연어 우회**와 에이전트 연쇄 공격

#### 한줄 요약

- 적대적 공격자 관점에서 AI 시스템(LLM, RAG, 에이전트)의 인젝션, 탈옥, PII 유출 취약점을 선제 탐색하고 재현 평가하는 체계이다.

## Ⅱ. 특징

<details><summary>핵심 용어</summary>

- **샌드박스(Sandbox / Isolated Environment)**: 레드팀 공격 수행 시 실제 운용 데이터 파손이나 Prod 환경 영향을 차단하기 위해 격리시킨 검증용 가상 테스트 환경이다.
- **중단 조건(Abort Criteria / Circuit Breaker)**: 테스트 진행 중 인프라 다운, 인접 시스템 파손, 과도한 API 과금 발생 시 레드팀 활동을 즉각 강제 중단하는 통제 규칙이다.
- **재현 증거(Reproducible Artifacts / Proof of Concept)**: 탐지된 AI 취약점의 입출력 프롬프트 로그, Lease ID, 파라미터를 동일하게 재현할 수 있는 증적 산출물이다.
- **회귀 평가(Regression Testing / Re-evaluation)**: 가드레일 보정 및 모델 재학습 후 기존 발견된 적대적 공격 시나리오가 확실히 차단되었는지 반복 재검증하는 과정이다.

</details>

- 프롬프트 텍스트 수준에 그치지 않고 RAG 지식베이스, 에이전트 API 툴 호출까지 전체 파이프라인의 연쇄 유출 경로를 추적한다.
- 실환경 피해 예방을 위해 격리된 **샌드박스** 및 과금/파손 방지 **중단 조건**을 엄격히 설정한다.
- 취약점 조치 후 보정 효과를 판단하기 위한 **재현 증거** 보존 및 자동화 **회귀 평가** 체계를 운용한다.

#### 한줄 요약

- 엔드투엔드 연쇄 공격 경로 탐색, 샌드박스 안전 격리, 중단 조건 통제, 재현 증적 보존 및 자동화 회귀 평가 특성을 지닌다.

## Ⅲ. 구조 및 구성요소

<details><summary>핵심 용어</summary>

- **검증 하네스(Test Harness / Automation Harness)**: PyRIT, Garak 등 자동화 적대적 텍스트 생성 툴과 프롬프트 패저(Fuzzer)를 묶어 실시간 반응을 테스트하는 엔진이다.
- **시나리오 저장소(Scenario Repository / Attack Pattern Store)**: DAN 페르소나, GCG 적대적 토큰, 간접 인젝션 모음 등 최신 레드팀 공격 패턴을 버전 관리하는 DB이다.

</details>

```text
AI 레드팀 체계
├─ 설계
│  ├─ 범위·위협 모델
│  └─ 시나리오 저장소
├─ 실행
│  └─ 하네스·샌드박스
└─ 판정·개선
   ├─ 증거·위험 분류
   └─ 완화·회귀 체계
```

선의 의미: 설계(위협 모델/시나리오), 실행(하네스/샌드박스), 판정 개선(증거 분류/회귀 체계)의 3단계 AI 레드팀 아키텍처이다.

| 도메인 단계 | 구성 요소 | 핵심 기능 및 역할 |
|:---|:---|:---|
| 설계 단계 | **위협 모델링**, **시나리오 저장소** | 보호 자산 및 신뢰 경계 확정, 최신 인젝션/탈옥 **시나리오 저장소** 로딩 |
| 실행 단계 | **검증 하네스**, **샌드박스** | PyRIT/Garak 기반 자동화 프롬프트 패징, **샌드박스** 내 안전 모의 침투 집행 |
| 판정·개선 단계 | **재현 증거** 분석, **회귀 평가** | 취약점 **재현 증거** 작성, Guardrail 보안 보정 및 회귀 자동화 시험 통과 |

#### 한줄 요약

- 위협 모델 설계, 시나리오 저장소 활용, 샌드박스 내 검증 하네스 실행, 재현 증적 분석 및 회귀 평가 구조로 이루어진다.

## Ⅳ. 흐름도

<details><summary>핵심 용어</summary>

- **잔여 위험 평가(Residual Risk Assessment)**: 가드레일 및 방어 통제를 수립한 이후에도 남아있는 우회 공격 성공률(ASR)을 측정 평가하는 단계이다.
- **변형 회귀(Mutation & Bypass Regression Testing)**: 기존 취약점에 방어 룰을 적용했을 때, 공격자가 룰을 우회하도록 변형한 시나리오까지 차단하는지 재시험하는 단계이다.
- **교전 규칙•안전 한도 검증(Rules of Engagement & Safety Limit Verification)**: 레드팀의 공격 범위, 허용 시간, 중단 조건을 계약 정의하는 단계이다.
- **공격 시나리오 안전 실행(Safe Attack Scenario Execution)**: 수립된 적대적 공격 시나리오를 하네스를 통해 샌드박스에서 수행하는 단계이다.
- **근본 원인•완화 구현(Root Cause & Mitigation Implementation)**: 오탐/미탐 가드레일을 보정하고 프롬프트/모델/PEP 정책을 수정하는 단계이다.
- **잔여 위험 재산정(Residual Risk Re-assessment)**: 통제 적용 후 ASR이 목표 기준 이하로 내려갔는지 평가하는 단계이다.
- **변형 회귀•배포 결정(Mutation Regression & Deployment Decision)**: 변형 공격 회귀 시험 통과 시 최종 프로덕션 배포를 승인하는 단계이다.

</details>

```text
자산·범위·중단 조건
          |
          v
1. 교전 규칙·안전 한도 검증
          |
          v
2. 공격 시나리오 안전 실행
          |
          v
3. 근본 원인·완화 구현
          |
          v
4. 잔여 위험 재산정
          |
          v
5. 변형 회귀·배포 결정
          |
          v
       배포 판정
```

### 동작 원리

1. **교전 규칙·안전 한도 검증**: 범위·중단 조건 확정
2. **공격 시나리오 안전 실행**: 샌드박스에서 공격 재현
3. **근본 원인·완화 구현**: 가드레일·PEP 정책 보정
4. **잔여 위험 재산정**: 완화 후 공격 성공률 재측정
5. **변형 회귀·배포 결정**: 우회 회귀 통과 시 배포 승인

#### 한줄 요약

- 교전 규칙 수립, 샌드박스 시나리오 실행, 가드레일 보정, 잔여 위험 재산정 및 변형 회귀 시험 후 배포 승인 단계로 이행된다.

## Ⅴ. 종류 및 비교

<details><summary>핵심 용어</summary>

- **레드팀 평가(Adversarial Red Team Evaluation)**: 공격자 관점에서 지능형 적대적 프롬프트를 창의적으로 조합하여 미지의 바이패스 취약점을 탐색하는 기법이다.
- **벤치마크 평가(Benchmark Evaluation)**: MMLU, GSM8K 등 정형화된 데이터셋으로 모델의 지식 및 안전 정확도를 기계적으로 비교 측정하는 평가이다.
- **자동 적대 평가(Automated Adversarial Evaluation / Automated Fuzzing)**: PyRIT, Garak 툴을 사용해 대량의 탈옥/인젝션 패징 프롬프트를 자동 투입 측정하는 기법이다.

</details>

| AI 평가 방법론 | AI 레드팀 평가 (AI Red Teaming) | 벤치마크 평가 (Benchmark Evaluation) | 자동 적대 평가 (Automated Fuzzing) |
|:---|:---|:---|:---|
| 핵심 목적 | 미지의 복합 공격 경로 및 실질적 바이패스 탐색 | 정형 데이터 세트를 통한 모델 간 상대적 성능 비교 | 알려진 인젝션/탈옥 패턴의 대량 고속 자동 검증 |
| 주체 및 방식 | 보안 전문가 (Human) + 자동화 툴 융합 | 자동화 벤치마크 평가 스크립트 실행 | PyRIT, Garak, Promptfoo 등 Fuzzer 툴 |
| 장점 | RAG, 에이전트 연쇄 취약점 등 실세계 위협 발굴 | 객관적 표준 정량 지표 도출 용이 | 적은 비용과 시간으로 대량 공격 테스트 가능 |
| 한계 | 공수 및 전문 보안 인력 요구 | 실제 공격자의 적대적 변형 탐지 불가 | 알려지지 않은 변종 페르소나 탐지 한계 |

#### 한줄 요약

- AI 레드팀(창의적 모의침투), 벤치마크(정형 성능 측정), 자동 적대 평가(툴 기반 대량 패징)로 구성되어 상호보완 적용된다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>핵심 용어</summary>
- **NIST(National Institute of Standards and Technology)**: 미국 국립표준기술연구소이다.
- **AI 600-1 (NIST Generative AI Profile, AI 600-1)**: 생성형 AI 시스템에 대한 적대적 레드팀 평가 지침을 수록한 NIST 지침이다.
- **RMF(Risk Management Framework)**: 표준 위험 관리 프레임워크이다.
- **ATLAS(MITRE ATLAS)**: AI 시스템 적대적 공격 기법(TTPs)을 정리한 MITRE 지식베이스이다.
- **RAG(Retrieval-Augmented Generation)**: 외부 벡터 지식베이스를 연동하는 아키텍처이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| AI 레드팀 평가의 체계적 프레임워크 부재 | **NIST AI 600-1** 및 **NIST RMF** 매핑 | 전사 AI 시스템 수명주기 전반의 적대적 레드팀 거버넌스 정립 |
| 표준화된 공격 시그니처 분석 미비 | **MITRE ATLAS** TTPs 프레임워크 적용 | 챗봇, RAG, 에이전트별 시그니처 및 방화벽 룰 정밀화 |
| 레드팀 평가 중 프로덕션 인프라 파손 | **샌드박스** 구축 및 **중단 조건** (Circuit Breaker) | 과도한 API 과금 및 데이터 파손 위험 원천 방지 |

#### 한줄 요약

- NIST AI 600-1 준용, MITRE ATLAS 기법 매핑, 샌드박스 및 Circuit Breaker 중단 조건을 적용하여 레드팀을 수행한다.

## Ⅶ. 결론

<details><summary>핵심 용어</summary>

- **레드팀 배포 근거(Red Teaming Deployment Sign-off Criteria)**: 레드팀 모의 침투를 통해 고위험 경로가 완화되었고 변형 회귀 시험까지 100% 차단됨을 입증하는 정량적 배포 승인 지침이다.

</details>

- 고위험 경로 완화 후 **변형 회귀** 통과 모델만 배포

#### 한줄 요약

- NIST AI 600-1 준수, MITRE ATLAS 매핑, 샌드박스 하네스 실행, 회귀 평가 및 레드팀 배포 근거 확립 중심 AI 레드팀 체계 구축 필수.
