---
title: "Multi Cloud 멀티클라우드 (Multi Cloud)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 288
extra:
  question_no: "288"
  exam_status: "기출"
  exam_history: "135회"
---

## 미리 알고가기

- 멀티클라우드는 둘 이상의 퍼블릭 클라우드나 클라우드 서비스를 함께 사용하는 전략임
- 단순히 여러 클라우드를 쓰는 것이 아니라 벤더 의존성 분산과 서비스 최적 선택이 핵심 목적임
- 운영 복잡도가 크게 늘어나는 만큼 표준화와 거버넌스가 필수임

## Ⅰ. 개요

- **정의/개념**: Multi Cloud는 조직이 두 개 이상의 클라우드 사업자나 클라우드 플랫폼을 조합해 워크로드를 배치하고 서비스별 최적 기능을 선택하는 클라우드 활용 전략임
- **배경/필요성**: 단일 벤더 종속을 줄이고 지역별 규제와 가용성과 서비스 특화 기능을 동시에 고려하려는 요구가 증가하면서 멀티클라우드 전략이 확산됨

## Ⅱ. 특징

- 벤더 종속성과 장애 집중 위험을 줄일 수 있음
- 서비스별 최적 기능과 가격 정책을 선택할 수 있음
- 네트워크와 보안과 관측과 운영 도구 표준화가 매우 중요함
- 중복 운영과 데이터 이동 비용이 예상보다 커질 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | Multi Cloud | Single Cloud | Hybrid Cloud |
|:---|:---|:---|:---|
| 사용 환경 | 여러 클라우드 사업자 | 단일 사업자 | 클라우드와 온프레미스 혼합 |
| 유연성 | 높음 | 낮음 | 중간 |
| 운영 복잡도 | 매우 높음 | 낮음 | 높음 |
| 대표 목적 | 벤더 분산과 최적 선택 | 단순 운영 | 점진 전환과 규제 대응 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Cloud Portfolio | 각 클라우드 사업자의 서비스 특성과 비용과 규제 조건을 관리하는 전략 자산 집합임 |
| Common Control Layer | IAM과 네트워크와 보안과 배포 표준을 통합해 운영 복잡도를 줄이는 공통 제어 계층임 |
| Workload Placement Policy | 어떤 워크로드를 어느 클라우드에 둘지 결정해 비용과 성능과 규제를 균형화하는 배치 정책임 |
| Data and Connectivity Fabric | 클라우드 간 네트워크 연결과 데이터 복제를 관리해 분산 워크로드를 가능하게 하는 연결 계층임 |
| FinOps and Governance | 비용 배분과 계약 관리와 규제 준수 상태를 추적하는 관리 계층임 |

```text
+-----------+    +------------------+    +-----------+
| Cloud A   |<-> | Common Control   |<-> | Cloud B   |
+-----------+    +------------------+    +-----------+
         \____________ Data / Network _____________/
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 요구 분석    | -> | 워크로드 배치 | -> | 공통 정책 적용 | -> | 클라우드 연동 | -> | 비용과 성능 관측 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **요구 분석**: 서비스별 규제와 성능과 비용 요구를 파악함
2. **워크로드 배치**: 적절한 클라우드 사업자에 워크로드를 배치함
3. **공통 정책 적용**: 보안과 배포와 관측 표준을 일관되게 적용함
4. **클라우드 연동**: 네트워크와 데이터 복제를 구성함
5. **비용과 성능 관측**: 전체 포트폴리오를 지속 최적화함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 클라우드별 IAM과 네트워크와 관측 방식이 다르면 운영 표준이 무너지고 장애 대응 시간이 길어질 수 있음
   - 해결방안: common platform layer와 policy standardization을 적용하고 multi cloud operational variance score와 incident recovery time으로 검증함
2. 문제: 데이터 이동과 복제 설계가 부족하면 지연과 이중 비용이 예상보다 크게 발생할 수 있음
   - 해결방안: data locality policy와 inter cloud transfer optimization을 적용하고 cross cloud transfer cost ratio와 replication latency로 검증함
3. 문제: 벤더 분산 효과를 기대해도 실제로는 특정 클라우드 고유 서비스 의존이 커져 종속성이 다시 생길 수 있음
   - 해결방안: portability review와 lock in risk assessment를 적용하고 proprietary dependency ratio와 migration readiness score로 검증함

## Ⅶ. 적용 사례

- 글로벌 서비스가 공통 제어 계층을 운영하며 확인 지표는 multi cloud operational variance score와 incident recovery time임
- 데이터 플랫폼이 데이터 지역성 정책을 적용하며 확인 지표는 cross cloud transfer cost ratio와 replication latency임
- 플랫폼 조직이 종속성 평가를 수행하며 확인 지표는 proprietary dependency ratio와 migration readiness score임

## Ⅷ. 결론

멀티클라우드는 유연성과 분산 효과가 크지만 표준화된 공통 제어 계층과 데이터 이동 전략이 없으면 복잡도만 커질 수 있음.
