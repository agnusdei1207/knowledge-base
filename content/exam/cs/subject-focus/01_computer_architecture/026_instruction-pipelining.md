---
title: "명령어 파이프라이닝 (Instruction Pipelining: IF·ID·EX·MEM·WB)"
date: "2026-06-30"
weight: 26
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 명령어 처리 단계를 여러 스테이지로 분할하고 서로 다른 명령어를 중첩 수행하여 단위 시간당 처리량(Throughput)을 높이는 기법이다.

## Ⅱ. 구성요소 / 원리
- IF(Instruction Fetch): 명령어 인출
- ID(Instruction Decode): 해독 및 레지스터 읽기
- EX(Execute): ALU 연산·유효주소 계산
- MEM(Memory Access): 메모리 적재/저장
- WB(Write Back): 결과를 레지스터에 기록
- 단계 간 파이프라인 레지스터로 데이터·제어신호 전달

## Ⅲ. 흐름도 / 구조
```text
Cycle :  1    2    3    4    5    6    7
I1    : IF   ID   EX   MEM  WB
I2    :      IF   ID   EX   MEM  WB
I3    :           IF   ID   EX   MEM  WB
        └ 매 클럭 1명령어 완료(이상적 CPI≈1)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 명령어 중첩 수행으로 처리량 향상 |
| 장점 | 클럭당 명령어 완료, 자원 활용 극대화 |
| 한계 | 해저드 발생, 단계 지연으로 레이턴시 자체는 미감소 |

## Ⅴ. 기술사적 적용
- 단계 세분화로 슈퍼파이프라인(예: 10단 이상) 구현, 클럭 향상
- 해저드 대응으로 포워딩·분기예측·스톨 기법과 결합, 슈퍼스칼라로 확장
