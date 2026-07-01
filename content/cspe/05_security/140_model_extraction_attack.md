---
title: "모델 추출 공격 (Model Extraction Attack)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 140
---

# 📖 【암기용】 개념 완전 이해

> 목적: 모델 추출 공격을 처음 보는 사람도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 모델 API를 반복 질의해 원본 모델과 유사하게 동작하는 복제 모델을 만드는 공격
- **왜 필요한가**: 모델은 학습 데이터, GPU 비용, 튜닝 노하우가 들어간 지식재산이다. API가 확률·로짓을 많이 제공하고 호출 제한이 약하면 경쟁자가 비용을 낮춰 모델을 모방할 수 있다.
- **핵심 직관**: 유명 셰프의 레시피를 훔치지 못해도 수천 번 시식하고 맛을 기록해 비슷한 조리법을 재현하는 방식이다.

## 깊이 이해
- **배경·문제의식**: MLaaS와 LLM API는 모델 내부 파라미터를 숨긴다. 그러나 예측 결과를 충분히 많이 수집하면 공격자는 입력과 출력 쌍을 학습 데이터처럼 사용해 대체 모델을 훈련할 수 있다.
- **작동 원리**: 공격자는 정상 API 사용자처럼 질의한다. 다양한 입력을 자동 생성하고 응답 라벨·확률·로짓을 저장한 뒤, 이를 teacher-student distillation 방식으로 학습해 decision boundary를 근사한다.
- **비유**: 자동 채점기에 수많은 문제를 넣고 정답을 모아, 채점기의 채점 기준을 모방하는 새 채점기를 만드는 과정이다.
- **구체 예시**: 이미지 분류 API가 top-5 확률을 제공하고 호출 제한이 느슨하면, 10만~100만 질의로 유사 정확도의 student 모델을 만들 수 있다.
- **흔한 오해·주의점**: "모델 파일을 다운로드할 수 없으니 안전함"은 틀렸다. 출력 API가 풍부하면 블랙박스만으로도 기능 복제가 가능하다.

## 연결 개념
- Knowledge Distillation: 원본 모델 출력을 teacher label로 사용해 student 모델 학습
- Watermarking: 추출 모델 여부를 판정하기 위한 특수 입력·출력 패턴 삽입
- Rate Limiting: 대량 질의와 탐색형 입력을 탐지·제한하는 API 보호

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 모델 추출 공격은 데이터 유출이 아니라 API 출력과 대량 질의를 이용한 모델 지식재산 탈취 문제이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 모델 추출 공격은 블랙박스 API 질의 결과를 수집해 원본 모델의 decision boundary 또는 기능을 복제하는 공격이다.
> 2. **가치**: 방어는 출력 정보량 제한, 질의 속도 제한, 이상 탐지, watermark, 계약·감사 통제를 함께 적용해야 한다.
> 3. **판단 포인트**: 고가 학습 모델, 특화 도메인 모델, 확률 출력 API는 모델 IP와 서비스 비용 관점에서 추출 위험을 우선 평가해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| AI 모델 IP 보호 위험 이해 | API 반복 질의, teacher-student 학습, decision boundary 근사 | 학습 데이터 탈취와 혼동 |
| 방어 아키텍처 설계 확인 | output limiting, rate limit, query anomaly, watermark | API 키 인증만 제시 |
| 운영 지표 판단 확인 | query entropy, fidelity, extraction cost, watermark hit | 정확도 지표만 쓰고 경제성·탐지 지표 누락 |

> 요약: 이 문제는 모델 파일 보호가 아니라 공개 API의 출력 정보량과 질의 행태를 통제하는 역량을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: API 응답 기반 모델 복제
- 배경: AI 모델은 학습 데이터, GPU 비용, 튜닝 노하우가 결합된 자산이며 API 응답만으로도 기능 복제가 가능함.
- 필요성: 테넌트별 rate limit, 응답 확률값 제한, 워터마킹, 이상 질의 탐지 기준으로 모델 IP와 과금 우회를 통제해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Attacker Input Generator -> Target Model API -> Label/Probability Output
                                   +-> Query Log / Rate Limit
Collected Pairs -> Student Training -> Substitute Model -> Fidelity Test
```

| 구성요소 | 역할 | 통제 포인트 |
|:---|:---|:---|
| 입력 생성기 | 무작위·경계·합성 입력을 대량 생성 | query diversity 탐지 |
| 대상 API | 원본 모델 예측 결과 제공 | output rounding, top-k 제한 |
| 응답 수집기 | 입력·라벨·확률 쌍 저장 | API key, quota, abuse score |
| 대체 모델 | 수집 데이터를 학습해 기능 모방 | watermark challenge 검사 |
| 탐지 계층 | 질의 패턴과 복제 정황 분석 | SIEM, anomaly model, 법적 로그 |

> 요약: 추출 공격은 입력 생성, API 응답 수집, student 학습, fidelity 검증으로 구성되며 API 출력과 질의량이 핵심 통제점이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
입력 공간 샘플링 -> API 대량 질의 -> 라벨/확률 저장
-> student 모델 학습 -> 원본 모델과 응답 일치율 측정
-> watermark challenge와 이상 질의 탐지로 차단
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 공격자가 입력 분포를 넓게 샘플링 | query entropy, OOD 비율 |
| 2 | API에서 라벨·확률·로짓을 반복 수집 | user/key별 QPS, quota |
| 3 | 수집 쌍으로 student 모델 학습 | distillation loss, fidelity |
| 4 | 원본과 대체 모델 응답 일치율 평가 | agreement rate 90% 이상 시 위험 |
| 5 | 탐지·차단·증거 보존 수행 | watermark hit, audit log |

> 요약: 공격 성공은 원본과 대체 모델의 응답 일치율로 판단하며, 방어는 질의 다양성과 대량 호출을 조기에 식별해야 한다.

---

## Ⅳ. 특징

| 구분 | 모델 역전 공격 | 모델 추출 공격 | 수치·판단 기준 |
|:---|:---|:---|:---|
| 공격 목표 | 학습 데이터·민감 특성 복원 | 모델 기능·decision boundary 복제 | fidelity, agreement rate |
| 주요 입력 | 목표 클래스 중심 반복 질의 | 입력 공간 대량 샘플링 | query entropy, QPS |
| 피해 영향 | 개인정보·민감정보 노출 | 지식재산 탈취, 과금 회피 | 추출 비용 대비 학습 비용 |
| 방어 전략 | DP, 출력 최소화 | rate limit, watermark, output limiting | top-1 label, quota 1일 N회 |

> 요약: 추출 공격은 개인정보보다 모델 IP 손실이 핵심이며, API 응답 정보량과 호출 경제성을 통제해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 내부 전용 모델 | 공개 API 모델 | 외부 고객에게 예측 API 제공 시 |
| 비용/성능 | top-k 확률 제공 | top-1 label, confidence rounding | 설명가능성 요구와 IP 보호 균형 |
| 운영/위험 | 정적 quota | 동적 abuse score, query entropy | 자동화 질의·경계 탐색 증가 시 |

> 요약: 공개 API는 사용 편의보다 출력 정보량·질의 비용·탐지 증거를 함께 설계해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 모델 IP 복제 | 대량 입력·출력 쌍 수집 | quota, output rounding, watermark | fidelity 80% 이상 계정 조사 |
| 탐지 회피 | 다수 계정·IP로 저속 질의 | device fingerprint, billing graph 분석 | 계정 군집 anomaly score |
| 서비스 비용 증가 | 공격 질의가 GPU 추론 자원 소비 | cost-based throttling, prepaid quota | 계정별 GPU-second 비용 |

> 요약: 추출 방어는 복제 정확도뿐 아니라 계정 군집, 비용 소모, watermark 증거를 함께 추적해야 한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 출력 제한 | top-1 label 또는 confidence 소수 2자리 이하 | API schema 검사 |
| 질의 탐지 | query entropy 상위 1% 계정 조사 | feature logging, anomaly detection |
| IP 보호 | watermark challenge hit 95% 이상 | canary input, legal evidence log |

> 요약: 모델 추출 대응 성과는 출력 제한, 이상 질의 탐지, watermark 판별률로 평가한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. API 단계: top-k 확률 대신 top-1 label 기본 제공, confidence는 소수 2자리 이하 반올림, 로짓·임베딩 원문 반환 금지
2. 운영 단계: API key별 QPS·일 quota·query entropy·OOD 비율을 수집하고 상위 1% 이상 계정은 step-up verification 적용
3. 법적·증거 단계: watermark/canary input 100개 이상 운영, hit 로그와 과금 기록을 1년 보존해 계약 위반 조사에 사용

**결론 (2줄):**
- 기술사 판단: 범용 저가 모델은 rate limit 중심, 고가 특화 모델은 watermark와 출력 제한과 비용 기반 throttling을 병행함
- 향후 방향: LLM API와 에이전트 도구 시장 확대에 따라 모델 사용권 계약, watermark 표준, 추출 탐지 관측성이 모델 보안의 핵심 축이 됨

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "모델 추출 공격을 설명하시오" | API 질의 수집과 student 학습 흐름 | 모델 역전 공격과의 차이 |
| 요구사항 명시형 | "대응 방안을 제시하시오", "운영 방안을 설명하시오" | 출력 제한, quota, watermark 탐지 흐름 | fidelity·query entropy·watermark 기준 |

> 요약: 설명형은 기능 복제 원리를, 방안형·운영형은 API 출력 정보량과 이상 질의 탐지를 중심으로 작성한다.
