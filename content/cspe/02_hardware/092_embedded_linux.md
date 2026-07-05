---
title: 임베디드 리눅스 (Embedded Linux)
date: 2026-07-05
tags: [cspe-hardware]
weight: 92
---

## Ⅰ. 개요
- 리눅스 커널을 임베디드 시스템 사양에 맞게 경량화 및 최적화하여 구현한 운영체제.
- 오픈소스 생태계의 풍부한 드라이버와 네트워크 프로토콜 스택 활용이 장점임.
| 구분 | 내용 | 비고 |
|---|---|---|
| 정의 | 범용 리눅스를 임베디드 타겟 HW에 이식한 시스템 | Open Source |
| 의도 | 커널 최적화, 빌드 시스템(Yocto), 이식 기술 이해 측정 | Ecosystem 활용 |

## Ⅱ. 구성요소
[ User Space (Applications / Libraries) ]
[ Kernel Space (Process, Memory, NW Stack) ]
[ Drivers (Char, Block, Network) ]
[ Architecture Specific Code (BSP) ]
| 구성요소 | 설명 | 비유 |
|---|---|---|
| 커널 | 프로세스 관리, 파일 시스템 등 핵심 서비스 제공 | 엔진 |
| 툴체인 | 타겟 HW용 실행 파일을 만드는 교차 컴파일 환경 | 연장통 |
| 루트파일시스템 | OS 구동에 필요한 최소한의 디렉토리와 파일 모음 | 창고 |
> 요약: 최적화된 커널, 드라이버, 루트파일시스템으로 구성됨.

## Ⅲ. 절차
(1) Toolchain Setup -> (2) Kernel Config -> (3) Build -> (4) Porting
1. Toolchain Setup: 타겟 CPU(ARM 등)에 맞는 크로스 컴파일러 환경 구축.
2. Kernel Config: 필요한 기능만 선택하고 불필요한 모듈을 제거하여 크기 최소화.
3. Build: 커널 이미지 및 루트파일시스템(BusyBox 등)을 생성함.
4. Porting: 부트로더를 통해 타겟 보드에 이미지를 적재하고 부팅 테스트 수행.
> 요약: 빌드 환경 구축, 구성 최적화, 이미지 생성, 타겟 이식 순임.

## Ⅳ. 문제점
- 실시간성 부족: 범용 커널의 특성상 엄격한 Hard Real-time 보장이 어려움.
- 부팅 지연: 커널 및 서비스 초기화 과정이 길어 즉각적인 반응성 확보가 난해함.

## Ⅴ. 개선방안
- 실시간 강화: PREEMPT_RT 패치 적용 또는 Xenomai 등 듀얼 커널 구조 도입.
- 고속 부팅: Fastboot, 정적 드라이버 로딩, 파일 시스템 최적화(XIP 등) 적용.

## Ⅵ. 전망
- Yocto Project 표준화: 제조사별 파편화된 빌드 방식을 통합하여 개발 효율성 증대.
- 컨테이너 도입: 임베디드 환경에서도 Microservices Architecture(MSA) 구현 가속화.
