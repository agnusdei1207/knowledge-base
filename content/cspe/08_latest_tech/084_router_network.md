---
title: "Router Network (라우터 네트워크)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 84
extra:
  question_no: "084"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- router network는 MoE에서 입력 토큰을 어떤 expert로 보낼지 결정하는 경량 게이팅 계층임
- 선택 정확도와 부하 균형을 동시에 만족해야 하므로 단순 분류기 이상의 운영 의미를 가짐
- top-k 선택 방식과 auxiliary loss가 router 품질을 좌우함

## Ⅰ. 개요

- **정의/개념**: router network는 입력 토큰의 은닉 표현을 바탕으로 expert별 점수를 계산하고, 상위 expert를 선택해 토큰 분배를 수행하는 MoE의 제어 계층임
- **배경/필요성**: expert 수가 많아질수록 어떤 expert를 활성화할지 잘못 고르면 모델 품질과 병렬 효율이 동시에 무너지므로, 정확하고 균형 잡힌 분배기가 필요함

## Ⅱ. 특징

- 매우 가벼운 연산으로 expert 선택을 수행하지만 전체 MoE 품질과 비용 구조를 좌우함
- top-1, top-2 같은 라우팅 정책에 따라 계산량과 품질과 통신량이 달라짐
- 특정 expert 쏠림을 막기 위한 load balancing 손실과 capacity 제어가 중요함
- router 불안정성은 dead expert, token drop, latency 상승으로 직접 이어질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Hash Routing | Top-1 Router | Top-2 Router |
|:---|:---|:---|:---|
| 선택 방식 | 규칙 기반 | 학습 기반 1개 선택 | 학습 기반 2개 선택 |
| 품질 잠재력 | 낮음 | 높음 | 더 높음 |
| 계산/통신 비용 | 낮음 | 낮음 | 중간 |
| 부하 제어 난도 | 낮음 | 높음 | 매우 높음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Scoring Layer | 토큰 표현을 expert 수만큼의 점수로 변환해 분배의 기초 정보를 생성함 |
| Softmax, Top-k Selector | 확률 분포를 만들고 실제 활성 expert를 선택해 계산량을 제한함 |
| Capacity Controller | expert별 허용 토큰 수를 관리해 쏠림과 과부하를 완화함 |
| Auxiliary Loss | 균형 잡힌 분배를 유도해 dead expert와 training collapse를 방지함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 토큰 표현 입력  | --> | expert 점수 계산 | --> | top-k 및 용량 검사 | --> | expert로 분배    |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **토큰 표현 입력**: shared layer 출력을 router가 입력으로 받음
2. **expert 점수 계산**: 각 expert에 대한 적합도 logits를 계산함
3. **top-k 및 용량 검사**: 상위 expert를 선택하고 capacity 초과 여부를 확인함
4. **expert로 분배**: 선택된 expert로 토큰을 전달하고 결과를 다시 결합함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 학습 초기에 우연히 선택된 expert로 토큰이 계속 몰리면 나머지 expert가 충분히 학습되지 못해 dead expert가 생길 수 있음
   - 해결방안: load balancing loss와 routing noise를 적용하고 expert utilization entropy와 dead expert ratio로 균형을 검증함
2. 문제: 특정 expert에 토큰이 과도하게 몰리면 capacity 초과로 일부 토큰이 drop되어 품질 저하와 tail latency 상승이 발생할 수 있음
   - 해결방안: capacity factor와 fallback 정책을 조정하고 token drop rate와 p99 latency로 안정성을 검증함
3. 문제: router 자체가 과도하게 복잡해지면 MoE의 계산 절감 효과를 일부 상쇄할 수 있음
   - 해결방안: 경량 router 구조를 유지하고 routing overhead ratio와 throughput으로 제어 비용을 검증함

## Ⅶ. 적용 사례

- 대형 MoE 학습: top-2 routing으로 품질을 높임, 확인 지표는 benchmark score와 utilization balance임
- 비용 민감 추론 서비스: top-1 routing으로 계산량을 제한함, 확인 지표는 cost per token과 latency임
- 멀티도메인 expert 실험: 분야별 expert 선택 패턴을 분석함, 확인 지표는 domain routing entropy와 task accuracy임

## Ⅷ. 결론

router network는 MoE의 부가 요소가 아니라 expert 선택 품질과 시스템 효율을 동시에 결정하는 핵심 제어 계층이므로, 정확도보다 균형과 운영성까지 포함해 설계해야 함.
