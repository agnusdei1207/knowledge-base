---
title: "토마술로 알고리즘 (Tomasulo's Algorithm)"
date: "2026-06-30"
weight: 35
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 예약국과 공통 데이터 버스(CDB)를 이용해 레지스터 리네이밍과 동적 스케줄링을 수행하는 비순차실행 알고리즘으로, IBM 360/91에서 유래했다.

## Ⅱ. 구성요소 / 원리
- 예약국(Reservation Station): 명령·피연산자/태그(Qj,Qk) 버퍼링
- 레지스터 상태(Register Status): 각 레지스터를 생산할 예약국 태그 기록
- CDB(Common Data Bus): 연산 결과를 전 예약국·레지스터에 브로드캐스트
- 분산 제어로 RAW는 태그 대기, WAR·WAW는 리네이밍으로 제거
- 단계: 발행(Issue)→실행(Execute)→기록(Write Result)

## Ⅲ. 흐름도 / 구조
```text
Issue ─▶ Reservation Station(Qj,Qk 대기)
              │ 피연산자 준비
              ▼
           Execute ─▶ CDB 브로드캐스트 ─▶ RS/레지스터 갱신
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 가짜 의존성 제거·동적 스케줄링으로 ILP 향상 |
| 장점 | 컴파일러 도움 없이 하드웨어가 OoO 수행 |
| 한계 | CDB 경합·하드웨어 복잡, 정밀 예외 미보장(ROB 보완) |

## Ⅴ. 기술사적 적용
- ROB를 추가해 정밀 예외·투기실행 지원, 현대 OoO 코어의 원형
- 레지스터 리네이밍·예약국 개념의 효시로 슈퍼스칼라 설계 토대
