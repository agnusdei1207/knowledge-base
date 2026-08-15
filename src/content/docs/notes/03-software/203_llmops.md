---
sidebar:
  order: 203
  label: "203. LLMOps (LLMOps)"
  badge:
    text: "기출 • 70%"
    variant: note
title: "LLMOps (LLMOps)"
date: "2026-08-14T05:40:00+09:00"
tags: ["notes-software"]
weight: 203
extra:
  question_no: "203"
  source_status: "기출"
  source_history: "138회"
  priority: 70
  priority_note: "언어모델 평가•배포•관측 수명주기가 최근 핵심임"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **LLM (Large Language Model, 대규모 언어 모델)**: 수천억 개의 매개변수를 가지고 방대한 텍스트 데이터로 사전 학습(Pre-training)된 생성형 AI 기반 언어 모델. GPT-4, Claude, Gemini 등이 대표적.
- **LLMOps (Large Language Model Operations)**: MLOps를 LLM의 특성(비결정 응답, 프롬프트 의존성, 환각, 고비용 API 호출)에 맞게 확장한 운영 체계. 모델·프롬프트·RAG 구성을 버전 관리·평가·배포·감시하는 전 과정.
- **Hallucination (환각)**: LLM이 사실에 근거하지 않은 그럴듯한 거짓 정보를 생성하는 현상. LLMOps의 평가와 가드레일이 반드시 탐지·차단해야 하는 핵심 위험.

</details>

- 정의/개념: Model•Prompt•RAG를 평가•배포•관측하는 **LLMOps**
- 배경/필요성: 비결정 응답•환각•Prompt 회귀로 **품질•안전 통제** 곤란

#### 한줄 요약

- 요리법·재료·안전 검사를 한 묶음으로 기록해 검증된 조합만 손님에게 제공한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **RAG (Retrieval-Augmented Generation, 검색 증강 생성)**: LLM이 고정된 학습 데이터의 지식 한계를 극복하기 위해, 사용자 질문에 관련된 외부 문서를 실시간으로 검색하여 LLM의 입력 컨텍스트에 제공함으로써 최신·도메인 특화 답변의 사실적 근거를 보강하는 패턴.

</details>

- **Configuration Versioning (구성 버전 관리)**: 모델(GPT-4o vs Claude 3.5), 시스템 프롬프트, RAG 설정(임베딩 모델·청크 크기·검색 전략)을 하나의 식별자로 묶어 구성 조합별 성능 비교 및 롤백 지원.
- **Probabilistic Evaluation (확률적 평가)**: 비결정 LLM 응답을 단일 실행이 아닌, 동일 평가 세트를 N회 반복 실행한 통계 분포(평균·표준편차·최솟값)로 품질·근거성·안전성 합격 여부 판정.
- **Guardrail (가드레일)**: 입력 단계(프롬프트 인젝션 차단, 개인정보 마스킹)와 출력 단계(유해 내용·환각 탐지)에서 LLM 응답의 안전성을 실시간으로 검사하는 통제 레이어.
- **Cost Governance (비용 거버넌스)**: 요청별 토큰 상한, 모델 라우팅(간단한 질문→소형 모델), 월별 API 예산 한도 등으로 LLM 호출 비용을 통제하는 관리 체계.

#### 한줄 요약

- 같은 질문을 여러 번 시험해 정확성·근거·안전·비용이 합격선 안인 구성을 선택한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **LLM Gateway (LLM 게이트웨이)**: 모든 LLM API 호출의 단일 진입점으로, 인증·모델 라우팅(비용 최적화)·요청 제한(Rate Limiting)·응답 캐싱·관측 로깅을 중앙에서 처리하는 구성요소.

</details>

```text
[LLMOps]
 ├── [Configuration Catalog | Model•Prompt•RAG]
 ├── [Evaluator | 품질•근거•안전•비용]
 ├── [LLM Gateway | 인증•Routing•Rate Limit]
 ├── [Guardrail | 입출력 안전 통제]
 └── [Observer | 지연•Token•비용•판정]
```

| 구성요소 | 책임 |
|---|---|
| Configuration Catalog | Model•Prompt•RAG **구성 Version** 관리 |
| Evaluator | 반복 평가로 품질•근거•안전•비용 판정 |
| LLM Gateway | 인증•Routing•Rate Limit•**Cache** 통제 |
| Guardrail | Prompt Injection•PII•유해 출력 차단 |
| Observer | 응답•지연•Token•비용을 **구성 Version**에 연결 |

#### 한줄 요약

- 카탈로그의 한 구성 묶음을 시험한 뒤 게이트웨이가 안전 검사를 거쳐 모델을 호출하고 결과를 기록한다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **Prompt Regression (프롬프트 회귀)**: 프롬프트를 수정한 후, 기존에 잘 동작하던 질문 유형에서 품질이나 응답 형식이 오히려 나빠지는 현상. 회귀 방지를 위해 수정 시마다 전체 평가 세트 재실행 필수.

</details>

```text
 1. [평가 구성 제출] ─── 모델·프롬프트·RAG 설정을 단일 버전으로 고정
          │
          ▼
 2. [품질·안전·비용 검증] ── 반복 평가 세트로 N회 실행 → 통계 분포 판정
          │
          ├─(하나라도 미달)──────► 승격 거부, 구성 수정
          │
          └─(모두 통과)──────────► Staging 환경 Canary 배포
                                           │
                                           ▼
 3. [승인 구성 Production 배포] ── LLM Gateway 라우팅 업데이트
          │
          ▼
 4. [운영 관측] ───────────── 응답·지연·토큰·비용·Guardrail 판정 기록
          │
          ├─(안전 사고 발생)──────► 즉각 이전 구성 롤백
          ├─(품질 저하 추세)──────► 개선 구성 준비 → 1단계 반복
          └─(정상)────────────────► 현재 구성 유지
```

### 동작 원리

1. **평가 구성 제출**: Model•Prompt•RAG를 단일 Version 고정
2. **품질•안전•비용 검증**: 반복 실행의 분포로 Gate 판정
3. **승인 구성 Production 배포**: Gateway Routing 갱신
4. **운영 관측**: 응답•지연•Token•비용•안전 판정 수집

#### 한줄 요약

- 시험 질문으로 합격한 조합만 배포하고 실제 대화의 품질·비용 문제를 다음 시험에 넣는다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Fine-Tuning (미세조정)**: 사전 학습된 LLM의 가중치를 도메인 특화 데이터셋으로 추가 학습하여, 특정 톤·형식·도메인 지식을 모델에 내재화하는 기법. RAG보다 추론 비용이 낮지만 학습 비용이 높고 지식 업데이트가 어려움.

</details>

| LLM 개선 방식 | Prompt Engineering | Fine-Tuning | RAG |
|:---|:---|:---|:---|
| **목적** | **응답 형식·행동 방향 즉시 조정** | **반복 패턴·도메인 지식 가중치 내재화** | **최신·사내 문서 기반 사실 답변 보강** |
| **지식 업데이트** | 즉각 (프롬프트 수정) | 학습 재실행 필요 (느림) | 검색 인덱스 업데이트로 즉각 반영 |
| **주요 위험** | 프롬프트 인젝션·회귀 | 과적합·학습 비용 | 검색 누락·잘못된 문서 근거 |
| **비용** | 낮음 (모델 변경 없음) | 높음 (GPU 학습 비용) | 중간 (벡터 DB·검색 비용) |

#### 한줄 요약

- 답변 형식은 지시문을 바꾸고 반복 행동은 학습하며 최신 문서 지식은 검색해 넣는다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **Promotion Gate (승격 게이트)**: 품질(RAGAS Score), 근거성(Faithfulness), 안전(Toxicity), 비용(토큰 예산) 등 각 항목의 합격 임계값을 모두 통과해야만 Production 배포를 허용하는 다중 기준 관문.

</details>

| 3대 실무 난제 | 발생 원인 | 실무 대책 및 해결방안 |
|:---|:---|:---|
| **1. 비결정 응답의 단일 평가 오류** | 1회 실행 결과로 LLM 품질을 판단 | **동일 평가 세트 N회 반복 → 평균·표준편차 기반 통계 분포 판정**|
| **2. 프롬프트 변경 시 회귀(Regression)** | 일부 질문 개선 후 기존 질문 품질 저하 방치 | **매 프롬프트 수정마다 전체 회귀 평가 세트 자동 재실행** |
| **3. 안전 실패가 평균 점수에 묻힘** | 전체 평균 품질 점수는 높지만 유해 응답 포함 | **Promotion Gate에 안전·근거성을 별도 독립 합격 조건으로 분리 설정** |

> 사례: **OpenAI API 기반 금융 상담 서비스에서 환각 탐지(Faithfulness Score < 0.9 차단) 및 개인정보 마스킹 가드레일 적용, 카카오·LG CNS의 LLMOps 플랫폼 구축 및 프롬프트 버전 관리 자동화 사례**

#### 한줄 요약

- 상담 답변은 검색 문서가 실제로 뒷받침하는지 확인한 뒤 새 구성을 배포한다.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Configuration Promotion (구성 승격)**: 품질·근거성·안전·비용의 4가지 승격 게이트를 모두 통과한 모델+프롬프트+RAG 조합을 Production 라우팅 대상으로 지정하는 LLMOps의 최종 배포 결정 절차.

</details>

- 모든 Gate를 통과한 **Model•Prompt•RAG 구성**만 승격•상시 감시

#### 한줄 요약

- 시험과 안전 검사를 통과하고 운영에서도 문제가 적은 모델·지시문·검색 조합만 승격한다.
