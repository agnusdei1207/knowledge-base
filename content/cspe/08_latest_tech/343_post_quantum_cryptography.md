---
title: "Post-Quantum Cryptography 양자내성암호 (Post-Quantum Cryptography)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 343
---

# 📖 【암기용】 개념 완전 이해

> 목적: PQC를 양자컴퓨터 공격에도 버티도록 설계된 고전 컴퓨터용 공개키 암호로 이해하게 만든다.

## 한눈에
- **개요**: 양자컴퓨터 공격을 고려해 설계된 공개키 암호 알고리즘과 전환 체계
- **왜 필요한가**: 충분한 규모의 양자컴퓨터가 Shor 알고리즘을 실행하면 RSA와 ECC 기반 공개키 암호가 위험해진다.
- **핵심 직관**: 양자컴퓨터를 쓰는 암호가 아니라, 현재 컴퓨터와 네트워크에서 양자 공격에 대비해 쓰는 새 공개키 암호다.

## 깊이 이해
- **배경·문제의식**: 장기 보관 데이터는 지금 수집되고 나중에 양자컴퓨터로 복호화되는 harvest now, decrypt later 위험이 있다.
- **작동 원리**: 격자, 해시, 코드 기반 등 양자 알고리즘에 알려진 취약성이 낮은 수학 문제를 기반으로 키교환·서명을 제공한다.
- **비유**: 도둑이 미래에 새 도구를 가질 것을 예상하고 지금부터 자물쇠 규격을 바꾸는 작업이다.
- **구체 예시**: NIST는 2024년 FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA를 최종 표준으로 승인했다.
- **흔한 오해·주의점**: PQC는 QKD와 다르다. PQC는 기존 디지털 시스템에 적용하는 소프트웨어·프로토콜 암호 전환이다.

## 연결 개념
- ML-KEM — NIST FIPS 203 키 캡슐화 표준
- ML-DSA — NIST FIPS 204 디지털서명 표준
- Crypto Agility — 암호 알고리즘 교체 가능 구조

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: PQC는 양자컴퓨터가 위협하는 RSA/ECC를 대체·병행하기 위한 고전 공개키 암호 표준과 전환 전략이다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Post-Quantum Cryptography는 양자 공격에 대비한 고전 컴퓨터용 공개키 암호 체계다.
> 2. **가치**: RSA/ECC 기반 키교환·서명·인증서 체계를 ML-KEM, ML-DSA 등 NIST 표준으로 전환한다.
> 3. **판단 포인트**: crypto inventory, hybrid TLS, 인증서·HSM·프로토콜 호환성, 장기 보관 데이터 위험을 함께 봐야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 양자 위협 이해 확인 | Shor, RSA/ECC 취약, Grover 영향 | 대칭키까지 동일 위험으로 표현 |
| 표준 인식 확인 | FIPS 203 ML-KEM, FIPS 204 ML-DSA, FIPS 205 SLH-DSA | Kyber/Dilithium 명칭만 쓰고 표준명 누락 |
| 전환 전략 판단 확인 | crypto agility, hybrid, inventory | 알고리즘 교체만 설명 |

> 요약: 이 문제는 PQC 알고리즘 암기가 아니라 암호 자산 전환과 운영 호환성 판단을 요구한다.

---

## Ⅰ. 개요 및 필요성

- 개요: 양자 대응 공개키 암호
- 배경: Shor 알고리즘은 충분한 오류정정 양자컴퓨터에서 RSA와 ECC 기반 공개키 암호를 위협한다.
- 필요성: 장기 보관 데이터와 인증 인프라는 양자컴퓨터 실현 전 crypto agility와 PQC 전환 계획이 필요하다.

---

## Ⅱ. 구조 및 구성요소

```text
Crypto Inventory -> Risk Classification -> PQC Algorithm Selection
      +-> Hybrid Deployment -> Certificate / HSM / Protocol Update
      +-> Monitoring / Rollback / Compliance
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Crypto Inventory | RSA/ECC 사용 위치 식별 | TLS, PKI, VPN, firmware |
| PQC Algorithm | 키캡슐화·서명 표준 제공 | ML-KEM, ML-DSA, SLH-DSA |
| Hybrid Mode | 기존+PQC 병행으로 전환 리스크 완화 | TLS hybrid draft 등 |
| Crypto Agility | 알고리즘 교체 가능한 구조 | policy, versioning |

> 요약: PQC 전환은 알고리즘 선택보다 암호 자산 식별, 표준 적용, 하이브리드 배포, 교체 가능 구조가 핵심이다.

---

## Ⅲ. 동작원리 및 흐름도

```text
암호 자산 식별 -> 데이터 수명·위험 평가 -> PQC 후보 선정
-> 시험 환경 검증 -> hybrid 배포 -> 운영 모니터링 -> 단계 전환
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | RSA/ECC 사용 시스템과 인증서를 식별함 | inventory coverage |
| 2 | 데이터 보존기간과 양자 위협 노출도를 평가함 | risk tier |
| 3 | ML-KEM/ML-DSA 등 표준 알고리즘을 시험함 | interoperability |
| 4 | hybrid 배포 후 성능·호환성·장애를 모니터링함 | handshake failure |

> 요약: PQC는 자산 식별에서 시작해 위험 기반 우선순위와 하이브리드 검증을 거쳐 단계 전환한다.

---

## Ⅳ. 특징

| 구분 | 기존 공개키 | PQC | 판단 기준 |
|:---|:---|:---|:---|
| 기반 문제 | 소인수분해·이산로그 | 격자·해시·코드 등 | 양자 공격 내성 |
| 대상 | RSA, ECDH, ECDSA | ML-KEM, ML-DSA, SLH-DSA | 용도별 매핑 |
| 전환 영향 | 키·서명 작음 | 키·서명 크기 증가 가능 | MTU, 인증서 크기 |
| 운영 | 장기 사용 | 알고리즘 교체 가능성 필요 | crypto agility |

> 요약: PQC는 보안 전환뿐 아니라 키·서명 크기와 프로토콜 호환성 영향을 함께 검증해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 키교환 | ECDH/RSA | ML-KEM | TLS/VPN 기밀성 |
| 서명 | ECDSA/RSA-PSS | ML-DSA/SLH-DSA | 인증서·펌웨어 서명 |
| 전환 | 일괄 교체 | hybrid+단계 전환 | 호환성·규제 일정 |

> 요약: PQC는 용도별로 KEM과 서명을 구분하고, 하이브리드 전환으로 호환성 리스크를 줄인다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 호환성 장애 | 인증서·패킷 크기 증가 | lab test, staged rollout | handshake failure rate |
| 미식별 자산 | 하드코딩·레거시 장비 | crypto discovery, SBOM | inventory gap |
| 알고리즘 변경 | 표준·취약점 변화 | crypto agility, policy update | algorithm replacement time |

> 요약: PQC 전환 리스크는 호환성, 미식별 자산, 알고리즘 변화이며 inventory와 crypto agility로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자산 식별 | RSA/ECC 사용 위치 추적 | scanner, CMDB |
| 전환 준비 | PQC 지원 라이브러리·HSM 확인 | compatibility test |
| 운영 영향 | handshake size·CPU·failure 추적 | APM, TLS log |

> 요약: PQC 준비도는 표준 알고리즘 채택 여부보다 자산 식별률과 운영 호환성으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. TLS, VPN, PKI, 코드서명, 펌웨어서명, 데이터 암호화에서 RSA/ECC 사용 위치를 crypto inventory로 작성함.
2. 장기 보관 데이터와 외부 공개 서비스부터 ML-KEM 기반 hybrid key exchange와 ML-DSA 시험을 수행함.
3. HSM, 인증서, 라이브러리, 프로토콜의 알고리즘 교체 정책을 정의하고 rollback 가능한 staged rollout을 적용함.

**결론 (2줄):**
- 기술사 판단: PQC 전환은 양자컴퓨터 완성 시점을 기다리는 작업이 아니라 장기 데이터 위험과 자산 교체 리드타임 기준으로 시작해야 함.
- 향후 방향: NIST FIPS 203/204/205 기반 표준 적용과 crypto agility가 기업 보안 아키텍처의 기본 요구가 됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PQC를 설명하시오" | 자산 식별·표준 선택·전환 흐름 | 기존 공개키와 차이 |
| 요구사항 명시형 | "PQC 전환 방안을 제시하시오" | inventory·hybrid·crypto agility | 호환성·미식별 자산 대응 |

> 요약: 설명형은 양자 위협과 표준을, 방안형은 전환 절차와 운영 리스크를 중심으로 작성한다.
