---
title: "QKD 양자키분배 (Quantum Key Distribution)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 347
extra:
  question_no: "347"
  exam_status: "기출"
  exam_history: "126회"
---

## 미리 알고가기

- QKD는 양자 상태의 측정 교란 특성을 이용해 대칭키를 안전하게 분배하는 기술임
- 암호화 자체를 수행하는 것이 아니라 키 분배 구간을 보호하는 물리 계층 보안 기술로 이해해야 함
- 양자 채널 외에도 고전 인증 채널과 키 관리 체계가 함께 있어야 실무 적용이 가능함

## Ⅰ. 개요

- **정의/개념**: Quantum Key Distribution은 광자 같은 양자 상태를 이용해 통신 당사자가 도청 여부를 탐지하면서 대칭 암호용 비밀키를 생성하고 공유하는 물리 기반 키 분배 기술임
- **배경/필요성**: 공개키 기반 키 교환이 미래 양자 공격에 취약할 수 있다는 우려와 최고 수준의 키 분배 신뢰 요구가 결합되면서 물리 법칙 기반의 키 분배 기술 필요성이 제기됨

## Ⅱ. 특징

- 도청 행위가 양자 상태를 교란하므로 통계적으로 침입을 감지할 수 있음
- 대칭키 암호와 결합해 높은 기밀성 통신을 구성할 수 있음
- 전용 광 채널과 거리 제약과 장비 비용이 크다는 한계가 있음
- 인증된 고전 채널이 없으면 중간자 공격에 취약할 수 있어 단독 기술로는 충분하지 않음

## Ⅲ. 종류 및 비교

| 판단 기준 | Classical Key Exchange | PQC KEM | QKD |
|:---|:---|:---|:---|
| 보안 근거 | 계산 난이도 | 양자내성 계산 난이도 | 물리 법칙 |
| 필요 인프라 | 일반 네트워크 | 일반 네트워크 | 양자 채널 + 인증 채널 |
| 적용 범위 | 광범위 | 광범위 | 제한적 고신뢰 구간 |
| 대표 한계 | 양자 위협 | 전환 복잡도 | 거리와 비용 제약 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Quantum Channel | 광자 전송 경로가 양자 상태를 전달해 도청 탐지 가능성을 제공하는 핵심 물리 계층임 |
| Photon Source and Detector | 송신과 수신 장비가 양자 상태를 생성하고 측정해 키 생성의 품질과 거리 한계를 좌우하는 장치 계층임 |
| Authenticated Classical Channel | basis 정보 교환과 오류 정정과 프라이버시 증폭을 수행해 최종 비밀키 합의로 이어지는 보조 통신 계층임 |
| Error Reconciliation and Privacy Amplification | 전송 오류를 줄이고 도청자가 얻었을 수 있는 정보를 제거해 실사용 가능한 비밀키로 정제하는 후처리 계층임 |
| Key Management Integration | 생성된 키를 VPN과 암호 장비와 애플리케이션에 배포해 실제 통신 보안으로 연결하는 운영 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Quantum     | -> | Photon      | -> | Classical   | -> | Key Mgmt /  |
| Channel     |    | Tx / Rx     |    | Auth + Post |    | Crypto Use  |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 양자 상태 전송 | -> | 수신/측정     | -> | basis sift  | -> | 오류 정정/증폭 | -> | 비밀키 사용    |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **양자 상태 전송**: 송신자가 광자 상태를 전송함
2. **수신과 측정**: 수신자가 상태를 측정함
3. **basis sift**: 고전 채널로 측정 기준을 맞춰 유효 비트를 남김
4. **오류 정정과 증폭**: 오류를 줄이고 도청 가능 정보를 제거함
5. **비밀키 사용**: 정제된 키를 대칭 암호에 적용함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 광 손실과 거리 한계가 크면 장거리 환경에서 키 생성률이 낮아져 실제 서비스 적용성이 떨어질 수 있음
   - 해결방안: trusted repeater architecture와 link budget optimization을 적용하고 secure key rate over distance와 long haul service availability로 검증함
2. 문제: 장비 구현 취약점이 있으면 이론적 안전성과 달리 side channel 형태의 공격에 노출될 수 있음
   - 해결방안: implementation security audit와 device vulnerability testing을 적용하고 device side channel test pass rate와 patched vulnerability recurrence count로 검증함
3. 문제: 인증된 고전 채널과 키 관리 연계가 약하면 생성된 키를 실제 통신 보안 체계에 안정적으로 연결하지 못할 수 있음
   - 해결방안: authenticated control channel integration과 downstream key lifecycle governance를 적용하고 authenticated session establishment rate와 generated key utilization ratio로 검증함

## Ⅶ. 적용 사례

- 국가 백본망이 중계 기반 장거리 구조를 운영하며 확인 지표는 secure key rate over distance와 long haul service availability임
- 양자 통신 장비 검증팀이 구현 보안 감사를 수행하며 확인 지표는 device side channel test pass rate와 patched vulnerability recurrence count임
- 보안 운영센터가 키 수명주기 연계를 적용하며 확인 지표는 authenticated session establishment rate와 generated key utilization ratio임

## Ⅷ. 결론

QKD는 계산 난이도 대신 물리 법칙에 기반한 키 분배 기술이지만 전용 인프라와 인증 체계와 운영 연계가 함께 있어야 실전 가치가 생김.
