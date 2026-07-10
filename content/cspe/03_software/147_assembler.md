---
title: 어셈블러 및 기계어 (Assembler)
date: 2026-07-05
tags: [cspe-software]
weight: 147
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 기계어와 1:1 매핑되는 저급 언어를 실제 이진 코드로 변환하는 프로그램 |
| 필요성 | ISA 명령·register·addressing mode를 직접 지정하는 boot code·driver·context switch 구현 |
| 출제 의도 | 2-Pass 어셈블러 작동 원리, 니모닉(Mnemonic) 매핑 이해 측정 |

## Ⅱ. 구성요소
```text
[ Assembly Source ]       [ Machine Code ]
MOV EAX, 1          --->  B8 01 00 00 00
ADD EAX, EBX        --->  01 D8
(Mnemonic/Operand)        (Opcode/Address)
```
| 구성요소 | 설명 | 변환 기준 |
|---|---|---|
| 니모닉 | ISA opcode를 사람이 작성하는 instruction symbol로 표현함 | opcode mapping |
| 오피코드 (Opcode) | CPU가 decode할 operation bit field임 | instruction encoding |
| 기호 표 (Symbol Table) | label·constant와 address·value를 기록함 | forward reference resolution |
> 요약: 기계어는 하드웨어가 실행하는 0과 1의 조합이며, 어셈블리어는 그 기호 표현임.

## Ⅲ. 절차 (2-Pass Assembler)
```text
Pass 1: Scan Source -> Build Symbol Table -> Process Pseudo-ops
Pass 2: Scan Again -> Translate Mnemonic to Opcode -> Generate Object
```
1. 패스 1 (기호 정의): 모든 기호(Label)의 주소를 계산하여 심볼 테이블에 저장.
2. 가상 명령 처리: 데이터 정의(DB, DW) 등 어셈블러 지시어 처리.
3. 패스 2 (번역): 니모닉을 오피코드로, 기호를 실제 주소값으로 변환.
4. 목적 파일 생성: 변환된 이진 코드와 로더를 위한 재배치 정보를 기록.
> 요약: 두 번 훑는 과정을 통해 전방 참조(Forward Reference) 문제를 해결함.

## Ⅳ. 문제점
- 기계 아키텍처(x86, ARM)에 종속적이어서 이식성이 전혀 없음.
- 소스 코드가 매우 길어지고 복잡해져 유지보수 및 디버깅 비용이 기하급수적 상승.

## Ⅴ. 개선방안
- 매크로 어셈블러를 사용하여 반복되는 코드 뭉치를 구조화 및 추상화.
- 인라인 어셈블리(C/C++ 내 삽입)를 통해 필요한 부분만 국소적으로 최적화.

## Ⅵ. 전망
- 보안 분석: 악성코드 리버싱 및 취약점 탐지 분야에서 어셈블리 분석 기술 고도화.
- 특수 목적 최적화: 임베디드 AI 칩 최적 연산을 위한 커스텀 명령어셋(ISA) 개발 활발.
