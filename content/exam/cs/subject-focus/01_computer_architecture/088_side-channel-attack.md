---
title: "사이드채널공격 (Side-Channel Attack)"
date: "2026-06-30"
weight: 88
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 사이드채널공격(Side-Channel Attack)은 암호 알고리즘 자체가 아닌 실행 중 발생하는 부수정보(시간·전력·캐시·전자파)를 분석해 비밀정보를 유추하는 공격이다.

## Ⅱ. 구성요소 / 원리
- 유형: 타이밍, 전력분석(SPA/DPA), 캐시(Flush+Reload), 전자파
- Spectre: 분기예측 추측실행을 악용해 권한 외 데이터 누출
- Meltdown: 비순차 실행으로 커널 메모리 무단 읽기
- Rowhammer: DRAM 반복접근으로 인접 행 비트 플립 유발

## Ⅲ. 흐름도 / 구조
```text
[추측실행/캐시 흔적] → 부수정보 측정(시간·전력)
        │
        ▼
 [통계 분석] → 비밀키/메모리 데이터 복원
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적(공격) | 물리적 부수정보로 기밀 추출 |
| 위협 | 암호키 유출, 격리 우회, 권한 상승 |
| 대응 | 상수시간 구현, KPTI, 마이크로코드 패치, TRR/ECC |

## Ⅴ. 기술사적 적용
- Spectre/Meltdown: CPU 추측실행 보안 패러다임 전환 계기
- Rowhammer: DDR5 TRR·On-die ECC로 완화
- TEE·기밀컴퓨팅 설계 시 사이드채널 내성 고려 필수
