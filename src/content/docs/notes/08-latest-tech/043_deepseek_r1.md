---
sidebar:
  order: 43
  label: "043. DeepSeek-R1 추론 모델 (DeepSeek-R1)"
  badge:
    text: "기출 · 50%"
    variant: note
title: "DeepSeek-R1 추론 모델 (DeepSeek-R1)"
date: "2026-07-27T23:59:59+09:00"
tags:
  - "notes-latest_tech"
weight: 43
extra:
  question_no: "043"
  source_status: "기출"
  source_history: "138회"
  priority: 50
  priority_note: "효율적 추론 학습 사례로 비교 가치"
---

## 미리 알고가기

- **딥시크 R1(DeepSeek-R1)**: 검증 보상으로 후학습한 추론 언어모델
- **딥시크 V3 기반(DeepSeek-V3-Base)**: R1 후학습의 기반 모델
- **R1 제로(DeepSeek-R1-Zero)**: 선행 SFT 없이 RL만 적용한 실험형 모델
- **대규모 언어모델(Large Language Model, LLM)**: R1 기반 생성 모델 유형
- **지도 미세조정(Supervised Fine-Tuning, SFT)**: 풀이 예시로 초기 행동 조정
- **강화학습(Reinforcement Learning, RL)**: 보상으로 추론 정책 강화
- **검증가능 보상 강화학습(RLVR)**: 정답 검증값을 보상으로 활용
- **그룹 상대 정책 최적화(Group Relative Policy Optimization, GRPO, 지알피오)**: 그룹 후보의 상대 보상으로 정책을 갱신하는 강화학습 기법
- **혼합 전문가(Mixture of Experts, MoE, 엠오이)**: 입력별 일부 전문가만 활성화하는 모델 구조
- **다중 헤드 잠재 어텐션(Multi-head Latent Attention, MLA, 엠엘에이)**: 잠재 표현으로 키·값 캐시 부담을 줄이는 어텐션 구조
- **응용 프로그래밍 인터페이스(API)**: 원본 모델 호출 경계



## Ⅰ. 개요

- 정의/개념: V3 기반 SFT·RL 결합 추론 모델
- 기존 한계: 추론 예시 중심 SFT만으로 자발적 해결 전략 학습 제한
- **배경/필요성**: 검증 보상 기반 추론 강화와 지식 증류

### 쉽게 이해하기 (학습용)

- 기반 모델에 풀이 예시와 정답 검증 보상을 적용해 해결 방식 후학습

## Ⅱ. 특징

- R1-Zero는 선행 SFT 없이 강화학습 효과를 실험한다
- R1은 콜드 스타트 SFT와 다단계 강화학습을 결합한다
- 추론 데이터를 다른 기반 모델에 증류해 소형화를 지원한다

### 쉽게 이해하기 (학습용)

- 원본·실험형·증류형 모델 변형별 구분 필요

## Ⅲ. 구성요소 및 구조

| 설계 요소 | 설명 |
|:---|:---|
| DeepSeek-V3-Base | MoE·MLA 기반 사전학습 모델 |
| Cold-start SFT | 추론 형식 및 초기 행동 안내 |
| GRPO·검증 보상 | 수학·코드 정답 보상 정책 강화 |
| Rejection Sampling | 양질 데이터 선별 및 일반화 보완 |
| Distillation | R1 데이터를 소형 모델에 이전 |

```text
[ DeepSeek-V3-Base: MoE·MLA ]
  +-- [ R1-Zero ]: 선행 SFT 없이 GRPO·검증 보상 RL
  |
  +-- [ DeepSeek-R1 ]
       +-- Cold-start SFT Data·Checkpoint
       +-- Reasoning GRPO·Verifier
       +-- Rejection-Sampled Reasoning + General SFT Data
       +-- 최종 Reasoning·Preference RL Checkpoint
       +-- 생성 Data --> [ Qwen·Llama 기반 Distilled Dense Models ]
```

> 요약: 기반 모델에 SFT·GRPO·선별 학습 연결

### 쉽게 이해하기 (학습용)

- 학습 뒤 보상 강화와 선별을 반복해 원본/증류 모델 생성

## Ⅳ. 원리 및 절차 흐름도

```text
기반준비
↓
초기학습
↓
보상학습
↓
데이터선별
↓
최종학습
↓
증류평가
```

| 절차 | 설명 |
|:---|:---|
| 기반 | V3-Base 및 검증기 준비 |
| 초기 | 초기 데이터로 SFT 수행 |
| 보상 | GRPO·검증 보상으로 강화 |
| 선별 | 정답·가독성 기준 응답 선택 |
| 최종 | 선별 데이터 SFT 및 RL 수행 |
| 증류 | 소형 모델 이전 및 성능 평가 |

> 요약: SFT·GRPO·선별 후 소형 모델로 증류함

### 쉽게 이해하기 (학습용)

- 모델 변형별 기반·라이선스·배포 조건을 확인함

## Ⅴ. 종류 및 비교

| 판단 기준 | R1-Zero | R1 |
|:---|:---|:---|
| 적용 기준 | 순수 RL 추론 연구 | 일반 활용·가독성 필요 |
| 핵심 특징 | 선행 SFT 없이 RL 적용 | 콜드 스타트 SFT·RL 결합 |
| 한계 | 가독성·언어 혼용 문제 | 긴 추론의 비용·오류 |

> 요약: R1-Zero는 실험형, R1은 활용형 모델임

### 쉽게 이해하기 (학습용)

- R1-Zero는 실험형, R1은 다단계 후학습 활용형임

## Ⅵ. 실무 사례

- 온프레미스 채택 시 모델별 성능·하드웨어 따로 평가
- 가중치 공개와 완전한 학습 데이터 재현성은 구분 필요

### 쉽게 이해하기 (학습용)

- 가중치를 받을 수 있다는 사실과 학습 데이터·과정을 모두 재현할 수 있다는 사실은 다름

## Ⅶ. 결론

- DeepSeek-R1은 SFT·검증 보상 RL을 결합한다
- 변형별 학습·구조·라이선스 확인해 과업 환경 적용 필요

### 쉽게 이해하기 (학습용)

- 같은 R1 이름 아래 모델마다 크기와 기반·학습법이 달라 정확한 변형을 확인해야 함
