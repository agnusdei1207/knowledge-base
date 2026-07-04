---
title: "기밀 컴퓨팅 (Confidential Computing)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-security"
weight: 26
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: 기밀 컴퓨팅은 TEE(025) 기반으로 **실행 중 데이터(data-in-use)** 까지 보호하는 **클라우드 보안 서비스 모델**임. TEE가 하드웨어 메커니즘이라면, 기밀 컴퓨팅은 이를 클라우드 서비스(Confidential VM·Container)로 제공하는 상위 개념임.
- **왜 필요한가**: 기존 암호화는 저장(AES-256 at-rest)·전송(TLS in-transit) 구간만 보호하고, CPU가 연산할 때는 평문이 메모리에 존재함. 멀티테넌트 클라우드에서 운영자·하이퍼바이저·관리자 권한까지 신뢰하지 않는 구조가 필요함.
- **핵심 직관**: 금고 안에 문서를 넣어 보관하는 수준을 넘어, 금고 안에서 문서 작업까지 끝내는 방식임. TEE(025)가 금고방 자체라면, 기밀 컴퓨팅은 금고방이 내장된 클라우드 공장을 빌리는 것임.

## 핵심 용어 정리 (내부에 등장하는 것들)

TEE 자체의 용어(enclave·attestation·sealed storage 등)는 025에서 상세히 다루므로, 여기서는 기밀 컴퓨팅 고유 개념에 집중함.

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| Data-in-use (상위 키워드) | 연산 중 메모리 데이터 보호 | 문서 작업 중 보호 |
| Confidential VM | VM 전체를 TEE로 격리하는 서비스 | VM 통째로 금고방 |
| Confidential Container | 컨테이너 워크로드를 TEE로 격리 | 컨테이너 단위 금고방 |
| CCC | Confidential Computing Consortium — 산업 표준 컨소시엄 | 기밀 컴퓨팅 표준 모임 |
| Attestation Service | 클라우드가 제공하는 원격 증명 서비스 | 금고방 봉인 검사 대행 |
| Key Release Policy | attestation 결과 기반 KMS 키 주입 조건 | 봉인 검사 통과 시만 열쇠 제공 |
| Workload Identity | enclave/VM의 코드·설정을 식별하는 고유값 | 금고방 주인 이름표 |
| 3대 데이터 보호 | at-rest(저장)·in-transit(전송)·in-use(사용) | 보관·배달·사용 세 단계 보호 |

## 깊이 이해
- **배경·문제의식**: TEE(025)에서 다룬 CPU 격리 메커니즘은 하드웨어 기능 자체임. 기밀 컴퓨팅은 이를 클라우드 서비스로 상용화한 것으로, Azure Confidential Computing·GCP Confidential VMs·AWS Nitro Enclaves 등이 대표적임. 금융·의료·공공 규제 데이터의 클라우드 위탁 처리에서 "운영자를 신뢰하지 않는 구조"를 요구하는 규제가 늘어남.
- **작동 원리**: (025 TEE 메커니즘 참조) 기밀 컴퓨팅 서비스 레이어에서 추가되는 것은 (1) 클라우드 제공자의 attestation service가 측정값·TCB 버전을 자동 검증함, (2) KMS key release policy에 attestation 결과·workload identity·mTLS 조건을 설정함, (3) confidential VM/container 템플릿으로 워크로드 배포가 표준화됨.
- **비유**: TEE(025)가 봉인 금고방이라면, 기밀 컴퓨팅은 금고방이 내장된 공장을 빌려주는 클라우드 서비스이며, 봉인 검사 대행·열쇠 보관·감사 로그까지 패키지로 제공하는 것임.
- **구체 예시**: Azure의 DCsv3 시리즈는 Intel SGX enclave를, DCasv5는 AMD SEV-SNP confidential VM을 제공함. GCP N2D confidential VM은 SEV 기반임. attestation 성공 후에만 KMS에서 데이터 키를 복호화해 enclave/VM에 주입함.
- **흔한 오해·주의점**: (1) 기밀 컴퓨팅이 모든 보안을 대체하지 않음 — side-channel, enclave 코드 버그, attestation 검증 누락은 별도 통제(025 참조). (2) TEE와 기밀 컴퓨팅을 동일시하면 안 됨 — TEE는 HW 메커니즘, 기밀 컴퓨팅은 서비스 모델임. (3) 일반 공개 데이터 처리에는 at-rest·in-transit 암호화로 충분하며, 기밀 컴퓨팅은 규제 민감 데이터에 적용함.

## 연결 개념
- **TEE(025)**: 기밀 컴퓨팅의 하드웨어 실행 기반 — 메커니즘 상세는 025 참조
- **HSM/KMS(030)**: attestation 검증 후 키를 주입하는 통제점
- **동형 암호(021)·MPC(023)**: 서버 비신뢰 연산의 SW 기반 대안

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 기밀 컴퓨팅은 CPU TEE로 실행 중 데이터(data-in-use)를 격리·암호화하는 클라우드 보안 서비스 모델임.
> 2. **가치**: 저장(AES-256)·전송(TLS 1.3) 이후 남는 운영자·하이퍼바이저·메모리 덤프 위협을 축소함.
> 3. **판단 포인트**: remote attestation 성공·TCB 패치·KMS key release policy·side-channel 통제가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Data-in-use 보호 범위 | at-rest/in-transit/in-use 3대 구분, TEE 격리 | 단순 디스크 암호화로 설명 |
| 클라우드 신뢰 경계 | 하이퍼바이저·관리자를 비신뢰 주체로 설정 | 클라우드 사업자를 전면 신뢰 가정 |
| 운영 통제 역량 | Attestation→KMS 조건부 키 릴리스→감사로그 | enclave 생성 후 키 무조건 주입 |

> 요약: 기밀 컴퓨팅 답안은 TEE 기능보다 위협 모델·attestation·키 릴리스 조건을 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: TEE 기반으로 실행 중 데이터를 보호하는 클라우드 보안 서비스 모델임.
- 배경: 기존 암호화는 at-rest·in-transit 보호에 집중하지만, 연산 시점 메모리 평문과 관리자 권한 위협이 남음.
- 필요성: Confidential VM/Container와 attestation service로 하이퍼바이저·운영자 비신뢰 구조를 실현해 규제 데이터의 클라우드 처리를 지원함.

---

## Ⅱ. 구조 및 구성요소

```text
민감 워크로드 -> TEE 생성(Confidential VM/Container)
  -> 측정값 생성 -> Attestation Service 검증
  -> KMS Key Release -> 암호화 연산 -> 결과 저장
  / TCB 버전 확인 / 감사로그 적재
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| TEE/Enclave | 코드·데이터 실행 영역 격리 | Intel SGX, AMD SEV-SNP, Arm CCA |
| Attestation Service | 측정값·서명·TCB 버전 자동 검증 | nonce로 재전송 공격 차단 |
| KMS/HSM | attestation 성공 시에만 데이터 키 릴리스 | key release policy, mTLS, RBAC |
| 보안 관측 | 실행·검증·키 사용 이벤트 수집 | SIEM 연계, 감사 보존 1년 이상 |

> 요약: 구조 핵심은 TEE 자체가 아니라 attestation 결과를 KMS key release 조건으로 묶는 통제 체계임.

---

## Ⅲ. 동작원리 및 흐름도

```text
워크로드 배포 -> TEE 측정값 산출 -> Attestation Service 검증 요청
  -> Key Release Policy 판정 -> KMS 데이터 키 복호화
  -> TEE 내부 처리 -> 결과 암호화 저장 -> 로그 감사
```

1. TEE 생성: Confidential VM 또는 enclave를 생성하고, 이미지 해시·TCB 버전으로 측정값을 산출함.
2. Attestation 검증: attestation evidence(서명된 quote)를 attestation service에 제출하고, nonce·인증서 체인으로 플랫폼 상태를 검증함.
3. Key Release: KMS가 workload identity·mTLS·attestation 결과를 key release policy로 평가하고, 모든 조건 만족 시에만 데이터 키를 릴리스함.
4. 격리 실행·감사: TEE 내부에서 데이터를 복호화·연산하고, 결과를 암호화 저장하며 키 사용 로그 100%와 실패 이벤트 경보를 SIEM에 전송함.

> 요약: 실행 신뢰는 배포 시 선언이 아니라 측정값 검증 후 키를 주입하는 절차로 확보함.

---

## Ⅳ. 특징

- 3대 데이터 보호 완성: at-rest(AES-256)·in-transit(TLS 1.3)에 in-use(TEE)를 추가해 전 구간 암호화를 실현함.
- 비신뢰 운영 모델: OS·하이퍼바이저·클라우드 관리자를 비신뢰 대상으로 설정해 멀티테넌트 환경의 신뢰 경계를 축소함.
- Attestation 기반 키 통제: attestation 성공 전에는 키를 주입하지 않는 순서가 보안 설계의 핵심이며, 미검증 키 릴리스 0건을 목표로 함.
- Side-channel·TCB 잔존: 캐시 타이밍·분기예측 등 부수 채널 공격과 CPU 벤더 TCB 취약점은 별도 통제가 필요함(025 참조).
- 서비스 가용성: CPU·클라우드 리전별 TEE 지원 여부가 다르므로 호환성 매트릭스와 fallback 워크로드 분리가 필요함.

---

## Ⅴ. 심화 비교 및 적용 판단

기밀 컴퓨팅(TEE 서비스)과 기존 암호화(at-rest/in-transit)를 보호 범위·신뢰 경계·비용 축으로 비교함.

| 구분 | 기존 암호화(at-rest/in-transit) | 기밀 컴퓨팅(TEE 서비스) | 선택 기준 |
|:---|:---|:---|:---|
| 보호 범위 | 저장·전송 구간 | 저장·전송+실행 중 메모리 | data-in-use 위협 존재 여부 |
| 신뢰 경계 | OS·하이퍼바이저 신뢰 | OS·하이퍼바이저 비신뢰 | 클라우드 운영자 비신뢰 요구 |
| 비용·성능 | 일반 VM 성능 | p95 지연 5~30% 증가·CPU 암호화 비용 | 성능 오버헤드 허용 범위 |

> 요약: 규제 데이터의 클라우드 처리·공동 분석에서 운영자 신뢰를 줄여야 하면 기밀 컴퓨팅을, 일반 데이터는 at-rest/in-transit 암호화를 적용함.

**리스크·대응:**
- Side-channel: 캐시·분기·페이지 접근 패턴 관측 → constant-time 코드·패치·민감 분기 최소화 (지표: TCB 패치 30일 이내)
- Attestation 우회: attestation 검증 누락·정책 미흡 → KMS policy에 측정값·TCB 버전 조건 필수 포함 (지표: 미검증 키 릴리스 0건)
- 리전 미지원: CPU·클라우드 리전별 TEE 미지원 → 호환성 매트릭스·fallback 워크로드 분리 (지표: 지원 리전 2개 이상)

**도입 후 점검 지표:**
- 기밀성: 평문 반출 경로 0건 — DLP·메모리 덤프 테스트
- 검증: attestation 성공률 99.9%·실패 경보 5분 이내 — KMS·attestation 로그
- 운영: 키 사용 로그 100%·관리자 접근 승인 2인 — SIEM·IAM 감사

---

## Ⅵ. 실무 적용 및 결론

**적용 방안:**
1. 위협 모델을 설정하고 at-rest/in-transit/in-use를 분리해 하이퍼바이저·관리자를 비신뢰 주체로 명시함.
2. KMS key release policy에 attestation 측정값·TCB 버전·workload identity·mTLS를 조건으로 설정함.
3. TCB 패치 SLA 30일·키 사용 로그 100%·attestation 실패 경보 5분 이내를 운영 기준으로 수립함.

**결론:**
- 기술사 판단: 규제 데이터의 클라우드 처리·공동 분석이면 기밀 컴퓨팅(TEE+KMS)을, 일반 공개 데이터는 at-rest/in-transit 암호화를 우선 적용함.
- 향후 방향: Confidential VM·Confidential Container·Confidential AI Inference로 확장되며, attestation 표준화와 키 거버넌스가 핵심 과제임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "기밀 컴퓨팅을 설명하시오" | TEE 생성·attestation·KMS key release 흐름 | 3대 데이터 보호 범위 비교 |
| 요구사항 명시형 | "클라우드 민감정보 보호 방안을 제시하시오" | 위협-통제-탐지-복구 흐름·key release policy | side-channel·TCB·운영 지표 기반 선택 기준 |

> 요약: 설명형은 TEE 원리와 3대 보호 범위를, 방안형은 키 관리·검증·감사 통제까지 확장함.
