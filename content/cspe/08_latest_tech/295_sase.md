---
title: "SASE 보안접근서비스엣지 (Secure Access Service Edge)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 295
extra:
  question_no: "295"
  exam_status: "기출"
  exam_history: "135회, 136회"
---

## 미리 알고가기

- SASE는 네트워크와 보안 기능을 클라우드 기반 서비스로 통합해 사용자와 지점과 애플리케이션 접근을 보호하는 아키텍처임
- SD-WAN과 보안 서비스가 결합된다는 점이 핵심임
- 원격 근무와 SaaS 중심 환경에서 기존 데이터센터 중심 보안 모델의 한계를 보완함

## Ⅰ. 개요

- **정의/개념**: SASE는 네트워크 연결 기능과 보안 검증 기능을 클라우드 엣지 서비스로 통합하여 사용자와 지점과 디바이스가 어디서든 안전하게 애플리케이션에 접근하도록 만드는 보안 네트워크 아키텍처임
- **배경/필요성**: 원격 근무와 SaaS와 멀티클라우드 확산으로 트래픽이 데이터센터를 거치지 않는 경우가 많아 네트워크와 보안을 분리 운영하던 모델이 비효율적이 됨

## Ⅱ. 특징

- 네트워크와 보안을 단일 클라우드 엣지 구조로 통합함
- 사용자 위치와 애플리케이션 위치가 달라도 일관된 정책을 적용함
- SD-WAN과 ZTNA와 SWG와 CASB 같은 기능이 함께 동작함
- 전면 전환 시 기존 네트워크 구조와 운영 모델 재설계가 필요함

## Ⅲ. 종류 및 비교

| 판단 기준 | SASE | 전통적 VPN + Firewall | SSE |
|:---|:---|:---|:---|
| 구성 범위 | 네트워크 + 보안 통합 | 분리된 네트워크와 보안 | 보안 기능 중심 |
| 원격 환경 적합성 | 높음 | 중간 | 높음 |
| 지점 연결 최적화 | 높음 | 낮음 | 낮음 |
| 대표 가치 | 통합 엣지 아키텍처 | 기존 투자 활용 | 사용자 중심 보안 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| SD WAN Fabric | 지점과 사용자 트래픽을 최적 경로로 연결해 네트워크 효율과 가용성을 높이는 연결 계층임 |
| Security Service Edge | ZTNA와 SWG와 CASB 같은 보안 기능을 클라우드 서비스로 제공하는 보호 계층임 |
| Identity Context Engine | 사용자와 단말과 위치 맥락을 결합해 접근 정책 판단에 활용하는 신원 맥락 계층임 |
| Cloud Edge PoP | 분산된 엣지 거점이 트래픽을 수용하고 정책을 집행하는 실제 서비스 진입점임 |
| Policy Orchestrator | 네트워크와 보안 규칙을 일관되게 배포하고 관리하는 중앙 제어 계층임 |

```text
+---------+    +-------------+    +----------------+    +-------------+
| User/BR | -> | Edge PoP    | -> | Security + SDWAN| -> | App / SaaS |
+---------+    +-------------+    +----------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 접속 요청    | -> | 엣지 유입    | -> | 신원과 정책 판단 | -> | 최적 경로 전달 | -> | 보안 검증 지속 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **접속 요청**: 사용자나 지점이 애플리케이션 접근을 요청함
2. **엣지 유입**: 가까운 PoP가 트래픽을 수용함
3. **신원과 정책 판단**: 사용자 맥락과 보안 정책을 평가함
4. **최적 경로 전달**: SD-WAN이 최적 경로로 트래픽을 보냄
5. **보안 검증 지속**: 세션 동안 보호 정책을 계속 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 네트워크와 보안 통합 범위를 무리하게 넓히면 전환 초기에 운영 복잡도와 정책 충돌이 커질 수 있음
   - 해결방안: phased SASE adoption과 domain based policy migration을 적용하고 migration incident rate와 policy conflict count로 검증함
2. 문제: 엣지 PoP 품질과 지역 커버리지가 부족하면 사용자 경험과 지연 특성이 기대보다 나빠질 수 있음
   - 해결방안: PoP performance benchmark와 geo coverage assessment를 적용하고 nearest PoP latency와 user experience satisfaction score로 검증함
3. 문제: 통합 플랫폼 의존이 커지면 특정 사업자 구조와 기능 범위에 종속될 수 있음
   - 해결방안: vendor capability review와 exit architecture planning을 적용하고 provider lock in risk score와 migration readiness index로 검증함

## Ⅶ. 적용 사례

- 글로벌 네트워크 팀이 단계적 SASE 전환을 운영하며 확인 지표는 migration incident rate와 policy conflict count임
- 원격 근무 인프라가 PoP 성능 검증을 수행하며 확인 지표는 nearest PoP latency와 user experience satisfaction score임
- 보안 아키텍처 조직이 사업자 이탈 설계를 유지하며 확인 지표는 provider lock in risk score와 migration readiness index임

## Ⅷ. 결론

SASE는 네트워크와 보안을 엣지에서 통합하는 전략이므로 PoP 품질과 정책 이행 방식과 벤더 종속성까지 함께 설계해야 함.
