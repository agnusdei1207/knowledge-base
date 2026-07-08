---
title: "Zero Trust Architecture 제로트러스트 아키텍처 (Zero Trust Architecture)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 294
extra:
  question_no: "294"
  exam_status: "기출"
  exam_history: "126회, 134회, 135회, 136회"
---

## 미리 알고가기

- Zero Trust는 네트워크 내부냐 외부냐로 신뢰를 나누지 않고 모든 접근을 계속 검증하는 보안 원칙임
- 사용자와 디바이스와 애플리케이션과 데이터 단위의 세밀한 접근 제어가 핵심임
- VPN 대체 기술이 아니라 보안 설계 원칙과 참조 아키텍처로 이해해야 함

## Ⅰ. 개요

- **정의/개념**: Zero Trust Architecture는 어떤 사용자나 단말이나 서비스도 기본적으로 신뢰하지 않고 요청마다 신원과 상태와 맥락을 검증해 최소 권한 접근만 허용하는 보안 아키텍처임
- **배경/필요성**: 원격 근무와 클라우드와 공급망 연결이 늘면서 경계형 보안만으로는 내부 확산과 계정 탈취와 권한 오남용을 막기 어려워짐

## Ⅱ. 특징

- 지속 검증과 최소 권한을 기본 원칙으로 삼음
- 네트워크 세분화와 신원 중심 접근 제어를 결합함
- 사용자와 디바이스 상태를 맥락적으로 반영함
- 단일 제품이 아니라 IAM과 네트워크와 관측이 결합된 구조임

## Ⅲ. 종류 및 비교

| 판단 기준 | Zero Trust | Perimeter Security | VPN 중심 접근 |
|:---|:---|:---|:---|
| 신뢰 기준 | 요청별 지속 검증 | 내부망 기본 신뢰 | 접속 후 내부 신뢰 |
| 세분 권한 | 높음 | 낮음 | 낮음 |
| 원격 환경 적합성 | 높음 | 낮음 | 중간 |
| 핵심 통제 | identity, device, context | firewall | tunnel access |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Identity Provider | 사용자와 서비스 계정의 신원을 관리해 접근 검증의 기준점을 제공하는 핵심 신원 계층임 |
| Device Trust Engine | 단말의 보안 상태와 등록 여부를 확인해 접근 조건에 반영하는 디바이스 검증 계층임 |
| Policy Decision Point | 요청 맥락과 정책을 비교해 허용과 차단과 추가 인증 여부를 결정하는 판단 엔진임 |
| Policy Enforcement Point | 결정된 정책을 실제 네트워크와 애플리케이션 경계에서 집행하는 실행 계층임 |
| Telemetry and Risk Context | 로그와 이상 징후와 사용자 행위를 수집해 실시간 위험 기반 접근 제어를 가능하게 하는 관측 계층임 |

```text
+---------+    +------------------+    +------------------+    +-------------+
| User/Dev| -> | Identity/Device  | -> | Policy Decision  | -> | Enforcement |
+---------+    +------------------+    +------------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 접근 요청    | -> | 신원/단말 검증 | -> | 정책 판단    | -> | 최소권한 허용 | -> | 지속 모니터링 |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **접근 요청**: 사용자나 서비스가 리소스 접근을 요청함
2. **신원과 단말 검증**: 인증과 단말 상태를 확인함
3. **정책 판단**: 위치와 시간과 위험도를 반영해 허용 여부를 정함
4. **최소권한 허용**: 필요한 범위만 접근을 허용함
5. **지속 모니터링**: 세션 중에도 이상 징후를 추적함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 애플리케이션과 사용자 맥락을 고려하지 않은 일괄 정책은 사용성 저하와 정책 예외 남발을 유발할 수 있음
   - 해결방안: context aware policy design과 adaptive authentication을 적용하고 access friction score와 exception request rate로 검증함
2. 문제: IAM과 네트워크와 단말 관리가 분절되면 제로트러스트 정책이 실시간으로 일관되게 집행되지 않을 수 있음
   - 해결방안: integrated control plane과 shared telemetry fabric을 적용하고 policy propagation latency와 inconsistent enforcement incident count로 검증함
3. 문제: 기존 내부망 구조를 유지한 채 부분 기술만 도입하면 내부 수평 확산 차단 효과가 약할 수 있음
   - 해결방안: micro segmentation roadmap과 asset trust mapping을 적용하고 lateral movement containment score와 segmented asset coverage로 검증함

## Ⅶ. 적용 사례

- 엔터프라이즈 보안팀이 상황 기반 정책을 운영하며 확인 지표는 access friction score와 exception request rate임
- 클라우드 조직이 통합 제어 평면을 구축하며 확인 지표는 policy propagation latency와 inconsistent enforcement incident count임
- 금융권이 마이크로세그멘테이션 로드맵을 적용하며 확인 지표는 lateral movement containment score와 segmented asset coverage로 검증함

## Ⅷ. 결론

Zero Trust는 제품 도입이 아니라 검증과 최소 권한과 세분화 원칙을 전 구간에 일관되게 연결하는 아키텍처 전환임.
