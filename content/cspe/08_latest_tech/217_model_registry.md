---
title: "Model Registry 모델 레지스트리 (Model Registry)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 217
---

# 📖 【암기용】 개념 완전 이해

> 목적: Model Registry를 모델 버전, 메타데이터, 승인 상태, 배포 이력을 관리하는 운영 저장소로 이해하게 만든다.

## 한눈에
- **개요**: 모델 아티팩트와 버전, 지표, 승인 단계, 배포 이력을 관리하는 중앙 저장소
- **왜 필요한가**: 같은 모델 이름이라도 학습 데이터, 파라미터, 코드, 평가지표, 승인 상태가 다르면 운영 결과와 책임이 달라짐.
- **핵심 직관**: Model Registry는 모델의 창고이자 출고 승인대이며 운영에 나갈 수 있는 버전만 표시함.

## 깊이 이해
- **배경·문제의식**: 노트북과 파일 서버에 모델을 저장하면 어떤 버전이 운영 중인지, 어떤 데이터로 학습했는지, 누가 승인했는지 추적하기 어렵다.
- **작동 원리**: 모델 아티팩트, experiment ID, metric, dataset version, stage, approval, deployment target을 하나의 registry record로 묶음.
- **비유**: 의약품 출하처럼 생산 배치, 품질검사 결과, 승인자, 출하 일자를 기록한 제품만 현장에 공급하는 방식임.
- **구체 예시**: `fraud-model:v17`은 F1 0.91, PSI 0.12, 승인자 2명, staging 통과 후 production stage로 승격됨.
- **흔한 오해·주의점**: Model Registry는 파일 저장소가 아니라 모델을 운영으로 승격시키는 승인 게이트와 lineage 저장소임.

## 연결 개념
- Experiment Tracking — registry에 등록할 후보 모델의 실험 근거 제공
- MLOps — registry를 CI/CD/CT 파이프라인의 배포 기준으로 사용
- ModelOps — registry를 전사 모델 감사와 승인 체계에 연결

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Model Registry는 모델 아티팩트, 버전, 메타데이터, 지표, 승인 상태를 관리하는 운영 저장소임.
> 2. **가치**: 모델 재현성, 승인 배포, rollback, 감사 추적성을 확보함.
> 3. **판단 포인트**: registry는 artifact 저장만이 아니라 stage transition과 배포 gate를 함께 설계해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MLOps 구성요소 이해 확인 | artifact, version, stage, lineage, approval | 파일 저장소와 동일시 |
| 운영 배포 통제 확인 | staging, production, archive, rollback | 승인 절차와 지표 기준 누락 |
| 감사·재현성 판단 확인 | dataset version, code SHA, metric, owner | 모델명만으로 버전 관리 설명 |

> 요약: Model Registry 문제는 모델 파일 보관보다 어떤 버전이 왜 운영 승인됐는지 추적하는 구조를 묻는 문제임.

---

## Ⅰ. 개요 및 필요성

- 개요: 모델 버전 승인 저장소
- 배경: 모델 파일만 저장하면 학습 데이터, 코드, 평가 지표, 승인자, 운영 배포 이력을 추적하기 어렵다.
- 필요성: 운영 모델 lineage 100%, 승인 없는 production 배포 0건, rollback 10분 이하 기준이 필요함.

---

## Ⅱ. 구조 및 구성요소

```text
Experiment Run -> Model Artifact -> Model Registry
Model Registry -> Staging -> Production -> Archive
CI/CD Gate -> Registry Stage Check -> Deployment
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Model Artifact | 학습된 모델 파일과 환경 정보 저장 | pickle, ONNX, container |
| Metadata | dataset version, code SHA, hyperparameter 기록 | reproducibility |
| Stage | None, Staging, Production, Archive 상태 관리 | promotion control |
| Approval | owner와 reviewer 승인 기록 | audit log |
| Deployment Link | 운영 endpoint와 모델 버전 연결 | rollback 지원 |

> 요약: Model Registry는 모델 아티팩트와 운영 stage를 연결해 승인된 버전만 배포되도록 통제함.

---

## Ⅲ. 동작원리 및 흐름도

```text
실험 완료 -> 모델 등록 -> 지표 검증
-> staging 승인 -> production 승격 -> 운영 감시와 rollback
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 실험 결과에서 후보 모델과 artifact를 등록 | artifact checksum 기록 |
| 2 | dataset version, code SHA, metric을 메타데이터로 저장 | 필수 필드 100% |
| 3 | 검증 지표와 보안 스캔을 통과하면 staging 승격 | AUC/F1 목표 달성 |
| 4 | 승인자 확인 후 production stage로 전환 | 승인자 2인 이상 |
| 5 | 운영 지표 악화 시 이전 production 버전으로 rollback | rollback 10분 이하 |

> 요약: Model Registry는 실험 결과를 운영 후보로 승격하고 승인된 stage만 배포 파이프라인에 전달함.

---

## Ⅳ. 특징

| 구분 | 파일 저장소 | Model Registry | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 저장 대상 | 모델 파일 | artifact+metadata+stage | lineage 100% |
| 배포 통제 | 수동 경로 지정 | stage 기반 gate | 미승인 배포 0건 |
| 재현성 | 파일명 의존 | dataset·code·환경 기록 | 재학습 재현 가능 |
| 운영 대응 | 버전 확인 지연 | endpoint-version 연결 | rollback 10분 이하 |

> 요약: Model Registry는 모델 저장을 운영 승인과 rollback이 가능한 통제 구조로 확장함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | object storage 직접 배포 | registry stage 기반 배포 | 모델 배포 빈도 월 1회 이상 |
| 비용/성능 | 수동 승인 문서 | 자동 gate와 audit log | 배포 리드타임 1일 이하 목표 |
| 운영/위험 | 운영 버전 불명 | endpoint와 version 매핑 | 규제·감사 대상 모델 운영 시 |

> 요약: Model Registry는 모델 배포가 반복되고 운영 버전 추적이 필요한 환경에서 필수 운영 구성요소임.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 잘못된 모델 배포 | stage 확인 없이 artifact 직접 배포 | CI/CD에서 production stage만 허용 | stage bypass 0건 |
| 재현성 상실 | dataset과 code 정보 누락 | 필수 메타데이터 검증 | metadata completeness 100% |
| rollback 실패 | endpoint와 버전 매핑 부재 | blue/green과 previous version 보관 | rollback 10분 이하 |

> 요약: Registry 리스크는 stage 우회, 메타데이터 누락, rollback 불가이며 배포 게이트와 버전 매핑으로 줄임.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 추적성 | lineage 필드 100% | registry metadata audit |
| 배포 통제 | 승인 없는 production 0건 | CI/CD gate log |
| 복구 | 이전 버전 rollback 10분 이하 | deployment drill |

> 요약: Model Registry 성과는 추적성, 승인 통제, rollback 시간으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 모델 등록 시 artifact checksum, dataset version, code SHA, environment, metric, owner를 필수 메타데이터로 지정함.
2. CI/CD 배포 단계에서 registry stage가 production인 모델만 운영 endpoint에 배포되도록 정책을 설정함.
3. production 승격 시 이전 버전을 유지하고 blue/green 또는 canary로 rollback 10분 이하를 검증함.

**결론 (2줄):**
- 기술사 판단: 실험 단계는 artifact store로 시작할 수 있으나 운영 배포가 존재하면 Model Registry를 배포 게이트로 사용해야 함.
- 향후 방향: Model Registry는 LLM prompt registry, dataset registry, AI governance catalog와 통합된 AI asset registry로 발전함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Model Registry를 설명하시오" | 등록->승인->배포->rollback 흐름 | 파일 저장소 대비 차이 |
| 요구사항 명시형 | "모델 배포 통제 방안을 제시하시오" | stage gate와 CI/CD 연동 | lineage·approval·rollback 기준 |

> 요약: 설명형은 registry 구성, 방안형은 production stage 통제와 rollback 절차를 중심으로 작성함.
