---
title: "디바이스 DNA (Device DNA)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 84
extra:
  question_no: "084"
  exam_status: "기출"
  exam_history: "125회"
---

## 미리 알고가기

- Device DNA는 장치마다 다른 하드웨어 고유 식별 정보를 활용하는 개념임
- 고정 unique ID나 PUF 응답이나 fuse 값이 구현 수단이 될 수 있음
- 인증서 바인딩과 provisioning과 attestation이 함께 설계돼야 함

## Ⅰ. 개요

- **정의/개념**: Device DNA는 칩이나 장치가 가진 고유 식별 정보나 물리 특성을 이용해 장치 신원을 식별하고 위조와 복제를 방지하는 하드웨어 기반 식별 체계임
- **배경/필요성**: 대량 배포되는 IoT와 차량과 산업 장비는 소프트웨어 시리얼 번호만으로는 위조와 복제를 막기 어려워, 장치 본체에 뿌리 둔 신원 수단이 필요함

## Ⅱ. 특징

- 장치 고유성을 기반으로 공급망 추적과 원격 인증에 활용할 수 있음
- 소프트웨어 값보다 위조 저항성이 높지만 설계에 따라 읽기 가능 범위가 달라짐
- 단순 식별자 노출만으로는 보안이 완성되지 않으며 인증서, attestation이 필요함
- 개인 식별성 및 프라이버시 고려가 필요한 환경도 존재함

## Ⅲ. 종류 및 비교

| 판단 기준 | 소프트웨어 시리얼 | Device DNA |
|:---|:---|:---|
| 변경 가능성 | 높음 | 낮음 |
| 위조 저항성 | 낮음 | 중간~높음 |
| 활용 방식 | 등록 번호 | 하드웨어 신원 바인딩 |
| 운영 요구 | 단순 발급 | provisioning, attestation 필요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Unique Hardware ID | fuse, secure ID, PUF 같은 고유 식별 원천이 됨 |
| Provisioning System | 생산 단계에서 장치 ID와 키와 인증서를 바인딩해 초기 신뢰를 만듦 |
| Attestation Service | 장치가 실제 자신임을 원격으로 증명하게 하는 운영 계층임 |
| Access, Privacy Policy | 누가 식별자를 읽고 어떤 서비스와 연결하는지 통제해 오남용을 막음 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 고유 ID 생성    | --> | 등록/인증서 바인딩 | --> | 장치 인증 요청  | --> | 신원 검증/사용  |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **고유 ID 생성**: 장치 제조 시 고유 식별 원천을 확보함
2. **등록 및 인증서 바인딩**: 서비스와 연결할 신뢰 정보를 생성함
3. **장치 인증 요청**: 서비스가 장치 신원 증명을 요구함
4. **신원 검증 및 사용**: 위조 여부를 판정하고 접근 권한을 부여함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 읽기 가능한 고유 ID만 노출되면 공격자가 식별자를 복사해 위조 장치에 재사용할 수 있음
   - 해결방안: challenge-response attestation을 적용하고 clone detection rate와 attestation success rate로 검증함
2. 문제: provisioning이 부실하면 장치 신원과 인증서 매핑 오류가 발생해 운영 신뢰가 무너질 수 있음
   - 해결방안: manufacturing PKI와 enrollment validation을 운영하고 provisioning defect rate와 identity binding accuracy로 검증함
3. 문제: 장치 식별자가 추적 목적으로 악용되면 프라이버시와 규제 이슈가 생길 수 있음
   - 해결방안: pseudonymous identifier와 접근 통제를 적용하고 privacy audit result와 identifier exposure count로 검증함

## Ⅶ. 적용 사례

- IoT 플랫폼 등록 단계에서는 Device DNA를 인증서와 결합하고, enrollment accuracy와 counterfeit detection rate로 결과를 확인함
- 자동차 부품 정품 인증에서는 하드웨어 식별자를 활용하고, anti-cloning success rate와 supply chain traceability로 결과를 확인함
- 산업 장비 원격 관리에서는 attestation 기반 신원 검증을 적용하고, attestation pass rate와 unauthorized device rejection rate로 결과를 확인함

## Ⅷ. 결론

Device DNA의 가치는 ID 자체보다 그 ID를 신뢰 체계와 어떻게 연결하느냐에 있으므로, provisioning과 attestation 설계가 핵심임.
