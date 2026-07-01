---
title: "서비스 메시 (Service Mesh)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 265
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서비스 메시를 MSA 서비스 간 통신 기능을 애플리케이션 코드 밖의 인프라 계층으로 분리하는 구조로 이해하게 만든다.

## 한눈에
- **개요**: 서비스 간 호출의 라우팅, mTLS, 재시도, 관측성을 프록시와 제어 평면으로 처리하는 인프라 계층
- **왜 필요한가**: MSA가 늘어나면 각 서비스 코드에 통신 정책, 인증서, 타임아웃, 추적 로직이 중복된다.
- **핵심 직관**: 도로마다 운전자가 신호 규칙을 직접 외우게 하지 않고, 교통 관제 시스템이 흐름과 안전 규칙을 관리하는 방식이다.

## 깊이 이해
- **배경·문제의식**: MSA는 독립 배포를 제공하지만 서비스 간 호출이 네트워크 장애, 인증서 관리, 분산 추적 문제를 만든다.
- **작동 원리**: 데이터 평면 프록시가 서비스 트래픽을 가로채고, 제어 평면은 라우팅 규칙, 인증서, 정책, telemetry 설정을 프록시에 배포한다.
- **비유**: 사무실마다 보안 담당자를 두는 대신 중앙 출입 관제와 층별 게이트가 출입 기록과 권한을 관리하는 구조다.
- **구체 예시**: 주문 서비스에서 결제 서비스로 가는 호출에 2초 timeout, 1회 retry, mTLS, trace id 전파를 애플리케이션 수정 없이 적용한다.
- **흔한 오해·주의점**: 서비스 메시는 MSA의 필수 전제가 아니다. 서비스 수, 배포 빈도, 보안 요구, 운영 인력이 맞지 않으면 프록시 비용만 늘 수 있다.

## 연결 개념
- Istio — 대표적인 Kubernetes 서비스 메시 구현
- Sidecar Proxy — 데이터 평면을 pod 옆에 배치하는 패턴
- Cloud Native Observability — 메시가 수집하는 metric, log, trace 활용

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: 서비스 메시는 MSA 통신 문제를 데이터 평면과 제어 평면으로 분리해 해결한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Service Mesh는 서비스 간 통신 제어를 애플리케이션 코드에서 분리한 네트워크 인프라 계층임.
> 2. **가치**: mTLS, traffic split, retry/timeout, circuit breaker, distributed tracing을 정책으로 일관 적용함.
> 3. **판단 포인트**: 서비스 수와 보안·관측성 요구가 낮으면 API Gateway와 라이브러리 기반 통제로 충분할 수 있음.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| MSA 통신 문제 이해 확인 | service-to-service, east-west traffic, 정책 분리 | API Gateway와 역할 혼동 |
| 구조 이해 확인 | data plane, control plane, proxy, policy | 프록시만 설명하고 제어 평면 누락 |
| 적용 판단 확인 | mTLS, traffic management, observability, overhead | 모든 MSA에 필수로 단정 |

> 요약: 이 문제는 서비스 간 통신 정책을 코드 밖에서 표준화하는 구조와 도입 조건을 묻는다.

---

## Ⅰ. 개요 및 필요성

- 개요: MSA 통신 정책 인프라 계층
- 배경: 서비스 수가 증가하면 인증, 재시도, 타임아웃, 추적 코드가 서비스별로 중복됨.
- 필요성: east-west traffic에 mTLS, traffic split, trace propagation을 일관 적용해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Service A -> Data Plane Proxy -> Service B
Control Plane -> Policy / Certificate / Route Config -> Data Plane Proxy
Data Plane Proxy -> Metric / Log / Trace -> Observability Backend
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Plane | 실제 트래픽 처리 | sidecar, node proxy, waypoint 등 구현 차이 |
| Control Plane | 정책·인증서·라우팅 설정 배포 | xDS 계열 설정 전파 |
| Policy | mTLS, authorization, retry, timeout | namespace·service 단위 적용 |
| Telemetry | metric, log, trace 수집 | RED 지표와 trace id 연계 |

> 요약: 서비스 메시는 데이터 평면이 트래픽을 처리하고 제어 평면이 정책과 인증서를 배포하는 구조다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 등록 -> 정책 작성 -> 제어 평면 설정 배포
-> 프록시가 요청 가로채기 -> mTLS / 라우팅 / retry 적용
-> telemetry 전송 -> 정책 조정
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 서비스와 워크로드 등록 | service discovery 일치 |
| 2 | 라우팅·보안 정책 정의 | policy validation |
| 3 | 프록시에 설정 전파 | config sync 상태 |
| 4 | 요청 처리와 telemetry 수집 | p95 latency, error rate, trace sampling |

> 요약: 서비스 메시는 정책을 프록시에 전파하고 프록시가 서비스 간 호출에 보안·라우팅·관측성을 적용한다.

---

## Ⅳ. 특징

| 구분 | 라이브러리 기반 통제 | Service Mesh | 판단 기준 |
|:---|:---|:---|:---|
| 적용 위치 | 애플리케이션 코드 | 인프라 프록시 | 언어·프레임워크 다양성 |
| 보안 | 서비스별 구현 | mTLS와 정책 일괄 적용 | zero trust 요구 |
| 배포 제어 | 코드 배포 필요 | 정책 변경으로 traffic split | canary·blue-green 빈도 |
| 비용 | 런타임 단순 | 프록시 자원과 운영 복잡도 추가 | pod 수, 요청량 |

> 요약: 서비스 메시는 다언어 MSA의 통신 정책 표준화에 유리하지만 프록시 자원과 운영 복잡도를 함께 평가해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | API Gateway 중심 north-south | service mesh east-west | 내부 서비스 호출 통제 필요 |
| 비용/성능 | 앱 라이브러리 의존 | 프록시 hop 추가 | p95 지연 예산 |
| 운영/위험 | 서비스별 설정 편차 | 중앙 정책 표준화 | 정책 변경 감사 필요 |

> 요약: 외부 API 진입은 Gateway, 내부 서비스 간 보안·관측성 통제는 Service Mesh가 담당한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 지연 증가 | 프록시 hop과 TLS 처리 | timeout budget, connection reuse | p95/p99 latency |
| 정책 오설정 | 라우팅·인가 규칙 충돌 | dry-run, staged rollout | 4xx/5xx 급증 |
| 운영 부담 | control plane 장애와 설정 폭증 | HA control plane, GitOps | config sync error |

> 요약: 서비스 메시 리스크는 지연, 정책 오설정, 운영 부담이며 단계 배포와 설정 검증으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 통신 품질 | SLO error budget 이내 | RED metric |
| 보안 | workload 간 mTLS 적용률 100% | certificate audit |
| 관측성 | trace id 전파 누락 0건 | tracing backend |

> 요약: 서비스 메시 성과는 지연 예산, mTLS 적용률, trace 전파율로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 결제·주문 등 핵심 namespace부터 mTLS와 authorization policy를 적용하고 범위를 단계 확대함.
2. canary 배포에는 traffic split 1% -> 10% -> 50% -> 100%와 error rate 중단 조건을 설정함.
3. mesh telemetry를 OpenTelemetry, Prometheus, tracing backend와 연결해 서비스별 SLO를 계산함.

**결론 (2줄):**
- 기술사 판단: 다언어 MSA와 내부 호출 보안 요구가 크면 Service Mesh를 선택하고, 소규모 서비스는 Gateway와 표준 라이브러리로 시작함.
- 향후 방향: 서비스 메시는 sidecar 방식과 node-level 방식이 공존하며 Kubernetes 네트워크·보안·관측성 계층으로 수렴함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "서비스 메시를 설명하시오" | 제어 평면과 데이터 평면 흐름 | API Gateway·라이브러리 대비 차이 |
| 요구사항 명시형 | "MSA 통신 보안 방안을 제시하시오" | mTLS·인가·traffic policy 적용 절차 | 지연·정책 오설정 리스크 |

> 요약: 설명형은 구조를, 보안·운영형은 정책 적용과 검증 지표를 중심으로 작성한다.
