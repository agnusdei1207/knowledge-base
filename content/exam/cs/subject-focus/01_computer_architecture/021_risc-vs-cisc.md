---
title: "RISC vs CISC (Reduced/Complex Instruction Set Computer)"
date: "2026-06-30"
weight: 21
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> RISC(축소명령어집합컴퓨터)는 단순·고정길이 명령어를 빠르게 실행하는 설계 철학이고, CISC(복합명령어집합컴퓨터)는 하나의 명령으로 복잡한 작업을 수행하는 다기능·가변길이 명령어 구조이다.

## Ⅱ. 구성요소 / 원리
- RISC: 고정길이 명령, Load-Store 구조, 다수 레지스터, 1명령=1사이클 지향
- CISC: 가변길이 명령, 메모리 직접 연산, 마이크로코드, 복잡한 주소지정
- RISC는 IC(명령어 수)↑·CPI↓, CISC는 IC↓·CPI↑ (성능방정식 트레이드오프)
- 현대 x86: CISC 명령을 내부 마이크로옵(μop, RISC형)으로 변환 실행

## Ⅲ. 흐름도 / 구조
```text
 RISC: 명령 →[고정포맷·디코드 단순]→ 파이프라인 →실행(1cyc)
 CISC: 명령 →[가변포맷·마이크로코드 해석]→ 복합실행(다cyc)
 현대 x86 = CISC 외피 + 내부 μop(RISC) 변환
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | RISC: 단순·고속 파이프라인 / CISC: 코드밀도·하위호환 |
| 장점 | RISC: 저전력·고효율 / CISC: 적은 명령수·메모리 절약 |
| 한계 | RISC: 코드량↑ / CISC: 디코드 복잡·전력↑ |

## Ⅴ. 기술사적 적용
- RISC: ARM·RISC-V·MIPS (모바일·임베디드·서버 확산)
- CISC: x86/x64 (PC·서버 레거시 호환)
- 경계 모호화: x86 내부 RISC화, 애플 M시리즈(ARM) 데스크톱 진입
