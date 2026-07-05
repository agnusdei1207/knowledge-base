---
title: 모바일 운영체제 — 커널·런타임 (Mobile OS)
date: 2026-07-05
tags: [cspe-software]
weight: 141
---

## Ⅰ. 개요
| 구분 | 내용 |
|---|---|
| 정의 | 스마트폰, 태블릿 등 모바일 기기에 최적화된 하드웨어 관리 및 앱 환경 OS |
| 배경 | 저전력 관리, 터치 UI, 센서 통합 및 앱 스토어 생태계 요구 증대 |
| 출제 의도 | 안드로이드 vs iOS 구조 비교, ART vs Dalvik 런타임 이해 측정 |

## Ⅱ. 구성요소
```text
[ Application ]        [ Android Framework ]
+-------------+        +-------------------+
| App Runtime |        |   HAL (Hardware   |
+-------------+        |   Abstraction)    |
|   Kernel    |        +-------------------+
+-------------+        |   Linux Kernel    |
```
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 런타임 (ART) | 앱 실행을 위해 미리 컴파일(AOT)하는 실행 환경 | 사전 조리실 |
| HAL | 하드웨어 독립성을 확보하기 위한 표준 인터페이스 계층 | 만능 리모컨 |
| 커널 (Linux) | 메모리, 전력 관리(Low Memory Killer) 기능 강화 | 특수 관리인 |
> 요약: 모바일 OS는 전력 효율과 사용자 경험(UX) 최적화에 집중함.

## Ⅲ. 절차
```text
App Launch -> Process Fork -> Runtime Init -> Component Load (UI)
      ^                                             |
      +----- (Background) <--- Power Save Mode <----+
```
1. 프로세스 생성: Zygote 방식을 활용해 공통 라이브러리가 로드된 프로세스 복제.
2. 런타임 로드: ART 환경에서 앱의 실행 파일(DEX)을 기계어로 해석 및 최적화.
3. 앱 라이프사이클: Foreground/Background 상태에 따라 자원 우선순위 조정.
4. 자원 회수: 메모리 부족 시 LMK(Low Memory Killer)가 비활성 앱부터 종료.
> 요약: 빠른 앱 실행을 위해 복제(Fork)와 사전 컴파일 기술을 활용함.

## Ⅳ. 문제점
- 안드로이드의 파편화(Fragmentation)로 인한 OS 업데이트 지연 및 보안 취약.
- 백그라운드 프로세스 증가 시 배터리 소모 및 전체 성능 저하 발생.

## Ⅴ. 개선방안
- Project Treble 적용으로 프레임워크와 제조사 구현 영역을 분리해 업데이트 가속.
- 머신러닝 기반 전력 관리로 사용자 앱 패턴 분석 및 자원 자동 최적화.

## Ⅵ. 전망
- 크로스 플랫폼: OS 경계를 넘나드는 앱 실행 환경(Flutter 등)과의 통합 강화.
- 온디바이스 AI: 모바일 OS 커널 레벨에서 NPU 가속기 직접 제어 및 보안 모델 강화.
