---
title: "Adapter Tuning (어댑터 튜닝)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 91
extra:
  question_no: "091"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- adapter tuning은 각 레이어 사이에 작은 병목 모듈을 추가해 적은 파라미터만 학습하는 PEFT 방식임
- base model은 고정하고 adapter만 교체해 다양한 업무를 분리 운영할 수 있음
- LoRA보다 구조 변경이 더 명시적이어서 추론 오버헤드와 모듈 관리 비용을 함께 봐야 함

## Ⅰ. 개요

- **정의/개념**: adapter tuning은 사전학습된 모델 계층 사이에 작은 bottleneck 모듈을 삽입하고 이 모듈만 학습해 특정 업무에 적응시키는 PEFT 기법임
- **배경/필요성**: full fine-tuning은 저장 비용이 크고 모델 복제가 많아지므로, 업무별 적응 정보를 작은 모듈로 분리해 재사용하는 방식이 필요함

## Ⅱ. 특징

- 적은 학습 비용으로 도메인별 모델 변형을 분리 관리할 수 있음
- base model을 공유하므로 멀티테넌트 운영과 빠른 전환에 유리함
- adapter 삽입으로 인해 추론 경로가 길어져 LoRA보다 오버헤드가 생길 수 있음
- 어떤 레이어에 어떤 크기의 adapter를 넣을지가 품질과 비용을 함께 결정함

## Ⅲ. 종류 및 비교

| 판단 기준 | Full FT | Adapter Tuning | LoRA |
|:---|:---|:---|:---|
| 학습 비용 | 매우 큼 | 낮음 | 낮음 |
| 구조 변경 | 없음 | 있음 | 적음 |
| 추론 오버헤드 | 없음 | 중간 | 낮음 |
| 업무별 모듈화 | 낮음 | 높음 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Frozen Base Layers | 범용 표현력을 유지하며 대부분의 계산을 담당함 |
| Adapter Bottleneck | 축소와 확장을 통해 적은 파라미터로 업무 적응 정보를 담음 |
| Task-specific Modules | 업무나 고객별 adapter를 분리 저장해 재사용성과 격리를 확보함 |
| Adapter Manager | 어떤 adapter를 언제 로딩할지 제어해 서비스 전환과 배포를 관리함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| base 모델 고정  | --> | adapter 삽입    | --> | adapter만 학습   | --> | 모듈 선택 배포   |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **base 모델 고정**: 원래 가중치는 변경하지 않음
2. **adapter 삽입**: 선택한 레이어 사이에 작은 병목 모듈을 추가함
3. **adapter만 학습**: 새 모듈만 업데이트해 도메인 적응을 수행함
4. **모듈 선택 배포**: 업무별 adapter를 로딩해 같은 base model 위에서 서비스함

## Ⅵ. 문제점 및 해결 방안

1. 문제: adapter 크기가 너무 작으면 적응 효과가 부족하고 너무 크면 비용과 오버헤드 이점이 줄어들 수 있음
   - 해결방안: bottleneck size를 업무별로 조정하고 parameter count와 validation score로 적정 크기를 검증함
2. 문제: adapter를 여러 개 관리하면 버전 충돌과 서비스 선택 실수가 발생할 수 있음
   - 해결방안: adapter registry와 표준 메타데이터를 운영하고 deployment failure rate와 switch latency로 운영성을 검증함
3. 문제: 추론 시 adapter 경로가 추가되면 고성능 실시간 서비스에서 지연이 누적될 수 있음
   - 해결방안: 지연 민감 서비스는 LoRA와 비교 검토하고 p95 latency와 throughput으로 경로 적합성을 검증함

## Ⅶ. 적용 사례

- 고객사별 응답 정책 분리: 같은 base model 위에 고객별 adapter를 운영함, 확인 지표는 tenant switch latency와 storage saving임
- 문서 분류 전용 모델: 업무별 adapter를 빠르게 바꿔 실험함, 확인 지표는 experiment turnaround time과 accuracy임
- 온프레미스 챗봇: 제한된 자원에서 도메인 적응을 수행함, 확인 지표는 training cost와 answer quality임

## Ⅷ. 결론

adapter tuning은 업무별 모델 적응을 작은 모듈로 분리하는 데 강점이 있으므로, 품질 향상뿐 아니라 추론 오버헤드와 모듈 운영 비용까지 함께 평가해야 함.
