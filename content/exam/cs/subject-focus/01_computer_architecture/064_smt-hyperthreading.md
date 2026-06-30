---
title: "동시멀티스레딩 (SMT, Simultaneous Multithreading / Hyper-Threading)"
date: "2026-06-30"
weight: 64
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 단일 물리 코어에서 다수 스레드를 동시에 실행해 유휴 실행유닛을 채우는 기술로, 인텔의 구현이 하이퍼스레딩(Hyper-Threading).

## Ⅱ. 구성요소 / 원리
- 스레드별 아키텍처 상태(레지스터·PC) 복제, 실행유닛은 공유
- 한 사이클에 복수 스레드 명령을 동시 발행(issue)
- 한 스레드 스톨(캐시미스) 시 다른 스레드가 유닛 활용
- 논리 코어(Logical Core)로 OS에 노출

## Ⅲ. 흐름도 / 구조
```text
Thread A ─┐
Thread B ─┴→ [공유 실행유닛: ALU/FPU/Load] 동시 발행
   stall시 상대 스레드가 빈 슬롯 채움 → 활용률↑
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 실행유닛 활용률 향상으로 처리량 증대(저비용 TLP) |
| 장점 | 작은 면적·전력으로 처리량↑, 지연 은닉 |
| 한계 | 자원 경쟁 시 효과 감소, 캐시 공유 보안 이슈(사이드채널) |

## Ⅴ. 기술사적 적용
- Intel Hyper-Threading, IBM POWER(SMT4/8), AMD SMT
- 멀티코어와 결합해 코어×스레드 처리량 확대
- 보안: L1TF·MDS 등 취약점 대응으로 일부 환경 비활성화
