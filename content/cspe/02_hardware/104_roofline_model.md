---
title: "루프라인 모델 (Roofline Model)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 104
---

## Ⅰ. 개요
- **정의**: 연산 강도 대비 달성 가능 성능 상한을 시각화하는 성능 분석 모델
- **배경/필요성**: 프로세서 성능이 연산 능력과 메모리 대역폭 중 어디에 병목이 있는지 정량적으로 판별할 수단이 필요함
- **비유**: 수도관(메모리 대역폭)과 물탱크(연산 능력) 중 좁은 쪽이 수도꼭지 유량을 결정하는 것과 유사함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 성능 병목 분석 능력 확인 | 연산 강도(OI) 기준 memory-bound/compute-bound 구분 | OI 단위(FLOP/Byte)와 축 로그 스케일 명시 필요 |

> 요약: 연산 강도 기준으로 메모리·연산 병목을 판별하는 시각적 성능 상한 모델임

## Ⅱ. 구성요소
```text
Performance(GFLOPS)
  |         ___________  <-- Peak Compute (ceiling)
  |        /
  |       /  <-- Memory Bandwidth slope
  |      /
  |     /
  |----+--- Operational Intensity (FLOP/Byte) -->
       ^
   Ridge Point
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Peak Compute | 프로세서 이론 최대 연산 처리량(GFLOPS) | 공장 최대 생산 능력 |
| Memory Bandwidth | 메모리에서 데이터를 전달하는 최대 속도(GB/s) | 원자재 공급 파이프 굵기 |
| Operational Intensity | 전송 바이트당 수행 연산 수(FLOP/Byte) | 원자재 1kg당 만드는 제품 수 |
| Ridge Point | memory-bound와 compute-bound 경계 지점 | 공급과 생산이 균형 잡히는 전환점 |

> 요약: 최대 연산량, 메모리 대역폭, 연산 강도, 분기점 4요소로 병목을 판별함

## Ⅲ. 절차
```text
HW spec 수집 --> OI 계산 --> Roofline 도식화 --> 병목 판별
```
- 1단계: 대상 HW의 Peak Compute(GFLOPS)와 Memory Bandwidth(GB/s) 측정
- 2단계: 대상 커널의 연산 강도(OI = 총 FLOP / 총 전송 Byte) 계산
- 3단계: 로그-로그 그래프에 대역폭 기울기선과 연산 상한선 도식화
- 4단계: 커널 OI를 그래프에 매핑하여 memory-bound 또는 compute-bound 판별

> 요약: HW 스펙 수집 후 OI를 계산하여 그래프상 병목 영역을 판별하는 4단계 절차임

## Ⅳ. 문제점
- memory-bound 과소평가: 캐시 계층 효과 미반영 — 실측 대역폭이 이론치와 괴리 발생
- 단일 병목 가정: 연산·메모리 외 네트워크·I/O 병목 표현 불가 — 분산 환경 적용 한계
- 정적 분석 한계: 런타임 동적 부하 변화 미반영 — 실 워크로드 예측 정확도 저하

> 요약: 캐시 미반영, 단일 병목 가정, 정적 분석 한계가 주요 문제임

## Ⅴ. 개선방안
1. 단기: Cache-Aware Roofline 적용으로 L1/L2/L3 각 계층별 대역폭 상한선 추가
2. 중기: 네트워크·I/O 축을 포함한 다차원 Roofline 확장 모델 도입
3. 장기: 런타임 프로파일링 연동 동적 Roofline 자동 생성 체계 구축

> 요약: 캐시 계층 반영, 다차원 확장, 동적 프로파일링 순으로 개선 필요

## Ⅵ. 전망
- 발전 방향: AI 가속기(GPU, NPU) 전용 Roofline 모델이 표준 벤치마크로 확산 중임
- 기술사적 판단: HW-SW 공동 최적화(Co-design) 시 성능 목표 설정의 핵심 도구로 자리잡을 전망임
- 기술사 제언: 설계 단계에서 Roofline 기반 병목 예측을 의무화하여 최적화 방향을 조기 확정할 필요
