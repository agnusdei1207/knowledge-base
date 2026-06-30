---
title: "분기예측 (Branch Prediction: 정적·동적·BTB·BHT)"
date: "2026-06-30"
weight: 31
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 분기 명령의 결과(Taken/Not-Taken)와 목적지를 미리 예측하여 제어 해저드로 인한 파이프라인 공백을 줄이는 기법이다.

## Ⅱ. 구성요소 / 원리
- 정적(Static) 예측: 항상 Taken/Not-Taken, 백워드-Taken 등 고정 규칙
- 동적(Dynamic) 예측: 실행 이력 기반, BHT의 1/2비트 포화 카운터 사용
- BHT(Branch History Table): 분기 결과 이력 저장
- BTB(Branch Target Buffer): 분기 목적지 주소 캐시 → IF 단계 조기 인출
- 오예측 시 파이프라인 플러시(flush) 후 재인출

## Ⅲ. 흐름도 / 구조
```text
IF ─▶ [BTB/BHT 조회] ─ Taken? ─Y─▶ 목적지 주소로 인출
                          │
                          └─N─▶ PC+1 순차 인출
   예측 적중 ⇒ 공백 0 / 오예측 ⇒ flush 후 정정
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 제어 해저드의 분기 페널티 최소화 |
| 장점 | 적중률↑ 시 파이프라인 공백 제거 |
| 한계 | 오예측 시 플러시 비용, 표 저장 하드웨어 비용 |

## Ⅴ. 기술사적 적용
- 2비트 포화 카운터·상관(Correlating)·gshare·TAGE 등 고정밀 예측기로 발전
- 슈퍼스칼라·깊은 파이프라인에서 적중률이 IPC를 좌우하는 핵심 요소
