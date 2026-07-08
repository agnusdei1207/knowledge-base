---
title: "Token Throughput 토큰 처리량 (Token Throughput)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 63
extra:
  question_no: "063"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Throughput은 단위 시간당 시스템이 처리한 총 토큰 수를 의미함
- 요청당 latency와 전체 throughput은 종종 상충하는 운영 지표임
- Prefill, decode 비중에 따라 같은 throughput 수치라도 사용자 경험은 다를 수 있음

## Ⅰ. 개요

- **정의/개념**: Token Throughput은 LLM 서빙 시스템이 초당 처리하는 전체 토큰 수를 나타내는 생산성 지표로, GPU 자원 활용과 동시 요청 처리 능력을 평가하는 핵심 메트릭임
- **배경/필요성**: 개별 요청 속도만으로는 다수 사용자 환경의 시스템 생산성을 알기 어려우므로, 모델 서빙 엔진이 얼마나 많은 토큰을 안정적으로 처리하는지 측정할 지표가 필요함

## Ⅱ. 특징

- GPU utilization과 scheduler 효율과 batch 정책의 영향을 직접 반영함
- latency와는 별개로 전체 인프라 생산성 관점에서 중요함
- prefill-heavy workload와 decode-heavy workload는 동일 throughput이어도 체감이 다를 수 있음
- 비용 산정과 capacity planning의 기초 지표로 활용됨

## Ⅲ. 종류 및 비교

| 판단 기준 | TTFT | TPOT | Token Throughput |
|:---|:---|:---|:---|
| 측정 관점 | 요청 시작 지연 | 토큰당 출력 지연 | 전체 시스템 생산성 |
| 단위 | ms | ms/token | tokens/sec |
| 최적화 초점 | prefill 병목 | decode 병목 | 자원 활용률 |
| 대표 활용 | UX 관리 | 스트리밍 품질 | 용량 계획 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Request Mix | 입력 길이와 출력 길이와 요청 난도가 throughput 수치를 좌우하는 작업 부하 구성임 |
| Scheduler | batch 구성과 요청 순서를 조정해 동일 자원으로 더 많은 토큰을 처리하게 함 |
| Execution Engine | attention kernel과 decode loop를 실행해 실제 토큰 처리량을 결정함 |
| Capacity Monitor | GPU utilization과 queue length를 함께 관찰해 병목 구간을 식별함 |

```text
+------------------+     +------------------+     +------------------+     +------------------+
| Request Mix      | --> | Scheduler        | --> | Execution Engine | --> | Capacity Monitor |
+------------------+     +------------------+     +------------------+     +------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 요청 유입    | --> | 배치 구성    | --> | 토큰 실행    | --> | 처리량 집계  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **요청 유입**: 다양한 길이와 난도의 요청이 시스템에 들어옴
2. **배치 구성**: 스케줄러가 GPU 활용률을 높이도록 배치를 조직함
3. **토큰 실행**: prefill과 decode 연산을 수행해 실제 토큰을 처리함
4. **처리량 집계**: 일정 시간 동안 처리된 전체 토큰 수를 계산해 throughput을 산출함

## Ⅵ. 문제점 및 해결 방안

1. 문제: throughput만 극대화하면 긴 배치와 큰 큐 때문에 개별 사용자 latency가 커져 인터랙티브 서비스 품질이 떨어질 수 있음
   - 해결방안: throughput과 p95 latency를 함께 SLA로 관리하고 workload별 QoS 정책으로 균형을 검증함
2. 문제: prefill-heavy 요청이 몰리면 decode 중심 throughput 수치만으로는 실제 병목을 제대로 설명하지 못할 수 있음
   - 해결방안: prefill tokens/sec와 decode tokens/sec를 분리 측정하고 단계별 GPU utilization로 병목을 검증함
3. 문제: benchmark 환경의 높은 throughput이 실제 운영 환경의 혼합 요청 패턴과 다르면 capacity planning이 빗나갈 수 있음
   - 해결방안: production-like workload replay를 수행하고 benchmark 대비 실서비스 throughput gap으로 계획 정확도를 검증함

## Ⅶ. 적용 사례

- API 서버 용량 계획: GPU 수와 동시 사용자 수를 산정함, 확인 지표는 tokens/sec와 queue length임
- 내부 문서 분석 배치: 대용량 오프라인 작업 처리량을 평가함, 확인 지표는 batch completion time과 throughput임
- 실시간 챗봇 운영: latency와 throughput 균형을 조정함, 확인 지표는 p95 latency와 tokens/sec임

## Ⅷ. 결론

Token Throughput은 시스템이 얼마나 빨리 일하는지를 보여주지만 단독 지표로는 충분하지 않으므로 TTFT와 TPOT과 함께 해석해야 실서비스 설계에 의미가 생김.
