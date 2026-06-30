---
title: "주소지정방식 (Addressing Mode)"
date: "2026-06-30"
weight: 20
tags:
  - "exam-cspe-computer-architecture"
---

## Ⅰ. 정의
> 명령어가 피연산자(operand)의 위치(실효주소, Effective Address)를 지정하는 방법으로, 명령어 길이·유연성·메모리 접근 효율을 결정한다.

## Ⅱ. 구성요소 / 원리
- 즉치(Immediate): 피연산자가 명령어 내 상수
- 직접(Direct): 명령어에 실효주소 직접 명시
- 간접(Indirect): 주소가 가리키는 곳에 실제 주소 저장
- 레지스터/레지스터 간접: 레지스터에 값 또는 주소 보관
- 변위(Displacement)·인덱스·상대(PC-relative)·베이스 방식

## Ⅲ. 흐름도 / 구조
```text
 즉치   : Operand = 명령어내 상수
 직접   : EA = 주소필드 → Memory[EA]
 간접   : EA = Memory[주소필드] → Memory[EA]
 레지스터: Operand = Reg[R]
 변위   : EA = Reg[Base] + 명령어내 offset
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 다양한 데이터 접근 패턴(배열·포인터·스택)을 효율 표현 |
| 장점 | 코드 밀도·유연성↑, 고급언어 구조 사상 용이 |
| 한계 | 방식 多 → 디코딩 복잡·CPI↑ (CISC 특징) |

## Ⅴ. 기술사적 적용
- CISC: 다양·복잡한 주소지정 / RISC: Load-Store 중심 소수 방식
- 배열·구조체 접근에 인덱스·변위 방식 활용
- ISA 설계 시 명령어 형식·길이와 직접 연계
