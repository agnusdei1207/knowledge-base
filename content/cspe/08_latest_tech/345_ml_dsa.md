---
title: "ML-DSA (Module-Lattice Digital Signature Algorithm)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 345
extra:
  question_no: "345"
  exam_status: "기출"
  exam_history: "136회"
  exam_note: "전망"
---

## 미리 알고가기

- ML-DSA는 모듈 격자 기반의 양자내성 전자서명 알고리즘임
- 기존 RSA나 ECDSA 서명과 달리 양자 위협을 고려한 서명 체계로 인증서와 코드 서명에 적용 가능함
- 성능과 크기와 구현 안전성을 함께 고려해야 실제 운영에 안착함

## Ⅰ. 개요

- **정의/개념**: ML-DSA는 모듈 격자 기반 난제를 사용해 메시지 무결성과 서명자 인증을 제공하는 양자내성 전자서명 알고리즘으로 미래 양자 공격에도 위조 저항성을 유지하도록 설계된 서명 체계임
- **배경/필요성**: 전자서명과 인증서와 코드 서명의 기반인 기존 공개키 서명 체계가 양자 공격에 취약할 수 있어 장기 신뢰를 유지할 새로운 서명 표준이 필요해짐

## Ⅱ. 특징

- 양자내성을 제공하면서도 범용 서명 프로토콜에 통합 가능함
- 서명 생성과 검증 속도 측면에서 실무 전환 대상으로 자주 검토됨
- 인증서 체계와 소프트웨어 서명 생태계 확장에 적용 범위가 넓음
- 키와 서명 크기 증가와 side channel 대응이 구현 품질을 크게 좌우함

## Ⅲ. 종류 및 비교

| 판단 기준 | ECDSA | ML-DSA | SLH-DSA |
|:---|:---|:---|:---|
| 양자내성 | 낮음 | 높음 | 높음 |
| 기반 문제 | 타원곡선 | 모듈 격자 | 해시 기반 |
| 크기 특성 | 작음 | 중간~큼 | 서명 매우 큼 |
| 대표 장점 | 성숙도 높음 | 균형 잡힌 실용성 | 보수적 안전성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Key Generation | 공개키와 비밀키를 생성해 서명자 신뢰 체계의 기반 자격 정보를 준비하는 시작 계층임 |
| Signature Generation | 메시지와 비밀키를 사용해 위조 저항성을 가진 서명을 생성하는 송신 계층임 |
| Verification Logic | 공개키로 서명의 유효성을 확인해 메시지 무결성과 출처를 검증하는 검증 계층임 |
| Parameter Set Selection | 보안 강도와 성능과 크기의 균형을 조정해 환경별 적용 수준을 결정하는 정책 계층임 |
| Certificate and Signing Integration | PKI와 코드 서명과 문서 서명 체계에 알고리즘을 연결해 실제 운영으로 확장하는 통합 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| KeyGen      | -> | Sign        | -> | Signature   | -> | Verify      |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 키쌍 생성     | -> | 메시지 서명   | -> | 서명 전송     | -> | 공개키 검증   | -> | 무결성 판단   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **키쌍 생성**: 서명자가 공개키와 비밀키를 생성함
2. **메시지 서명**: 비밀키로 서명을 생성함
3. **서명 전송**: 메시지와 서명을 전달함
4. **공개키 검증**: 수신자가 공개키로 서명을 검증함
5. **무결성 판단**: 유효하면 메시지 출처와 무결성을 신뢰함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 서명과 키 크기 증가를 고려하지 않으면 인증서 체인과 코드 서명 배포 비용이 크게 늘 수 있음
   - 해결방안: certificate size impact analysis와 signing pipeline capacity tuning을 적용하고 artifact size growth tolerance와 signature verification latency로 검증함
2. 문제: 서명 구현에서 난수와 side channel 방어가 약하면 이론적 안전성과 달리 키 유출 가능성이 커질 수 있음
   - 해결방안: hardened implementation review와 side channel resistant signing runtime을 적용하고 implementation conformance score와 side channel leakage test result로 검증함
3. 문제: 기존 검증기와 PKI 도구가 새로운 서명 체계를 지원하지 않으면 전환이 부분 도입에 머물 수 있음
   - 해결방안: verifier ecosystem readiness audit와 hybrid certificate transition plan을 적용하고 PQC capable verifier coverage와 legacy verification failure count로 검증함

## Ⅶ. 적용 사례

- PKI 운영팀이 인증서 크기 영향 분석을 수행하며 확인 지표는 artifact size growth tolerance와 signature verification latency임
- 보안 구현팀이 강화된 서명 런타임을 적용하며 확인 지표는 implementation conformance score와 side channel leakage test result임
- 전환 프로그램이 검증기 준비도 감사를 운영하며 확인 지표는 PQC capable verifier coverage와 legacy verification failure count임

## Ⅷ. 결론

ML-DSA는 PQC 전자서명 전환의 실무 중심축이므로 서명 크기 영향과 검증 생태계 호환성을 함께 관리해야 실제 배포가 가능함.
