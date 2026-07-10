---
title: 함수 및 서브루틴 — 스택 프레임 (Functions Stack Frame)
date: 2026-07-05
tags: [cspe-software]
weight: 153
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 함수 호출 시 해당 함수의 매개변수, 로컬 변수, 복귀 주소를 저장하는 메모리 블록 |
| 배경 | 재귀 호출 지원 및 모듈 간의 독립적인 실행 환경(Scope) 보장 필요 |
| 출제 의도 | 콜 스택(Call Stack) 동작 원리, 레지스터(ESP, EBP) 변화 과정 이해 |

## Ⅱ. 구성요소
```text
[ Stack Memory ]           [ Stack Frame ]
|      ...       | high    +-------------------+
+----------------+         | Parameters        |
|  Frame n       |         +-------------------+
+----------------+         | Return Address    |
|  Frame n+1     |         +-------------------+
+----------------+         | Saved EBP         |
|      ...       | low     +-------------------+
                           | Local Variables   |
                           +-------------------+
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| Return Addr | 함수 종료 후 돌아갈 명령의 위치 | 복귀 지점 표시 |
| Saved EBP | 이전 함수의 스택 기준점 저장 | 되돌아갈 베이스캠프 |
| Local Var | 호출 convention과 compiler 배치에 따라 register·stack slot에 저장되는 지역 값 | frame 저장 대상 |
> 요약: 스택 프레임은 함수가 실행되는 동안의 '상태'를 캡슐화한 공간임.

## Ⅲ. 절차
```text
Push Params -> CALL (Push Ret Addr) -> Push EBP -> Set New EBP -> Sub ESP
                                                                     |
Pop EBP <--- Leave (Move ESP, Pop EBP) <--- RET (Pop PC) <--- Work Done +
```
1. 프롤로그(Prologue): 호출자 스택 기준점(EBP) 저장 및 현재 ESP를 새 EBP로 설정.
2. 공간 할당: 로컬 변수 저장을 위해 ESP를 아래로 이동시켜 스택 공간 확보.
3. 바디 실행: 함수 로직 수행 및 로컬 변수 접근(EBP 기준 상대 주소 활용).
4. 에필로그(Epilogue): 할당 공간 해제, 이전 EBP 복구 및 RET 명령으로 복귀.
> 요약: call마다 return address·saved register·argument·local value를 frame에 배치하고 return 시 역순으로 복원함.

## Ⅳ. 문제점
- 과도한 재귀 호출 시 스택 공간 부족으로 인한 스택 오버플로우(Stack Overflow) 발생.
- 로컬 버퍼 크기 미체크 시 복귀 주소를 변조하는 버퍼 오버플로우 보안 공격에 취약.

## Ⅴ. 개선방안
- 꼬리 재귀 최적화(Tail Call Optimization)를 통해 스택 재사용 유도.
- Stack Canary 또는 ASLR 적용으로 스택 메모리 보호 및 코드 실행 공격 차단.

## Ⅵ. 전망
- 보안 강화: 하드웨어 지원 제어 흐름 보호(Intel CET) 기술을 통한 스택 무결성 보장.
- 분산 실행: 클라우드 환경에서 스택 프레임을 직렬화하여 타 노드로 이주/실행하는 기술.
