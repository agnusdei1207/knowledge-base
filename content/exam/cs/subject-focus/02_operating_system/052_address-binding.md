---
title: "주소바인딩 (Address Binding)"
date: "2026-06-30"
weight: 52
tags:
  - "exam-cspe-operating-system"
---

## Ⅰ. 정의
> 주소바인딩(Address Binding)은 프로그램의 명령어·데이터가 사용하는 논리주소(Logical Address)를 실제 메모리의 물리주소(Physical Address)로 사상(Mapping)하는 과정이다.

## Ⅱ. 구성요소 / 원리
- 컴파일 시간(Compile Time) 바인딩: 적재 위치를 미리 알 때 절대주소(Absolute Code) 생성, 위치 변경 시 재컴파일 필요
- 적재 시간(Load Time) 바인딩: 위치를 컴파일 시 모르면 재배치 가능 코드(Relocatable Code) 생성, 적재 시 확정
- 실행 시간(Execution Time) 바인딩: 실행 중 프로세스 이동 가능, MMU(Memory Management Unit) 하드웨어 지원 필요
- 논리주소: CPU가 생성하는 가상주소, 물리주소: 메모리 장치가 인식하는 실제 번지

## Ⅲ. 흐름도 / 구조
```text
소스 → [컴파일] → 목적모듈 → [링크] → 적재모듈 → [적재] → 메모리
        │컴파일시간          │적재시간            │실행시간
        절대주소            재배치주소          MMU 동적변환
CPU(논리주소) → MMU(재배치레지스터 가산) → 물리주소
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 논리주소를 물리주소로 변환하여 메모리 적재·실행 지원 |
| 장점 | 실행시간 바인딩 시 프로세스 동적 재배치·스와핑 가능 |
| 한계 | 컴파일/적재시간 바인딩은 위치 고정, 유연성 부족 |

## Ⅴ. 기술사적 적용
- 실행시간 바인딩은 MMU·재배치 레지스터(Relocation Register)와 결합하여 가상메모리·페이징의 기반이 됨
- 다중프로그래밍 환경에서 동적 적재(Dynamic Loading), 동적 링킹(Dynamic Linking)과 연계
