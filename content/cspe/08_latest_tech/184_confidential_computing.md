---
title: "Confidential Computing 기밀 컴퓨팅 (Confidential Computing)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 184
extra:
  question_no: "184"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 기밀 컴퓨팅은 TEE를 포함한 하드웨어 격리 기술을 클라우드 운영 모델에 확장한 개념임
- 목적은 저장과 전송을 넘어 사용 중 데이터까지 보호하는 것임
- 원격 증명과 정책 기반 키 릴리스가 실제 서비스 신뢰 모델의 중심 역할을 함

## Ⅰ. 개요

- **정의/개념**: 기밀 컴퓨팅은 하드웨어 기반 격리 환경과 원격 증명과 정책 제어를 활용해 클라우드나 외부 인프라에서 처리 중인 데이터와 코드를 보호하는 보안 운영 모델임
- **배경/필요성**: 멀티테넌트 클라우드와 외부 위탁 연산이 확대되면서 CSP 내부자와 하이퍼바이저와 메모리 스크래핑까지 고려한 사용 중 데이터 보호가 필수 요구가 됨

## Ⅱ. 특징

- 기존 암호화가 보호하지 못하던 data in use 영역까지 보호 범위를 넓힘
- 인프라 운영자도 내용을 볼 수 없게 신뢰 경계를 하드웨어까지 축소함
- TEE와 키 관리와 증명 체계가 함께 작동해야 하므로 플랫폼 통합 난도가 높음
- 규제 산업의 퍼블릭 클라우드 전환을 가능하게 하는 실무형 보안 수단임

## Ⅲ. 종류 및 비교

| 판단 기준 | App-level Enclave | Confidential VM | Confidential Data Clean Room |
|:---|:---|:---|:---|
| 보호 단위 | 애플리케이션 | 가상머신 전체 | 공동 분석 환경 |
| 장점 | 세밀한 통제 | 레거시 이전 용이 | 다자 데이터 협업 가능 |
| 한계 | 개발 수정 부담 | TCB가 상대적으로 큼 | 운영 복잡도 큼 |
| 대표 활용 | 민감 API, 비밀 처리 | 클라우드 이전 워크로드 | 데이터 협업 분석 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| TEE Foundation | enclave나 confidential VM 같은 하드웨어 격리 기반을 제공해 실행 환경을 보호함 |
| Attestation Service | 워크로드의 무결성과 플랫폼 상태를 검증해 신뢰 가능한 환경인지 확인함 |
| Key, Secret Management | 증명 결과에 따라 데이터 복호화 키와 비밀값을 동적으로 제공함 |
| Confidential Runtime | VM이나 컨테이너와 애플리케이션이 보호된 상태로 실행되도록 운영 계층을 구성함 |
| Policy, Audit Layer | 어떤 조건에서 실행과 키 릴리스를 허용할지 정책화하고 감사 기록을 남김 |

```text
+-------------------+      +-------------------+      +-------------------+
| TEE Foundation    | ---> | Attestation       | ---> | Key / Secret Mgmt |
+-------------------+      +-------------------+      +-------------------+
                                                           |
                                                           v
                                                   +-------------------+
                                                   | Confidential Run  |
                                                   +-------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 보호 환경 기동   | --> | 원격 증명 검증  | --> | 키/비밀 주입    | --> | 기밀 워크로드 실행 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **보호 환경 기동**: confidential VM이나 enclave 환경을 띄움
2. **원격 증명 검증**: 플랫폼과 애플리케이션 무결성을 외부에서 확인함
3. **키 및 비밀 주입**: 정책을 만족할 때만 비밀키를 전달함
4. **기밀 워크로드 실행**: 데이터가 보호된 상태로 분석과 추론을 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 원격 증명과 키 릴리스가 운영 파이프라인과 분리되면 보호 환경이 있어도 실제 비밀 관리가 우회될 수 있음
   - 해결방안: attestation-gated key release를 적용하고 unauthorized key release rate와 attestation compliance로 검증함
2. 문제: 로그 수집과 관측성이 제한되면 운영 장애 분석과 성능 튜닝이 어려워질 수 있음
   - 해결방안: privacy-safe observability를 설계하고 debug turnaround time과 secure telemetry coverage로 검증함
3. 문제: 하드웨어와 CSP 종속성이 커지면 멀티클라우드 이식성과 비용 통제가 어려워질 수 있음
   - 해결방안: abstraction layer와 workload portability 전략을 적용하고 migration effort와 vendor lock-in score로 검증함

## Ⅶ. 적용 사례

- 금융사의 퍼블릭 클라우드 이전 워크로드가 confidential VM에서 신용정보를 처리하며 확인 지표는 attestation success rate와 data-in-use exposure rate임
- 기업 간 데이터 클린룸이 기밀 컴퓨팅 위에서 공동 분석을 수행하며 확인 지표는 joint analysis latency와 raw data exposure rate임
- AI 추론 서비스가 모델 키를 기밀 런타임 내부에서만 열어 사용하며 확인 지표는 key release policy compliance와 inference SLA attainment임

## Ⅷ. 결론

기밀 컴퓨팅은 TEE를 서비스 운영 모델로 확장해 클라우드 신뢰 문제를 기술적으로 줄이는 방식이므로 증명과 키 관리의 자동화가 핵심 경쟁력이 됨.
