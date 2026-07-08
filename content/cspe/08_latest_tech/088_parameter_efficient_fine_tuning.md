---
title: "Parameter-Efficient Fine-Tuning (PEFT)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 88
extra:
  question_no: "088"
  exam_status: "기출"
  exam_history: "135회, 136회"
---

## 미리 알고가기

- PEFT는 기반 모델 대부분을 고정하고 소수의 추가 파라미터만 학습하는 튜닝 방식의 총칭임
- LoRA, Adapter Tuning, Prefix Tuning이 대표 계열임
- 모델 복제 비용을 줄여 멀티테넌트 서비스와 빠른 실험에 유리함

## Ⅰ. 개요

- **정의/개념**: PEFT는 거대 모델의 기존 가중치는 유지한 채 적은 수의 학습 가능한 파라미터만 추가 또는 조정해 특정 업무에 적응시키는 비용 효율적 튜닝 기법군임
- **배경/필요성**: full fine-tuning은 GPU 메모리와 학습 시간과 모델 저장 비용이 커서 도메인별 반복 튜닝과 다수 고객 대응에 비효율적이므로, 경량 적응 방식이 필요함

## Ⅱ. 특징

- 학습 대상 파라미터 수가 적어 비용과 시간과 저장 공간을 크게 줄임
- 하나의 base model 위에 여러 adapter를 얹어 다수 업무를 분리 운영하기 쉬움
- full fine-tuning보다 표현력이 제한될 수 있어 복잡한 도메인 적응에서는 성능 한계가 있을 수 있음
- base model 버전과 강하게 결합되므로 운영 시 호환성과 버전 관리를 함께 설계해야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Full Fine-Tuning | PEFT | Prompt-only |
|:---|:---|:---|:---|
| 학습 비용 | 매우 큼 | 낮음 | 없음 |
| 저장 비용 | 매우 큼 | 낮음 | 없음 |
| 적응력 | 매우 높음 | 높음 | 제한적임 |
| 운영 유연성 | 낮음 | 높음 | 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Frozen Base Model | 범용 능력을 유지하며 대부분의 연산과 표현을 담당함 |
| Trainable PEFT Module | LoRA, adapter, prefix 같은 소형 파라미터 집합이 도메인 적응을 담당함 |
| Optimizer, Scheduler | 적은 파라미터만 안정적으로 업데이트해 빠른 수렴과 비용 절감을 유도함 |
| Adapter Registry | 업무별 모듈을 분리 저장하고 배포 시 필요한 모듈만 로딩하게 함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| base 모델 고정  | --> | 소형 모듈 부착   | --> | 선택 파라미터 학습 | --> | 모듈별 배포/전환 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **base 모델 고정**: 대부분의 가중치를 freeze해 비용을 제한함
2. **소형 모듈 부착**: 업무 목적에 맞는 adapter나 LoRA 모듈을 추가함
3. **선택 파라미터 학습**: 적은 수의 파라미터만 업데이트해 도메인 적응을 수행함
4. **모듈별 배포 및 전환**: 업무별 모듈을 필요할 때 교체하거나 병행 운영함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 적응 가능한 파라미터가 너무 적으면 복잡한 업무 규칙이나 깊은 도메인 추론을 충분히 반영하지 못할 수 있음
   - 해결방안: LoRA rank나 adapter 크기를 업무별로 조정하고 trainable parameter ratio와 domain score로 적합성을 검증함
2. 문제: 업무별 adapter가 늘어나면 관리 대상이 많아져 버전 충돌과 배포 혼선이 생길 수 있음
   - 해결방안: adapter registry와 표준 메타데이터를 운영하고 deployment failure rate와 adapter switch latency로 운영성을 검증함
3. 문제: base model이 바뀌면 기존 PEFT 모듈을 재사용하지 못해 자산 호환성이 떨어질 수 있음
   - 해결방안: base model 버전 정책을 고정하고 migration lead time과 compatibility pass rate로 교체 비용을 검증함

## Ⅶ. 적용 사례

- 기업별 맞춤 챗봇: 고객사별 adapter를 분리 운영함, 확인 지표는 storage saving과 tenant isolation임
- 빠른 실험 튜닝: 다양한 프롬프트 스타일을 저비용으로 검증함, 확인 지표는 experiment turnaround time과 benchmark score임
- 온프레미스 소형 모델 적응: 제한된 GPU로 도메인 튜닝을 수행함, 확인 지표는 training cost와 domain accuracy임

## Ⅷ. 결론

PEFT는 거대 모델을 여러 업무와 고객 환경에 현실적으로 확장하게 만드는 핵심 튜닝 전략이므로, 적응 성능과 운영 모듈 관리를 함께 고려해 선택해야 함.
