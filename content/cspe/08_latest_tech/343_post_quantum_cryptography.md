---
title: "Post-Quantum Cryptography 양자내성암호 (Post-Quantum Cryptography)"
date: "2026-07-08"
tags:
  - "cspe-latest-tech"
weight: 343
extra:
  question_no: "343"
  exam_status: "기출"
  exam_history: "126회, 129회, 135회, 136회"
  exam_note: "전망"
---

## 미리 알고가기

- PQC는 양자컴퓨터 공격에도 안전하도록 설계된 공개키 기반 암호 계열을 뜻함
- 기존 RSA와 ECC는 쇼어 알고리즘에 취약할 수 있어 장기 정보 보호를 위해 전환 준비가 필요함
- KEM과 전자서명과 하이브리드 전환 전략을 함께 고려해야 현실적인 migration이 가능함

## Ⅰ. 개요

- **정의/개념**: Post-Quantum Cryptography는 양자컴퓨터가 실용화되어도 공개키 교환과 전자서명 기능을 유지하도록 격자 기반과 해시 기반 등 양자내성 수학 문제를 사용하는 차세대 공개키 암호 체계임
- **배경/필요성**: 현재 인터넷과 PKI의 핵심인 RSA와 ECC가 양자 알고리즘에 의해 위협받을 수 있어 장기 기밀성과 미래 복호 위험을 줄이기 위한 암호 전환이 요구됨

## Ⅱ. 특징

- 양자내성을 제공하면서도 기존 디지털 인프라와 호환 가능한 소프트웨어 구현이 가능함
- 양자 하드웨어 없이도 오늘 바로 도입과 시험이 가능한 점이 장점임
- 키와 서명과 ciphertext 크기가 기존 방식보다 커지는 경우가 많음
- 알고리즘 교체만으로 끝나지 않고 인증서와 프로토콜과 HSM과 운영 체계까지 함께 바뀌어야 함

## Ⅲ. 종류 및 비교

| 판단 기준 | Classical PKC | Lattice based PQC | Hash based PQC |
|:---|:---|:---|:---|
| 양자 공격 저항 | 낮음 | 높음 | 높음 |
| 대표 기능 | RSA, ECC | KEM, 서명 | 주로 서명 |
| 크기 특성 | 비교적 작음 | 중간~큼 | 서명 크기 큼 |
| 대표 장점 | 성숙도 높음 | 범용 전환성 | 보수적 안전성 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Algorithm Family Selection | KEM과 서명 알고리즘 계열을 선택해 조직의 보안 요구와 성능 요구를 맞추는 전략 계층임 |
| Protocol and PKI Integration | TLS와 VPN와 인증서 체계에 PQC 알고리즘을 연결해 실제 통신 보호로 이어지게 하는 적용 계층임 |
| Hybrid Migration Design | 기존 알고리즘과 PQC를 병행 적용해 상호운용성과 보수적 전환을 동시에 확보하는 전환 계층임 |
| Key and Certificate Lifecycle | 큰 키와 새 인증서 형식을 안전하게 발급하고 저장하고 폐기해 운영 안정성을 유지하는 관리 계층임 |
| Crypto Agility Governance | 알고리즘 변경과 취약성 대응을 빠르게 수행할 수 있게 암호 유연성을 설계하는 장기 운영 계층임 |

```text
+-------------+    +-------------+    +-------------+    +-------------+
| Algorithm   | -> | Protocol /  | -> | Hybrid      | -> | Lifecycle / |
| Selection   |    | PKI         |    | Migration   |    | Agility     |
+-------------+    +-------------+    +-------------+    +-------------+
```

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
| 보호 자산 식별 | -> | 알고리즘/프로토콜 선정 | -> | 하이브리드 시험 | -> | 인증서/키 전환 | -> | 운영 모니터링   |
+-------------+    +-------------+    +-------------+    +-------------+    +-------------+
```

1. **보호 자산 식별**: 장기 기밀성과 서명 신뢰가 필요한 자산을 식별함
2. **알고리즘과 프로토콜 선정**: KEM과 서명과 적용 프로토콜을 정함
3. **하이브리드 시험**: 기존 암호와 PQC 병행 동작을 검증함
4. **인증서와 키 전환**: 발급과 저장과 배포 체계를 갱신함
5. **운영 모니터링**: 상호운용성과 성능과 취약성 대응을 점검함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 키와 서명 크기 증가를 고려하지 않으면 네트워크 성능과 저장소와 인증서 처리 체계에 예상보다 큰 부담이 생길 수 있음
   - 해결방안: size impact benchmarking과 protocol specific tuning을 적용하고 handshake size growth tolerance와 certificate processing latency로 검증함
2. 문제: 레거시 장비와 HSM과 라이브러리가 PQC를 지원하지 않으면 전환 계획이 문서 수준에 머물 수 있음
   - 해결방안: dependency compatibility inventory와 phased crypto upgrade roadmap을 적용하고 PQC ready dependency coverage와 unsupported critical component count로 검증함
3. 문제: 양자 위협만 강조하다가 실제 운영 자산별 전환 우선순위를 정하지 못하면 투자 대비 효과가 떨어질 수 있음
   - 해결방안: data longevity risk model과 use case based migration prioritization을 적용하고 prioritized asset protection coverage와 migration ROI traceability score로 검증함

## Ⅶ. 적용 사례

- PKI 조직이 크기 영향 벤치마킹을 운영하며 확인 지표는 handshake size growth tolerance와 certificate processing latency임
- 인프라 보안팀이 의존성 호환성 인벤토리를 구축하며 확인 지표는 PQC ready dependency coverage와 unsupported critical component count임
- 암호 전환 프로그램이 자산 우선순위 모델을 적용하며 확인 지표는 prioritized asset protection coverage와 migration ROI traceability score임

## Ⅷ. 결론

PQC는 미래 위협 대비 기술이지만 실제 전환은 프로토콜과 PKI와 운영 자산 전반의 구조 변경이므로 하이브리드 이행 전략이 핵심임.
