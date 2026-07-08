---
title: "SLH-DSA (Stateless Hash-Based Digital Signature Algorithm)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 346
extra:
  question_no: "346"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- SLH-DSA는 해시 함수 기반의 상태 없는 양자내성 전자서명 알고리즘임
- 격자 기반 서명과 달리 보수적 안전성에 강점을 두지만 서명 크기와 성능 부담이 큼
- stateful 서명과 달리 서명 횟수 관리 부담이 적어 운영 단순성이 높음

## Ⅰ. 개요

- **정의/개념**: SLH-DSA는 해시 기반 일회용 서명과 하이퍼트리 구조를 사용해 양자 공격에도 견디는 전자서명을 제공하는 상태 없는 해시 기반 PQC 서명 알고리즘임
- **배경/필요성**: 양자내성 서명 전환에서 특정 수학 문제 의존을 줄이고 보다 보수적으로 검증된 해시 함수 기반 대안을 확보하려는 요구가 커짐

## Ⅱ. 특징

- 해시 함수 보안성에 기반해 보수적 신뢰성이 높음
- 상태 없는 구조라 서명 사용량 관리 오류 위험이 적음
- 기존 서명보다 서명 크기와 검증 비용이 커질 수 있음
- 대량 트랜잭션이나 대규모 인증서 환경에서는 성능 부담이 크게 드러날 수 있음

## Ⅲ. 종류 및 비교

| 판단 기준 | ECDSA | ML-DSA | SLH-DSA |
|:---|:---|:---|:---|
| 양자내성 | 낮음 | 높음 | 높음 |
| 기반 원리 | 타원곡선 | 모듈 격자 | 해시 기반 |
| 운영 특성 | 성숙도 높음 | 균형형 | 보수적 안전성 |
| 크기/성능 | 작고 빠름 | 중간 | 크고 상대적으로 느림 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Hash Function Foundation | 보안성을 지탱하는 핵심 primitive로 전체 서명 체계의 무결성과 위조 저항성을 좌우하는 기반 계층임 |
| One Time Signature Structure | 일회용 서명 단위를 구성해 개별 메시지 서명을 안전하게 수행하는 하위 서명 계층임 |
| Hypertree Composition | 여러 서명 계층을 트리 구조로 연결해 상태 없는 장기 사용이 가능하도록 확장하는 상위 구조 계층임 |
| Key and Signature Generation | 공개키 생성과 메시지 서명을 수행해 실제 전자서명 기능을 구현하는 실행 계층임 |
| Verification and Deployment Integration | 검증 절차와 인증서 및 코드 서명 체계 연계를 담당해 운영 환경 적용 가능성을 만드는 통합 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Hash Basis  | -> | OTS Layer   | -> | Hypertree   | -> | Sign /      |
|             |    |             |    | Structure   |    | Verify      |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 키 생성       | -> | 해시 기반 서명  | -> | 트리 인증 정보 포함 | -> | 서명 전송     | -> | 검증 수행     |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **키 생성**: 공개키와 비밀키 구조를 생성함
2. **해시 기반 서명**: 일회용 서명 계층으로 메시지를 서명함
3. **트리 인증 정보 포함**: 상위 트리 경로를 함께 구성함
4. **서명 전송**: 메시지와 대형 서명을 전달함
5. **검증 수행**: 수신자가 트리와 해시를 검증함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 서명 크기가 매우 크면 네트워크 전송과 저장과 로그 보관 비용이 크게 증가할 수 있음
   - 해결방안: signature size impact profiling과 selective usage policy를 적용하고 storage overhead per signature와 transmission latency impact로 검증함
2. 문제: 검증 비용이 높은 환경에서는 대량 요청 처리나 대규모 인증 체계에서 병목이 발생할 수 있음
   - 해결방안: verification offload design과 high assurance workload targeting을 적용하고 verification throughput under peak load와 selective deployment efficiency score로 검증함
3. 문제: 격자 기반 서명과 함께 운영할 때 알고리즘 선택 기준이 불명확하면 복잡도만 늘고 보안 전략은 흐려질 수 있음
   - 해결방안: algorithm selection governance와 risk based signature portfolio를 적용하고 signature portfolio clarity score와 misapplied algorithm incident count로 검증함

## Ⅶ. 적용 사례

- 고신뢰 서명 체계가 선택적 적용 정책을 운영하며 확인 지표는 storage overhead per signature와 transmission latency impact임
- 검증 인프라가 오프로딩 설계를 적용하며 확인 지표는 verification throughput under peak load와 selective deployment efficiency score임
- 암호 거버넌스 조직이 서명 포트폴리오 기준을 운영하며 확인 지표는 signature portfolio clarity score와 misapplied algorithm incident count임

## Ⅷ. 결론

SLH-DSA는 보수적 양자내성 서명 대안이지만 큰 서명과 검증 비용을 감당할 사용처를 선별해 배치해야 실무성이 확보됨.
