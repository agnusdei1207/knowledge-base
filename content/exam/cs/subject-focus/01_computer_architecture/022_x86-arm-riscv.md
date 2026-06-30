---
title: "x86·ARM·RISC-V (대표 ISA 비교)"
date: "2026-06-30"
weight: 22
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 현대 컴퓨팅을 대표하는 세 가지 명령어집합구조(ISA)로, x86은 CISC 기반 PC·서버, ARM은 RISC 기반 저전력 모바일, RISC-V는 개방형(Open) RISC ISA이다.

## Ⅱ. 구성요소 / 원리
- x86(Intel/AMD): CISC, 가변길이, 강력한 하위호환, 내부 μop 변환
- ARM: RISC, 고정/Thumb 가변, 저전력 설계, 라이선스(IP) 모델
- RISC-V: 개방형 RISC, 모듈형 확장(RV32I/64 + M/A/F/D/C), 로열티 무료
- 공통: Load-Store(ARM/RISC-V) vs 메모리연산(x86) 차이

## Ⅲ. 흐름도 / 구조
```text
 x86    : CISC 외피 →(내부)→ RISC μop 실행 [PC/서버]
 ARM    : RISC 고정포맷 → 저전력 파이프라인 [모바일/임베디드]
 RISC-V : Base ISA + 선택적 확장모듈(M,A,F,D,C) [개방형]
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | x86:호환성 / ARM:전력효율 / RISC-V:개방·맞춤화 |
| 장점 | x86:생태계 / ARM:저전력·성숙IP / RISC-V:무료·확장자유 |
| 한계 | x86:전력·라이선스 / ARM:라이선스비용 / RISC-V:생태계 미성숙 |

## Ⅴ. 기술사적 적용
- 애플 M시리즈·Ampere(ARM) 데이터센터 진출로 x86 독점 약화
- RISC-V: AI 가속기·IoT·맞춤형 SoC에 채택 확대
- ISA 주권·공급망(개방형 표준) 측면에서 RISC-V 전략적 부상
