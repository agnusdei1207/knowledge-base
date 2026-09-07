---
sidebar:
  order: 82
  label: "082. RAGAS"
  badge:
    text: "기출 · 50%"
    variant: note
title: "RAGAS"
date: "2026-09-07T16:00:00+09:00"
tags:
  - "notes-latest-tech"
weight: 82
extra:
  question_no: "082"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "RAG 평가지표 묶음의 대표 도구"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **RAGAS**: 질의•문맥•응답•기준 정보로 RAG 품질을 자동 평가하는 프레임워크이다.
- **검색 증강 생성(Retrieval-Augmented Generation, RAG)**: 검색 문서를 생성 답변의 근거로 제공하는 방식이다.

</details>

- 정의: 구조화 표본과 자동 지표로 RAG 품질을 평가하는 **RAGAS**이다.
- 배경/필요성: RAG 파이프라인의 구성요소(임베딩, 청킹, 검색기, LLM 프롬프트)를 튜닝할 때마다 정답 레이블(Ground Truth)을 수작업으로 라벨링하고 사람이 일일이 채점하는 방식은 막대한 시간과 비용이 소요될 뿐 아니라 평가자 간 주관적 편차로 인해 지속적인 회귀 테스트가 불가능한 병목이 발생함에 따라, 정답 레이블이 없어도(Reference-free) 또는 최소한의 기준 정보만으로 LLM을 판정관으로 활용해 검색 및 생성 품질을 자동 채점하는 오픈소스 평가 프레임워크 RAGAS(Retrieval Augmented Generation Assessment: Faithfulness, Answer Relevance, Context Precision, Context Recall / Synthetic Testset Generation)를 도입하여 **정답 라벨링 비용 없는 무참조(Reference-free) 자동 평가를 통한 초고속 RAG 튜닝 및 CI/CD 배포 파이프라인 연계, 지식 그래프 기반의 합성 테스트 데이터셋(Synthetic Testset) 자동 생성 지원, RAG 핵심 4대 지표의 수학적/의미적 정량화를 통한 파이프라인 최적화 가속**을 달성할 필요

#### 한줄 요약
- 동일 표본•조건으로 **검색•생성 품질** 반복 평가

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **충실성(Faithfulness)**: 응답 주장이 검색 문맥으로 뒷받침되는 정도이다.
- **문맥 정밀도•재현율(Context Precision•Recall)**: 관련 근거의 순위와 포함 정도이다.

</details>

- 질의•응답•문맥•기준 정보의 **평가 스키마 구조화**
- 목적별 **충실성•문맥 정밀도•재현율** 조합
- 평가 모델·프롬프트·반복 조건의 **재현 가능한 실행 기록**

#### 한줄 요약
- **평가 스키마•지표•실행 조건** 고정으로 점수 비교

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **평가 모델(Evaluation Model)**: 자연어 의미와 지표 규칙으로 표본을 판정한다.
- **임베딩 모델(Embedding Model)**: 의미 유사도 지표를 위한 벡터를 생성한다.
- **평가 스키마(Evaluation Schema)**: 질의•응답•문맥•기준 답 필드 구조이다.
- **지표 모음(Metrics Suite)**: 검색과 생성을 분리 측정하는 지표 집합이다.
- **평가 실행기(Evaluation Runner)**: 표본•지표•모델과 결과•비용•버전을 연결한다.

</details>

```text
[RAGAS System]
├── [입력/데이터 계층]
│   └── [평가 데이터셋 (Evaluation Dataset)]
├── [평가 정의 계층]
│   ├── [지표 모음 (Metrics Suite)]
│   └── [평가 모델 (Judge/Embedding LLM)]
└── [실행/결과 계층]
    ├── [평가 실행기 (Evaluation Runner)]
    └── [결과 저장소 (Result Store)]
```

- 선의 의미: 계층 구조 및 상하위 포함 관계를 나타낸다.

| 구성요소 | 책임 |
|:---|:---|
| 평가 데이터셋 | 단일 질의•대화 표본의 **평가 스키마 보관** |
| 지표 모음 | 평가 대상•필수 입력•**점수 규칙 정의** |
| 평가 모델 | **평가 모델•임베딩 모델** 기반 의미 판정 |
| 평가 실행기 | 프롬프트•재시도•동시성의 **실행 조건 통제** |
| 결과 저장소 | 표본별 점수•비용•추적의 **평가 결과 보존** |

#### 한줄 요약
- **데이터셋•지표•평가 모델•실행기•결과 저장소** 구성

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **실행 조건 고정(Execution-condition Pinning)**: 모델•프롬프트•버전•재시도를 기록한다.

</details>

```text
평가 책임자
   │ 1. 평가 목적•표본 스키마 정의
   │ 2. 지표•평가 모델 선택
   ▼
평가 실행기
   │ 3. 프롬프트•버전•재시도 고정
   │ 4. 표본 지표 점수 실행
   │ 자동 평가 결과
   ▼
인간 검증자
   │ 5. 대표 표본 인간 검증
   └── 평가 결과 ──▶ 평가 책임자
```

### 동작 원리

1. 평가 목적•표본 스키마 정의: 목표와 지표별 **필수 필드** 구성
2. 지표•평가 모델 선택: 질문별 **점수 규칙·판정 모델** 지정
3. 프롬프트•버전•재시도 고정: 비교 가능한 **실행 조건** 저장
4. 표본 지표 점수 실행: 문맥·응답별 **자동 점수·비용** 산출
5. 대표 표본 인간 검증: 자동 결과와 **전문가 판정 일치도** 대조

#### 한줄 요약
- **스키마•지표•실행 조건•자동 평가•인간 검증** 수행

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **LLM 기반 평가(LLM-based Evaluation)**: 모델의 의미 이해로 판정한다.
- **비LLM 기반 평가(Non-LLM-based Evaluation)**: 문자열•통계•임베딩 계산으로 판정한다.
- **인간 평가(Human Evaluation)**: 전문가가 고위험 결과를 직접 판정한다.

</details>

| 구분 | LLM 기반 지표 | 비LLM 기반 지표 | 인간 평가 |
|:---|:---|:---|:---|
| 적용 기준 | **의미·문맥 판정** | **문자열·통계 판정** | **고위험 최종 판정** |
| 핵심 특징 | 프롬프트 기반 **의미 평가** | 일치•유사도 기반 **결정론적 평가** | 전문가 지침 기반 **직접 평가** |
| 한계 | **비결정성·모델 편향** | **의미 관계 판정 한계** | **시간·비용·평가자 편차** |

#### 한줄 요약
- 의미 이해·결정성·비용·편향에 따른 **평가 방식 구분**

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **점수 기준 이동(Score Baseline Shift)**: 모델•프롬프트 변경으로 점수 의미가 달라지는 현상이다.
- **반복 실행 분포(Repeated-run Distribution)**: 반복 점수의 평균•분산•범위이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 지표별 **필수 스키마 누락** | 지표 입력 계약에 맞춘 필드 사전 검증 | 계산 실패•무효 점수 **방지** |
| 평가 모델 변경의 **점수 기준 이동** | 모델•프롬프트 버전 고정과 병렬 재평가 | 지표 시계열의 **비교 가능성 확보** |
| 비결정 평가의 **점수 변동** | 반복 실행 분포•인간 일치도 측정 | 자동 점수의 **불확실성 확인** |

#### 한줄 요약
- **필수 스키마•버전•반복 분포•인간 일치도** 검증

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **지표 선택 기준(Metric Selection Criteria)**: 목적•스키마•인간 일치도•반복 안정성이다.

</details>

- RAG 시스템의 성능을 표준화된 4대 핵심 지표로 자동 정량화하여 글로벌 RAG 평가 방법론의 사실상 표준(De Facto Standard)으로 자리 잡은 **최고의 오픈소스 RAG 자동 평가 프레임워크(RAGAS / Reference-free LLM-as-a-Judge / Synthetic Data Generator / Context Precision & Recall / Faithfulness & Answer Relevance / CI/CD Pipeline Integration)의 핵심 도구**로 확고히 자리 잡았으며, 다국어 및 멀티모달 RAG 평가로 진화하는 가운데, 실무 RAGAS 적용 시에는 **평가용 LLM(Judge LLM: GPT-4o, Claude 3.5 Sonnet 등)의 채점 프롬프트 버전과 온도(Temperature=0)를 엄격히 고정하고, 자동 채점 결과와 사내 도메인 전문가 평가 간의 상관계수(Correlation)를 정기 실측하여 지표 신뢰성을 보정하며, 테스트셋 자동 생성 파이프라인과의 연계를 통한 테스트 커버리지 극대화**를 결합하여 완벽한 자동 평가 신뢰성과 민첩한 RAG 엔지니어링을 완성

#### 한줄 요약
- **스키마 완전성•인간 일치도** 대상 따라 평가 구성 결정
