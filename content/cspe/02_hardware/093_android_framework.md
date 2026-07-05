---
title: 안드로이드 프레임워크 (Android Framework)
date: 2026-07-05
tags: [cspe-hardware]
weight: 93
---

## Ⅰ. 개요
- 리눅스 커널 위에서 앱 실행에 필요한 핵심 API와 서비스 레이어를 제공하는 구조체.
- 앱 개발자가 하드웨어의 복잡성을 몰라도 표준 인터페이스로 기능을 쓰게 함.
| 구분 | 내용 | 비고 |
|---|---|---|
| 정의 | 안드로이드 앱과 시스템 서비스를 연결하는 계층적 구조 | Middleware |
| 의도 | 계층별 역할 분담 및 HAL, Binder 메커니즘 이해 측정 | 상호운용성 |

## Ⅱ. 구성요소
[ Application Layer ]
[ Java API Framework (Managers) ]
[ Native C/C++ Libs / Android Runtime (ART) ]
[ Hardware Abstraction Layer (HAL) ]
[ Linux Kernel ]
| 구성요소 | 설명 | 비유 |
|---|---|---|
| API Framework | Activity, Window 등 서비스 관리 API 제공 | 서비스 센터 |
| ART | DEX 파일을 기계어로 변환하여 실행하는 런타임 | 번역기 |
| HAL | 상위 프레임워크와 HW 드라이버 간 표준 인터페이스 | 통번역사 |
> 요약: API 레이어, 런타임, HAL, 커널의 샌드위치 구조임.

## Ⅲ. 절차
(1) App Call -> (2) Framework Service -> (3) Binder IPC -> (4) HAL/Kernel
1. App Call: 앱이 자바 API를 통해 특정 기능(예: 카메라)을 요청함.
2. Framework Service: 해당 Manager 서비스가 요청을 검증하고 처리 준비.
3. Binder IPC: 서비스 프로세스와 실제 기능을 수행할 시스템 프로세스 간 통신.
4. HAL/Kernel: HAL 인터페이스를 거쳐 리눅스 커널 드라이버가 하드웨어 제어.
> 요약: API 호출, 서비스 중계, IPC 통신, 하드웨어 제어 순임.

## Ⅳ. 문제점
- 성능 오버헤드: 계층이 많고 Binder IPC가 빈번하여 자원 소모와 지연 발생.
- 버전 파편화: 하드웨어 제조사의 HAL 업데이트 지연으로 인한 OS 판올림 난항.

## Ⅴ. 개선방안
- 최적화: Project Mainline을 통해 핵심 시스템 컴포넌트의 모듈식 업데이트 강화.
- 구조 혁신: Project Treble 적용으로 프레임워크와 HAL을 분리하여 업데이트 속도 향상.

## Ⅵ. 전망
- 확장성: 모바일 넘어 전장(Android Automotive), IoT로의 도메인 특화 프레임워크 확산.
- 보안 강화: 가상화 기반의 격리된 실행 환경(pVM) 도입으로 개인정보 보호 강화 필수.
