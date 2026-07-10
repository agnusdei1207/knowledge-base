---
title: 소프트웨어 신뢰성 및 가용성 (Reliability and Availability)
date: 2026-07-05
tags: ["cspe-software"]
weight: 190
---

## Ⅰ. 개요
- 정의: 시스템이 주어진 환경과 기간에 고장 없이 기능을 수행할 확률(신뢰성)과 서비스 가능한 시간의 비율(가용성)
- 배경: 미션 크리티컬 시스템의 중단 없는 서비스 제공 및 장애 내성 확보
| 구분 | 내용 |
|------|------|
| 출제 의도 | MTBF, MTTR 지표의 의미와 99.999%(Five-Nines) 가용성 전략 이해 |

## Ⅱ. 구성요소
  [ Up-time ] | [ Down-time ] | [ Up-time ]
  <-- MTBF --> | <-- MTTR --> |
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| MTBF | 고장 사이의 평균 시간 (신뢰성 지표) | 수명 |
| MTTR | 수리 완료까지의 평균 시간 (유지보수성 지표) | 수리 속도 |
| Availability | MTBF / (MTBF + MTTR) (가용성 비율) | 가동률 |
> 요약: MTBF와 MTTR을 기준으로 고장 간격과 복구 시간을 관리하여 가용성을 산정함

## Ⅲ. 절차
  Design Fault Tolerance -> Monitor -> Detect -> Recover
1. Designing: 이중화, 클러스터링을 통한 단일 장애점(SPOF) 제거
2. Monitoring: 실시간 헬스 체크 및 임계치 기반 이상 탐지
3. Failover: 장애 감지 후 예비 시스템으로 자동 전환
4. Root Cause Analysis: 장애 원인 분석 및 재발 방지 대책 반영
> 요약: 사전 예방적 설계와 사후 자동 복구 메커니즘의 결합

## Ⅳ. 문제점
- 가용성 목표가 높아질수록 이중화·운영·검증 비용 증가
- 복잡한 분산 환경에서의 연쇄 장애(Cascading Failure) 예측 난해

## Ⅴ. 개선방안
- 카오스 엔지니어링을 통한 장애 주입 및 회복력 테스트
- 서킷 브레이커 및 격리(Bulkhead) 패턴 적용으로 장애 전이 방지

## Ⅵ. 전망
- AI-Ops 기반의 선제적 장애 예측 및 자동 자가 치유(Self-healing) 인프라 보편화
