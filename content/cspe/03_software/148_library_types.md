---
title: 라이브러리 — 정적 vs 동적 라이브러리 (Library Types)
date: 2026-07-05
tags: [cspe-software]
weight: 148
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 자주 사용되는 함수나 데이터들의 집합으로, 재사용 가능하도록 모듈화된 파일 |
| 필요성 | 코드 중복 방지, 개발 생산성 향상 및 전문화된 기능(수학, 통신 등) 공유 |
| 출제 의도 | 정적(Static) vs 동적(Dynamic/Shared) 연결 방식의 장단점 비교 |

## Ⅱ. 구성요소
```text
[ Static Lib (.lib/.a) ]       [ Dynamic Lib (.dll/.so) ]
+----------------------+       +-----------------------+
|  Included in .exe    |       |  External to .exe     |
+----------------------+       +-----------------------+
|  Linking Time Load   |       |  Runtime Load (Lazy)  |
+----------------------+       +-----------------------+
```
| 항목 | 정적 라이브러리 | 동적 라이브러리 |
|---|---|---|
| 포함 시점 | 컴파일/링킹 시 | 실행(Runtime) 시 |
| 실행 파일 크기 | 큼 (함수 코드 포함) | 작음 (참조 정보만 포함) |
| 프로세스 공유 | executable마다 library code 포함 | 동일 shared library의 read-only page를 여러 process가 공유 가능 |
> 요약: 정적 연결은 library code를 executable에 포함하고, 동적 연결은 load·run time에 shared object symbol을 resolve함.

## Ⅲ. 절차
```text
(Dynamic Linking Case)
Load .exe -> Start Execution -> Call Function -> Find Lib on Disk
                                                      |
                          Run Func <--- Map Lib to Memory <---+
```
1. 헤더 포함: 개발 시 필요한 함수 선언이 담긴 헤더 파일을 소스에 포함.
2. 참조 기록: (동적 시) 실행 파일 내부에 외부 라이브러리 이름과 주소 정보를 기록.
3. 런타임 탐색: 프로그램 실행 중 함수 호출 발생 시 OS가 라이브러리 위치 검색.
4. 메모리 매핑: 해당 라이브러리를 메모리에 한 번만 올리고 호출 프로세스들이 공유.
> 요약: dynamic loader는 필요한 shared object를 mapping하고 symbol resolution·relocation 후 호출 주소를 연결함.

## Ⅳ. 문제점
- 동적 라이브러리의 버전 불일치로 인한 "DLL Hell" 및 실행 실패 위험.
- 정적 라이브러리는 라이브러리 업데이트 시 전체 프로그램을 재배포해야 함.

## Ⅴ. 개선방안
- Side-by-Side (SxS) 배포 또는 매니페스트 파일을 통해 여러 버전의 공존 지원.
- 컨테이너화를 통해 필요한 모든 라이브러리를 단일 패키징하여 환경 일관성 확보.

## Ⅵ. 전망
- 모듈 시스템: Java, C++ 등 최신 표준에서 헤더 대신 모듈 단위를 사용하여 성능 향상.
- 보안 라이브러리: 하드웨어 보안 모듈(HSM)과 연동되는 신뢰 실행 환경 라이브러리 강화.
