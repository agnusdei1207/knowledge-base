---
title: "SPEC 벤치마크 (SPEC, Standard Performance Evaluation Corporation Benchmark)"
date: "2026-06-30"
weight: 18
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> SPEC(표준성능평가협회)이 제정한 표준화된 워크로드 모음으로, 서로 다른 시스템의 CPU·메모리·전력 성능을 실제 응용 기반으로 객관 비교하는 벤치마크이다.

## Ⅱ. 구성요소 / 원리
- SPEC CPU(예: CPU2017): 정수(SPECint)·부동소수점(SPECfp) 성능
- Rate(처리량) vs Speed(단일 작업 지연) 측정 방식
- 기준 시스템 대비 상대 성능비를 기하평균으로 산출
- SPECjbb(Java), SPECpower(전력효율), SPECvirt 등 도메인별 제품군

## Ⅲ. 흐름도 / 구조
```text
 실제 응용 워크로드 모음
        │ 컴파일·실행
        ▼
 측정 시간 → 기준기 대비 비율 → 기하평균
        ▼
 SPECspeed / SPECrate 점수 (정수·부동소수점)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 실제 워크로드 기반 시스템 성능 객관·재현 비교 |
| 장점 | 표준화·공신력, 컴파일러·시스템 종합 평가 |
| 한계 | 특정 워크로드 편향, 벤치마크 최적화(치팅) 가능성 |

## Ⅴ. 기술사적 적용
- MIPS·FLOPS의 한계를 보완하는 실측 종합 지표
- CPU·서버 도입 시 성능/전력효율(SPECpower) 비교 근거
- TPC(트랜잭션), LINPACK(TOP500)과 함께 분야별 표준 벤치마크
