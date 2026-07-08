---
title: "ARM TrustZone 보안 익스텐션 (ARM TrustZone)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 76
extra:
  question_no: "076"
  exam_status: "기출"
  exam_history: "138회"
---

## 미리 알고가기

- TrustZone은 하나의 ARM 시스템 안에서 secure world와 normal world를 분리하는 보안 확장임
- secure monitor와 메모리, 주변장치 접근 제어가 핵심 구성임
- 보안 키 관리와 secure boot와 함께 쓰일 때 효과가 커짐

## Ⅰ. 개요

- **정의/개념**: ARM TrustZone은 ARM 기반 SoC를 secure world와 normal world로 논리 분리해 민감 코드와 키와 보안 서비스를 격리 실행하게 하는 하드웨어 보안 아키텍처임
- **배경/필요성**: 모바일과 임베디드 장치는 일반 애플리케이션과 보안 기능을 함께 실행하므로, 하나의 칩 안에서 신뢰 영역을 분리해 공격면을 줄일 필요가 있음

## Ⅱ. 특징

- 하나의 프로세서 안에서 보안 영역과 일반 영역을 분리할 수 있음
- 메모리와 인터럽트와 주변장치 접근을 secure attribute로 통제함
- TEE와 secure boot와 결합해 키 보호와 신뢰 부팅 기반을 제공함
- secure world 코드가 커지면 공격면과 유지보수 부담이 다시 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | 일반 실행 환경 | TrustZone 기반 환경 |
|:---|:---|:---|
| 보안 격리 | 소프트웨어 중심 | 하드웨어 분리 기반 |
| 키 보호 | 취약 | secure world 저장 가능 |
| 공격면 | OS 전체 | secure world 최소화 가능 |
| 대표 활용 | 일반 앱 실행 | TEE, 결제, 키 관리 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Secure, Normal World | 민감 기능과 일반 기능을 논리적으로 분리해 권한 경계를 형성함 |
| Secure Monitor | world 전환과 컨텍스트 저장을 담당해 경계 통제의 핵심이 됨 |
| TZASC, Access Control | 메모리와 주변장치의 secure 속성을 관리해 접근 범위를 제한함 |
| TEE, Secure Service | 키 저장과 인증과 결제 같은 민감 서비스를 secure world에서 제공함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| secure boot 시작 | --> | world 속성 설정 | --> | secure 서비스 실행 | --> | normal world 연계 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **Secure boot 시작**: 신뢰된 초기 코드가 secure world를 설정함
2. **World 속성 설정**: 메모리와 주변장치 접근 권한을 구분함
3. **Secure 서비스 실행**: TEE와 키 관리 기능을 secure world에서 수행함
4. **Normal world 연계**: 일반 OS가 요청 시 monitor를 통해 보안 서비스를 호출함

## Ⅵ. 문제점 및 해결 방안

1. 문제: secure world 코드가 커지고 복잡해지면 보안 영역 자체가 큰 공격면이 될 수 있음
   - 해결방안: TCB 최소화를 적용하고 secure code size와 vulnerability count로 검증함
2. 문제: 메모리와 주변장치 속성 설정이 잘못되면 normal world에서 민감 자원에 접근할 수 있음
   - 해결방안: secure attribution 검증을 자동화하고 isolation test coverage와 unauthorized access count로 검증함
3. 문제: world 전환과 secure monitor 호출이 잦으면 성능 오버헤드와 설계 복잡도가 커질 수 있음
   - 해결방안: secure service 호출 경로를 최소화하고 world switch overhead와 secure call frequency로 검증함

## Ⅶ. 적용 사례

- 모바일 결제 환경에서는 TEE와 키 저장을 TrustZone에 배치하고 확인 지표는 key extraction resistance와 transaction latency임
- IoT 게이트웨이에서는 secure boot와 인증 서비스를 분리하고 확인 지표는 boot integrity와 device attestation success rate임
- 자동차 보안 ECU에서는 민감 자격 증명을 secure world에서 관리하고 확인 지표는 unauthorized access count와 service overhead임

## Ⅷ. 결론

TrustZone의 핵심은 하나의 칩을 두 개의 신뢰 수준으로 나누는 데 있으므로, secure world를 작게 유지하고 자원 속성 설정을 정확히 하는 것이 본질임.
