---
title: "ML-KEM (Module-Lattice Key Encapsulation Mechanism)"
date: "2026-07-02"
tags:
  - "cspe-latest-tech"
weight: 344
---

# 📖 【암기용】 개념 완전 이해

> 목적: ML-KEM을 NIST FIPS 203으로 표준화된 격자 기반 키 캡슐화 메커니즘으로 이해하게 만든다.

## 한눈에
- **개요**: 공개키로 공유 비밀을 캡슐화·복원하는 NIST PQC 키교환 표준
- **왜 필요한가**: RSA/ECDH 기반 키교환은 충분한 양자컴퓨터의 Shor 알고리즘에 취약해질 수 있다.
- **핵심 직관**: 양측이 공개 채널에서 같은 대칭키 재료를 만들되, 공격자는 격자 문제 때문에 공유 비밀을 알아내기 어렵게 하는 방식이다.

## 깊이 이해
- **배경·문제의식**: TLS, VPN, 메시징은 세션키를 만들기 위해 공개키 기반 키교환을 사용하므로 양자내성 KEM이 필요하다.
- **작동 원리**: 수신자가 keygen으로 공개키·개인키를 만들고, 송신자가 encaps로 ciphertext와 shared secret을 생성하며, 수신자가 decaps로 같은 shared secret을 복원한다.
- **비유**: 공개된 특수 상자에 비밀 재료를 넣어 잠그면, 개인 열쇠를 가진 사람만 같은 재료를 꺼낼 수 있는 구조다.
- **구체 예시**: FIPS 203은 ML-KEM-512, ML-KEM-768, ML-KEM-1024 세 parameter set을 정의한다.
- **흔한 오해·주의점**: ML-KEM은 암호문 자체로 데이터를 암호화하는 범용 대칭암호가 아니다. 공유 비밀을 만들고, 실제 데이터 보호는 AEAD 같은 대칭키 암호가 담당한다.

## 연결 개념
- FIPS 203 — ML-KEM 표준 문서
- PQC — ML-KEM이 속한 양자내성암호 전환
- TLS Hybrid — 기존 ECDHE와 ML-KEM을 병행하는 전환 방식

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식.
> 핵심: ML-KEM은 NIST FIPS 203의 Module-Lattice 기반 KEM으로, 공개키 채널에서 양자내성 공유 비밀을 생성한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ML-KEM은 Module-LWE 계열 난제에 기반한 키 캡슐화 메커니즘이다.
> 2. **가치**: TLS, VPN, 메시징의 키교환을 RSA/ECDH에서 양자내성 KEM으로 전환하는 표준 선택지다.
> 3. **판단 포인트**: parameter set, key/ciphertext 크기, decapsulation failure, hybrid 배포, HSM·라이브러리 지원을 확인해야 한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| NIST PQC 표준 이해 확인 | FIPS 203, ML-KEM-512/768/1024 | Kyber 명칭만 사용 |
| KEM 원리 확인 | keygen, encaps, decaps, shared secret | 데이터 암호화 알고리즘으로 설명 |
| 적용 판단 확인 | TLS hybrid, 인증서·HSM 호환성 | PQC 전환 절차 누락 |

> 요약: 이 문제는 ML-KEM을 서명이나 대칭암호가 아니라 키 설정용 KEM으로 구분하는 것이 핵심이다.

---

## Ⅰ. 개요 및 필요성

- 개요: NIST PQC KEM 표준
- 배경: RSA/ECDH 기반 키교환은 장기적으로 양자 알고리즘 위협을 받는다.
- 필요성: ML-KEM은 공개 채널에서 양자내성 공유 비밀을 생성해 TLS·VPN·메시징 전환에 사용된다.

---

## Ⅱ. 구조 및 구성요소

```text
Receiver KeyGen -> Public Key / Secret Key
Sender Encaps(Public Key) -> Ciphertext + Shared Secret
Receiver Decaps(Secret Key, Ciphertext) -> Shared Secret
      +-> KDF -> Symmetric Session Key
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| KeyGen | 공개키와 개인키 생성 | parameter set 선택 |
| Encaps | 공개키로 ciphertext와 shared secret 생성 | 송신자 수행 |
| Decaps | 개인키로 shared secret 복원 | 수신자 수행 |
| KDF/AEAD | 공유 비밀을 세션키와 데이터 암호화에 사용 | TLS key schedule |

> 요약: ML-KEM은 캡슐화·복원으로 공유 비밀을 만들고, 실제 데이터 암호화는 KDF 이후 대칭키 암호가 담당한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
parameter 선택 -> KeyGen -> public key 배포
-> Encaps로 ciphertext 생성 -> Decaps로 shared secret 복원 -> TLS key schedule 연결
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | ML-KEM-512/768/1024 중 보안 수준을 선택함 | security category |
| 2 | 수신자가 공개키·개인키를 생성함 | key validity |
| 3 | 송신자가 공개키로 ciphertext와 shared secret을 생성함 | encaps test vector |
| 4 | 수신자가 decaps 후 동일 shared secret을 얻음 | KAT, interop test |

> 요약: ML-KEM은 keygen·encaps·decaps 세 알고리즘과 parameter set 선택으로 운영된다.

---

## Ⅳ. 특징

| 구분 | ECDH | ML-KEM | 판단 기준 |
|:---|:---|:---|:---|
| 보안 기반 | 이산로그 | Module-LWE 계열 격자 문제 | 양자 위협 |
| 기능 | 키 합의 | 키 캡슐화 | 프로토콜 통합 방식 |
| 표준 | FIPS 186 등 ECC 생태계 | NIST FIPS 203 | PQC 전환 |
| 운영 영향 | 작은 키 | 더 큰 public key/ciphertext | MTU·handshake 크기 |

> 요약: ML-KEM은 ECDH 대체·병행 대상이지만 KEM 구조와 메시지 크기 증가를 프로토콜에서 검증해야 한다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 보안 수준 | ECDHE P-256 | ML-KEM-512/768/1024 | 정책·성능 균형 |
| 배포 | ECDHE 단독 | ECDHE+ML-KEM hybrid | 호환성 전환 |
| 용도 | 키교환 | shared secret encapsulation | TLS/VPN/메시징 |

> 요약: ML-KEM은 단독 교체보다 hybrid로 검증하고, 보안 수준과 handshake 크기를 함께 비교해야 한다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 호환성 실패 | 클라이언트·서버 라이브러리 미지원 | negotiation fallback, canary | handshake failure |
| 패킷 크기 증가 | public key·ciphertext 크기 | MTU test, fragmentation check | packet drop |
| 키 관리 미비 | 개인키 보호와 로테이션 미정 | HSM/KMS 지원 확인 | key access audit |

> 요약: ML-KEM 적용 리스크는 상호운용, 메시지 크기, 키 관리이며 실험 배포와 HSM 검증이 필요하다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 표준 적합 | FIPS 203 KAT 통과 | known-answer test |
| 성능 | handshake CPU·latency 추적 | load test |
| 전환 | hybrid 적용률과 실패율 추적 | TLS log |

> 요약: ML-KEM 도입 효과는 FIPS 적합성, handshake 영향, hybrid 전환 지표로 확인한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. 외부 공개 TLS, VPN, 메시징 시스템에서 ECDHE 사용 위치를 식별하고 ML-KEM hybrid 지원 라이브러리를 시험함.
2. ML-KEM-768을 기본 후보로 두고 보안 정책, CPU 사용량, handshake 크기, MTU 영향을 부하 시험으로 비교함.
3. HSM/KMS, 인증서 자동화, 모니터링이 ML-KEM 키와 협상 로그를 지원하는지 검증함.

**결론 (2줄):**
- 기술사 판단: ML-KEM은 키교환 영역의 PQC 핵심 표준이며, hybrid 배포로 호환성 리스크를 줄인 뒤 단계 전환해야 함.
- 향후 방향: ML-KEM은 TLS, VPN, 클라우드 KMS, 기기 인증 프로토콜에서 기본 KEM 후보로 확산됨.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ML-KEM을 설명하시오" | keygen·encaps·decaps 흐름 | ECDH와 차이 |
| 요구사항 명시형 | "PQC 키교환 전환 방안을 제시하시오" | hybrid TLS 검증 절차 | 호환성·크기·키관리 리스크 |

> 요약: 설명형은 KEM 원리를, 전환형은 hybrid 배포와 운영 영향을 중심으로 작성한다.
