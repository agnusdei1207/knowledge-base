---
title: "서비스 메시 - Istio·Envoy (Service Mesh)"
date: "2026-07-01"
tags:
  - "cspe-software"
weight: 46
---

# 📖 【암기용】 개념 완전 이해

> 목적: 서비스 메시를 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 서비스 간 통신 기능을 애플리케이션 밖의 프록시 계층으로 분리한 인프라
- **왜 필요한가**: MSA에서는 timeout, retry, mTLS, traffic split, trace를 모든 서비스가 반복 구현하기 쉬움. Service Mesh는 이 통신 정책을 sidecar와 control plane으로 표준화함.
- **핵심 직관**: 도로마다 신호등과 CCTV를 설치하고 중앙 교통센터가 정책을 내려 교통 흐름을 제어하는 구조임.

## 깊이 이해
- **배경·문제의식**: 서비스 수가 50개 이상이면 언어·프레임워크별 통신 정책이 달라지고, 보안·관측성 수준도 서비스마다 달라짐. 공통 통신 기능을 코드에서 떼어내야 함.
- **작동 원리**: 각 Pod 옆에 Envoy sidecar를 붙여 모든 inbound/outbound 트래픽을 통과시킴. Istio control plane은 라우팅, mTLS, retry, circuit breaking 정책을 sidecar에 배포함.
- **비유**: 각 사무실 문 앞에 경비원을 두고, 본부가 출입 규칙과 동선을 내려보내는 방식임.
- **구체 예시**: 신규 결제 서비스 v2에 10% 트래픽을 보내고, error rate 1% 초과 시 v1으로 되돌리는 canary 정책을 코드 수정 없이 적용함.
- **흔한 오해·주의점**: Service Mesh는 비즈니스 로직을 해결하지 않음. L7 통신 정책과 보안·관측성을 제공하며, 운영 복잡도와 프록시 지연을 추가함.

## 연결 개념
- Istio/Envoy: control plane과 data plane 구현체
- Zero Trust: 서비스 간 mTLS와 정책 기반 접근통제
- Observability: metric, log, trace 자동 수집

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: Service Mesh는 sidecar, control/data plane, mTLS, traffic policy, observability를 코드 외부에서 통제하는 구조로 답안을 구성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Service Mesh는 서비스 간 통신을 sidecar proxy가 처리하고 control plane이 정책을 배포하는 인프라 계층이다.
> 2. **가치**: mTLS, retry, timeout, traffic split, circuit breaking, tracing을 애플리케이션 코드 변경 없이 적용함.
> 3. **판단 포인트**: 서비스 수, 보안 요구, 트래픽 제어 요구가 높을 때 적용하며 sidecar 지연·운영 난이도·정책 충돌을 검증해야 함.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| Mesh 구조 이해 확인 | sidecar, data plane, control plane, Envoy, Istio | API Gateway와 역할 혼동 |
| 보안·통신 정책 판단 확인 | mTLS, authorization policy, traffic split | 단순 로드밸런서로 설명 |
| 운영 리스크 확인 | proxy overhead, policy drift, observability | sidecar 지연과 장애 범위 누락 |

> 요약: 이 문제는 서비스 간 동서 트래픽을 코드가 아닌 인프라 정책으로 통제하는 구조를 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 서비스 간 통신 제어 계층
- 배경: MSA 규모가 커지면 각 서비스가 인증, 암호화, retry, timeout, trace를 반복 구현해 언어별 편차와 정책 누락이 발생함.
- 필요성: Sidecar proxy와 control plane으로 mTLS, traffic shifting, retry budget, distributed tracing을 표준 적용하고 success rate와 p95 latency를 관측해야 함.

---

## Ⅱ. 구조 및 구성요소

```text
Service A -> Envoy Sidecar -> Network -> Envoy Sidecar -> Service B
              / mTLS / Retry / Timeout / Trace
Istio Control Plane -> Policy / Certificate / Route Config -> Envoy
Telemetry -> Metric / Log / Trace -> Observability
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Data Plane | Envoy sidecar가 실제 트래픽 처리 | inbound/outbound proxy |
| Control Plane | 정책·인증서·라우팅 설정 배포 | Istio istiod |
| Security Policy | mTLS, authorization, identity 관리 | SPIFFE ID, RBAC |
| Traffic Policy | canary, retry, timeout, circuit breaking | VirtualService, DestinationRule |

> 요약: Service Mesh는 data plane이 트래픽을 처리하고 control plane이 보안·라우팅·관측 정책을 배포한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
서비스 배포 -> sidecar 주입 -> 인증서 발급
-> control plane 정책 배포 -> Envoy가 트래픽 가로채기
-> mTLS/라우팅/재시도 수행 -> telemetry 수집
-> SLO와 정책 위반 점검
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | Pod 생성 시 sidecar injection | injection success rate 100% |
| 2 | workload identity와 인증서 발급 | cert rotation, SPIFFE ID |
| 3 | VirtualService로 라우팅 정책 적용 | v2 traffic 10% 등 split 검증 |
| 4 | Envoy가 mTLS, retry, timeout 처리 | handshake error, retry count |
| 5 | metric, access log, trace 수집 | telemetry coverage 95% 이상 |

> 요약: Mesh는 sidecar 주입 후 control plane 정책을 Envoy에 내려 서비스 간 통신을 일관된 방식으로 처리한다.

---

## Ⅳ. 특징

| 구분 | 애플리케이션 내 구현 | Service Mesh | 수치·판단 포인트 |
|:---|:---|:---|:---|
| 보안 | 서비스별 TLS 구현 | mTLS 자동화 | 서비스 간 암호화 100% |
| 트래픽 제어 | 코드·LB 설정 의존 | canary, mirroring, fault injection | 10% 단위 canary |
| 관측성 | SDK 직접 삽입 | proxy telemetry 자동 수집 | trace coverage 95% 이상 |
| 비용 | proxy 없음 | sidecar CPU/메모리 추가 | p95 proxy latency 5ms 이하 |

> 요약: Service Mesh는 통신 정책 표준화를 제공하지만 sidecar overhead와 정책 운영 역량을 요구한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 라이브러리 기반 resilience | sidecar proxy 기반 mesh | 다언어 서비스 20개 이상 |
| 비용/성능 | 앱 코드 직접 호출 | proxy hop 추가 | p95 overhead 5ms 이하 허용 |
| 운영/위험 | 코드별 정책 차이 | 중앙 정책 배포 | mesh SRE 운영 인력 확보 |

> 요약: Mesh는 서비스 수와 보안·트래픽 정책 요구가 높을 때 선택하며 지연 예산을 먼저 계산한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 정책 충돌 | VirtualService 중복 | policy lint, GitOps review | rejected config 수 |
| 지연 증가 | sidecar hop과 mTLS | resource limit, locality load balancing | p95/p99 latency |
| 장애 확대 | control plane 장애 | control plane HA, config cache | xDS push 실패율 |

> 요약: Mesh 리스크는 정책 충돌과 프록시 지연이며, GitOps 검증과 HA control plane으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 보안 | mTLS 적용률 100%, 인증서 자동 회전 | mesh dashboard, cert log |
| 트래픽 | canary error rate 1% 이하 | Envoy metric, SLO |
| 관측 | telemetry coverage 95% 이상 | Prometheus, Jaeger |

> 요약: Mesh 성공 여부는 mTLS 적용률, 트래픽 정책 품질, telemetry coverage로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. namespace 단위로 Istio sidecar injection을 적용하고 mTLS permissive에서 strict로 단계 전환함.
2. VirtualService와 DestinationRule로 canary 10%, retry 2회, timeout 1초, circuit breaking을 표준 정책으로 배포함.
3. Envoy metrics, access log, distributed trace를 Prometheus·Grafana·Jaeger에 연결해 SLO 위반을 알림화함.

**결론 (2줄):**
- 기술사 판단: 서비스 간 보안·트래픽·관측 정책이 분산되면 Service Mesh를 적용하고, 소규모 서비스에는 Gateway와 라이브러리 패턴을 우선 검토함.
- 향후 방향: Ambient mesh, eBPF 기반 dataplane, zero trust policy와 결합해 sidecar 부담을 줄이는 방향임.

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "Service Mesh를 설명하시오" | sidecar, control/data plane, mTLS 흐름 | Gateway·라이브러리 방식 대비 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "설계하시오" | Istio 정책 적용 절차와 지표 | overhead, 정책 충돌, HA 대응 |

> 요약: 설명형은 구조·정책 흐름, 설계형은 mTLS·traffic policy·관측 지표를 중심으로 전환한다.
