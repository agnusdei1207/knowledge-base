---
title: "ARM TrustZone (ARM TrustZone)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 76
---

## Ⅰ. 개요
- **정의**: ARM 프로세서에서 하드웨어 수준으로 Secure/Normal 두 실행 환경을 격리하는 보안 기술임
- **배경/필요성**: 소프트웨어 기반 보안만으로는 커널 권한 탈취 시 전체 시스템이 노출되어 하드웨어 격리가 필요함
- **비유**: 은행 금고와 일반 창구를 물리적 벽으로 분리하는 구조임

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TEE 구현 원리와 활용 사례 | NS비트 기반 버스·메모리 분리 메커니즘 | Secure Monitor 역할을 빠뜨리면 감점 |

> 요약: 하드웨어 격리로 민감 데이터·코드를 Normal World로부터 보호하는 기술임

## Ⅱ. 구성요소
```text
+-- Normal World --+    +-- Secure World --+
|  Rich OS (Linux) |    |  Trusted OS      |
|  Normal Apps     |    |  Trusted Apps    |
+--------+---------+    +--------+---------+
         |                       |
         +----> Secure Monitor (EL3) <----+
                     |
                 TZASC / TZPC
                     |
                 Bus Fabric
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| Secure Monitor | EL3에서 World 전환(SMC 호출)을 중재하는 펌웨어 | 금고실 출입 통제 보안관 |
| TZASC/TZPC | 메모리·주변장치 접근을 NS비트로 제어하는 하드웨어 컨트롤러 | 출입증 기반 구역별 잠금장치 |
| Trusted OS | Secure World에서 실행되는 경량 OS(OP-TEE 등) | 금고실 내부 관리 시스템 |

> 요약: Secure Monitor·접근제어·Trusted OS로 이중 실행 환경을 구현함

## Ⅲ. 절차
```text
Normal App 요청 --> SMC 호출 --> World 전환 --> Secure 처리/반환
      |                |             |               |
      v                v             v               v
   TEE API호출    EL3트랩발생   컨텍스트전환    암호연산후복귀
```
- 1단계: Normal World 앱이 TEE Client API를 통해 보안 서비스를 요청함
- 2단계: SMC(Secure Monitor Call) 명령으로 EL3 트랩이 발생함
- 3단계: Secure Monitor가 컨텍스트를 전환하여 Secure World로 진입함
- 4단계: Trusted App이 암호연산·키관리를 수행한 뒤 결과를 Normal World로 반환함

> 요약: SMC 기반 World 전환을 통해 보안 연산을 격리 수행하고 결과만 반환함

## Ⅳ. 문제점
- 전환 오버헤드: World 전환 시 캐시 플러시·컨텍스트 저장으로 수 μs 지연이 발생함
- Secure World 취약점: Trusted OS 자체 버그 발생 시 패치 배포가 느림
- 제한된 자원: Secure World에 할당 가능한 메모리·코어가 제한되어 복잡한 연산이 어려움

> 요약: 전환 지연·보안측 취약점·자원 제한이 TrustZone의 주요 과제임

## Ⅴ. 개선방안
1. 단기: 배치 호출로 SMC 횟수를 줄여 전환 오버헤드를 최소화함
2. 중기: Trusted OS OTA 업데이트 체계를 구축하여 취약점 패치 주기를 단축함
3. 장기: CCA(Confidential Compute Architecture) 도입으로 Realm 단위 격리를 확대함

> 요약: 호출 최적화·OTA·CCA로 TrustZone의 한계를 단계적으로 해소함

## Ⅵ. 전망
- 발전 방향: ARMv9 CCA 기반 Realm 격리로 VM·컨테이너 수준 기밀 컴퓨팅이 확대됨
- 기술사적 판단: 모바일 결제·DRM·FIDO 인증 등 TEE 의존 서비스가 지속 증가할 전망임
- 기술사 제언: TrustZone과 CCA의 적용 범위를 구분하여 보안 아키텍처를 설계할 필요가 있음
