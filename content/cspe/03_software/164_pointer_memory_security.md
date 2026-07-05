---
title: C/C++ 포인터 및 메모리 보안 (Pointer and Memory Security)
date: 2026-07-05
tags: ["cspe-software"]
weight: 164
---

## Ⅰ. 개요
- 정의: 메모리 주소를 직접 다루는 포인터 사용 시 발생하는 취약점 방지 및 관리 기술
- 배경: C/C++의 저수준 메모리 제어로 인한 Buffer Overflow 등 보안 사고 빈번
| 구분 | 내용 |
|------|------|
| 출제 의도 | Dangling Pointer, Buffer Overflow 등 취약점 원인과 현대적 방어 기법 파악 |

## Ⅱ. 구성요소
  [ Memory Space ] -> [ Address ] -> [ Value ]
  *ptr -> Vulnerable Point -> Exploit
| 구성요소 | 설명 | 비유 |
|----------|------|------|
| Pointer | 메모리 주소를 저장하는 변수 | 주소록 |
| Stack/Heap | 데이터 저장 영역(정적/동적) | 창고 |
| Canary | 버퍼 오버플로우 감지용 무작위 값 | 경보 장치 |
> 요약: 직접적인 메모리 접근 권한에 따른 관리 책임과 보안 경계

## Ⅲ. 절차
  Allocate -> Validate -> Access -> Deallocate
1. Allocation: malloc/new 등을 통한 메모리 영역 확보
2. Boundary Check: 접근 인덱스가 할당 범위를 넘는지 검사
3. Secure Access: 스마트 포인터 등을 사용한 안전한 참조
4. Free/Null: 메모리 해제 후 포인터를 NULL로 초기화
> 요약: 할당부터 해제까지의 생명주기 제어 및 경계 검사 강화

## Ⅳ. 문제점
- 버퍼 범위를 벗어난 쓰기 작업으로 인한 복귀 주소 변조(Stack Overflow)
- 해제된 메모리 재사용(Use-After-Free) 및 메모리 누수 발생

## Ⅴ. 개선방안
- ASLR(주소 공간 임의화), DEP(데이터 실행 방지) 하드웨어 보안 적용
- Smart Pointer(Unique, Shared) 사용 및 정적 분석 도구 도입

## Ⅵ. 전망
- 메모리 안전 언어(Rust)로의 커널 전환 가속화 및 하드웨어 기반 태그 지정 메모리(MTE) 보편화
