---
title: "MLOps (Machine Learning Operations)"
date: "2026-07-01"
tags:
  - "cspe-latest-tech"
weight: 211
---

# 📖 【암기용】 개념 완전 이해

> 목적: MLOps를 처음 봐도 완벽히 이해하게 만든다.

## 한눈에
- **개요**: ML 모델의 개발, 학습, 배포, 모니터링, 재학습을 자동화·표준화하는 운영 체계
- **왜 필요한가**: ML은 코드뿐 아니라 데이터, feature, 모델, 실험, 성능 drift가 함께 바뀌므로 일반 DevOps만으로 관리가 부족함.
- **핵심 직관**: 모델을 한 번 만드는 프로젝트가 아니라 계속 학습·배포·감시하는 제품 운영 체계로 다루는 방식임.

## 깊이 이해
- **배경·문제의식**: 실험 노트북에서 만든 모델은 운영 데이터 분포 변화, 재현성 부족, 수동 배포, 성능 저하 문제를 겪기 쉽다.
- **작동 원리**: 데이터 버전관리, feature store, experiment tracking, model registry, CI/CD/CT, monitoring, drift detection을 연결함.
- **비유**: 요리 레시피, 재료 출처, 조리 장비, 품질 검사, 고객 반응을 모두 기록해 같은 품질로 계속 생산하는 공장 운영임.
- **구체 예시**: 대출 모델의 AUC가 운영 후 0.82에서 0.76으로 하락하면 drift 알람을 발생시키고 검증된 재학습 파이프라인을 실행함.
- **흔한 오해·주의점**: MLOps는 도구 설치가 아니라 책임·승인·모니터링 기준을 포함하는 운영 프로세스임.

## 연결 개념
- LLMOps — LLM 서비스의 프롬프트·평가·비용 운영
- Model Registry — 모델 버전·승인 관리
- Data Drift — 운영 데이터 분포 변화

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: MLOps는 ML 모델의 전 생명주기를 자동화·재현·감시하는 운영 체계임.
> 2. **가치**: 모델 품질 저하, 배포 오류, 재현성 부족, 규제 감사 리스크를 줄임.
> 3. **판단 포인트**: 데이터·모델 버전, 승인 게이트, drift 모니터링, 재학습 기준을 명확히 해야 함.

## Ⅰ. 개요 및 필요성

- 개요: ML 학습·배포·운영 자동화 체계다.
- 배경: ML 시스템은 데이터 분포, feature, 모델 성능이 운영 중 계속 변해 재현성과 추적성이 깨질 수 있다.
- 필요성: MLOps는 pipeline, model registry, monitoring, retraining으로 학습·배포·재학습 프로세스를 관리한다.

## Ⅱ. 구조 및 구성요소

```text
Data Pipeline -> Feature Store -> Training Pipeline
  -> Model Registry -> Deployment/Monitoring
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data/Feature Pipeline | 데이터 수집·검증·특징 생성 | schema validation |
| Experiment Tracking | 실험 파라미터·지표 기록 | MLflow 등 |
| Model Registry | 모델 버전·승인 관리 | stage, lineage |
| Monitoring | 성능·drift·운영 지표 감시 | AUC, latency |

> 요약: MLOps는 데이터부터 모델 배포와 모니터링까지 연결해 재현 가능한 ML 운영을 구현함.

## Ⅲ. 동작원리 및 흐름도

```text
데이터 검증 -> 학습·평가 -> 모델 등록
  -> 승인 배포 -> 운영 감시·재학습
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 데이터 품질·schema 검증 | 결측률·분포 기준 |
| 2 | 학습·평가·실험 기록 | AUC/F1 목표 달성 |
| 3 | 모델 registry 등록·승인 | owner 승인 100% |
| 4 | drift 감시·재학습 트리거 | PSI>0.2 경보 |

> 요약: MLOps는 데이터 품질과 모델 성능을 기준으로 승인 배포하고 drift 발생 시 재학습을 수행함.

## Ⅳ. 특징

| 구분 | DevOps | MLOps | 판단 포인트 |
|:---|:---|:---|:---|
| 대상 | 코드·인프라 | 코드·데이터·모델·feature | 산출물 확대 |
| 배포 | deterministic build | 데이터 의존 학습 | 재현성 |
| 모니터링 | 장애·로그 | 성능·drift·bias | 모델 품질 |
| 자동화 | CI/CD | CI/CD/CT | 재학습 |

> 요약: MLOps는 DevOps에 데이터·모델 버전과 drift 감시, 지속 학습을 추가한 운영 체계임.

## Ⅴ. 실무 적용 및 결론

**적용 방안 3개:**
1. 파이프라인 구축: 데이터 검증, feature store, experiment tracking, model registry를 연결해 lineage 100% 기록
2. 배포 통제: 모델 승인 게이트에 AUC, fairness gap, latency, 보안 스캔 기준을 포함하고 실패 시 배포 차단
3. 운영 감시: drift PSI>0.2, AUC 5%p 하락, p95 latency 500ms 초과 시 알람과 재학습 workflow 실행

**결론 (2줄):**
- 기술사 판단: 운영 ML은 모델 정확도보다 재현성, 승인, drift 감시, 책임 추적성을 함께 설계해야 함
- 향후 방향: MLOps는 LLMOps, ModelOps, AI Governance와 통합된 AI 운영 플랫폼으로 발전함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "MLOps를 설명하시오" | 데이터->학습->배포->감시 흐름 | DevOps 대비 차이 |
| 요구사항 명시형 | "ML 운영체계 구축 방안을 제시하시오" | registry·drift·재학습 기준 | 승인 게이트·lineage |

> 요약: 설명형은 ML 생명주기 운영, 방안형은 재현성과 drift 기반 운영체계를 중심으로 작성함.
