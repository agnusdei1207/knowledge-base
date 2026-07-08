---
title: "Cilium (Cilium)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 269
extra:
  question_no: "269"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- Cilium은 eBPF 기반으로 Kubernetes 네트워킹과 보안 정책을 구현하는 클라우드 네이티브 네트워크 플랫폼임
- 전통적 iptables 기반 CNI보다 더 세밀한 정책과 관측 기능을 제공하는 것이 강점임
- eBPF 이해가 부족하면 운영 난도가 높아질 수 있음

## Ⅰ. 개요

- **정의/개념**: Cilium은 eBPF를 활용해 Kubernetes 환경에서 네트워크 연결과 보안 정책과 서비스 로드밸런싱과 관측 기능을 제공하는 클라우드 네이티브 네트워킹 플랫폼임
- **배경/필요성**: 대규모 Kubernetes 환경에서는 기존 네트워크 플러그인의 정책 성능과 관측 한계가 드러나 커널 수준에서 더 효율적으로 제어하는 방식이 요구됨

## Ⅱ. 특징

- eBPF 기반으로 고성능 네트워킹과 정책 집행이 가능함
- L3에서 L7까지 세밀한 보안 정책을 적용할 수 있음
- 흐름 관측과 서비스 연결 상태를 세밀하게 가시화할 수 있음
- 커널 기능 의존성과 운영 학습 비용이 존재함

## Ⅲ. 종류 및 비교

| 판단 기준 | Cilium | iptables 기반 CNI | 단순 Overlay Network |
|:---|:---|:---|:---|
| 정책 성능 | 높음 | 중간 | 낮음 |
| 관측성 | 매우 높음 | 제한적 | 낮음 |
| 구현 기반 | eBPF | iptables | encapsulation 중심 |
| 운영 난도 | 중간 이상 | 중간 | 낮음 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cilium Agent | 각 노드에서 eBPF 프로그램 배포와 정책 적용과 엔드포인트 상태 관리를 수행하는 핵심 에이전트임 |
| eBPF Data Path | 패킷 처리와 서비스 로드밸런싱과 정책 집행을 커널에서 수행하는 고성능 데이터 경로임 |
| Identity and Policy Engine | 워크로드 신원과 정책 매핑을 통해 세밀한 네트워크 접근 제어를 수행하는 보안 계층임 |
| Hubble Observability | 흐름과 서비스 호출 상태를 시각화해 운영자가 네트워크를 분석하게 하는 관측 계층임 |
| CNI Integration | Kubernetes 네트워크 플러그인으로 동작해 Pod 연결과 서비스 연계를 제공하는 통합 계층임 |

```text
+-------------- Node ----------------+
| Cilium Agent -> eBPF Data Path     |
| Pods / Services / Policy / Hubble  |
+------------------------------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 정책 선언    | -> | Agent 수신   | -> | eBPF 배포    | -> | 패킷 처리    | -> | 흐름 관측    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **정책 선언**: 운영자가 네트워크와 보안 정책을 정의함
2. **Agent 수신**: Cilium Agent가 정책과 엔드포인트 상태를 반영함
3. **eBPF 배포**: 필요한 프로그램을 커널 후크에 로드함
4. **패킷 처리**: 데이터 경로에서 정책과 로드밸런싱을 수행함
5. **흐름 관측**: Hubble 등으로 통신 상태를 시각화함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 커널 기능 차이와 eBPF 의존성이 크면 노드별 동작 편차와 배포 실패가 발생할 수 있음
   - 해결방안: kernel readiness baseline과 compatibility validation을 적용하고 node compatibility rate와 rollout failure rate로 검증함
2. 문제: 세밀한 정책이 많아질수록 팀 간 정책 충돌과 의도치 않은 통신 차단이 늘어날 수 있음
   - 해결방안: policy simulation과 staged enforcement를 적용하고 policy conflict count와 unintended deny incident rate로 검증함
3. 문제: 관측 기능과 보안 기능을 동시에 많이 쓰면 커널 오버헤드와 운영 복잡도가 증가할 수 있음
   - 해결방안: observability sampling policy와 performance budget control을 적용하고 datapath overhead ratio와 operator troubleshooting time으로 검증함

## Ⅶ. 적용 사례

- Kubernetes 플랫폼이 커널 준비도 기준을 적용하며 확인 지표는 node compatibility rate와 rollout failure rate임
- 멀티팀 서비스가 정책 시뮬레이션을 운영하며 확인 지표는 policy conflict count와 unintended deny incident rate임
- 보안 관측 환경이 샘플링 정책을 적용하며 확인 지표는 datapath overhead ratio와 operator troubleshooting time임

## Ⅷ. 결론

Cilium은 eBPF 기반 클라우드 네트워킹의 강력한 구현체이지만 커널 호환성과 정책 거버넌스와 관측 오버헤드를 함께 다뤄야 안정적으로 운영됨.
