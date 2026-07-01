---
title: "ML-KEM CRYSTALS-Kyber (ML-KEM CRYSTALS-Kyber)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 16
---

# 📖 【암기용】 개념 완전 이해

> 목적: ML-KEM CRYSTALS-Kyber를 처음 봐도 완전하게 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 양자컴퓨터 공격에 대비한 NIST FIPS 203 키 캡슐화 표준
- **왜 필요한가**: RSA와 ECC 기반 키 교환은 Shor 알고리즘이 실용화되면 개인키 노출 위험이 생긴다. ML-KEM은 공개 채널에서 32바이트 공유 비밀을 합의하는 PQC 전환의 기본 부품이다.
- **핵심 직관**: 공개키로 잠근 작은 비밀 상자를 보내고, 개인키 보유자만 같은 세션키를 꺼내는 방식이다.

## 깊이 이해
- **배경·문제의식**: 기존 TLS의 ECDHE는 현재 네트워크에는 실용적이나, "수집 후 복호화(Harvest Now, Decrypt Later)" 공격에는 장기 기밀성이 취약하다. 10년 이상 보호해야 하는 의료·국방·금융 데이터는 양자내성 키 교환이 필요하다.
- **작동 원리**: 수신자는 ML-KEM 키쌍을 만들고 공개키를 배포한다. 송신자는 공개키로 캡슐화하여 ciphertext와 shared secret을 만들고, 수신자는 개인키로 같은 shared secret을 복원한다. 내부 난제는 Module-LWE이다.
- **비유**: 누구나 넣을 수 있지만 주인만 열 수 있는 우편함과 같다. 우편함 입구가 공개키, 우편물 봉인이 ciphertext, 주인이 꺼낸 비밀번호가 shared secret이다.
- **구체 예시**: ML-KEM-768은 공개키 1184바이트, ciphertext 1088바이트, shared secret 32바이트이며 TLS 하이브리드에서 X25519와 함께 쓰인다.
- **흔한 오해·주의점**: ML-KEM은 암호문 본문을 직접 암호화하는 알고리즘이 아니다. 세션키 합의용 KEM이며 실제 데이터 보호는 AES-256-GCM, ChaCha20-Poly1305 같은 대칭키 AEAD가 수행한다.

## 연결 개념
- TLS 1.3 핸드셰이크 — ML-KEM shared secret을 HKDF 입력으로 결합
- PQC 전환 로드맵 — crypto inventory, hybrid TLS, crypto agility 필요
- ML-DSA — 키 교환이 아닌 전자서명 표준

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ML-KEM은 CRYSTALS-Kyber 기반의 NIST FIPS 203 양자내성 키 캡슐화 메커니즘임.
> 2. **가치**: TLS, VPN, 메시징에서 32바이트 shared secret을 생성하여 장기 기밀 데이터의 HNDL 위험을 낮춤.
> 3. **판단 포인트**: ML-KEM-768 기본 적용, hybrid TLS, KAT 검증, 개인키·seed 보호, 인증서·KMS 연계가 채점 포인트임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PQC 키 교환 이해 확인 | FIPS 203, Module-LWE, KeyGen/Encaps/Decaps | ML-KEM을 전자서명으로 설명 금지 |
| 표준·파라미터 판단 확인 | ML-KEM-512/768/1024, shared secret 32B | Kyber 명칭만 쓰고 FIPS 203 누락 금지 |
| 전환 운영 역량 확인 | hybrid TLS, crypto inventory, crypto agility | 단독 교체만 제시하고 상호운용성 누락 금지 |

> 요약: ML-KEM 답안은 표준명, KEM 3연산, 파라미터, TLS 하이브리드 전환을 연결해야 함.

---

## Ⅰ. 개요 및 필요성

ML-KEM은 격자 기반 KEM이다.
RSA/ECC 키 교환은 대규모 양자컴퓨터의 Shor 알고리즘에 취약하다.
ML-KEM은 NIST FIPS 203 표준으로, 공개 채널에서 공유 비밀을 합의하여 TLS·VPN·메시징의 장기 기밀성 요구를 충족함.

---

## Ⅱ. 구조 및 구성요소

```text
Parameter Set -> KeyGen -> Public Key 배포
Public Key -> Encaps -> Ciphertext / Shared Secret
Private Key + Ciphertext -> Decaps -> Shared Secret
/ HKDF -> AEAD Session Key -> TLS/VPN 보호
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| KeyGen | 공개키·개인키 생성 | seed와 난수 품질, FIPS 140-3 모듈 검증 |
| Encaps | 공개키로 ciphertext와 shared secret 생성 | ciphertext 크기 768/1088/1568B |
| Decaps | 개인키로 shared secret 복원 | decapsulation failure 처리와 side-channel 방어 |
| Parameter set | 보안강도·크기 선택 | ML-KEM-768이 일반 TLS 기본 후보 |

> 요약: ML-KEM은 KeyGen, Encaps, Decaps 3연산으로 shared secret을 만들고 HKDF로 세션키에 연결함.

---

## Ⅲ. 동작원리 및 흐름도

```text
수신자 KeyGen -> 공개키 전달 -> 송신자 Encaps
-> ciphertext 전송 -> 수신자 Decaps
-> shared secret 일치 확인 -> HKDF -> AEAD 통신
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | ML-KEM 키쌍 생성 | FIPS 203 KAT, DRBG seed 기록 |
| 2 | 공개키 전달·인증 | X.509, mTLS, pinning 정책 |
| 3 | 캡슐화·복호화 | shared secret 32B 일치, 실패율 0건 |
| 4 | 세션키 파생 | TLS HKDF transcript binding |
| 5 | 트래픽 보호 | AES-256-GCM 또는 ChaCha20-Poly1305 |

> 요약: ML-KEM은 공개키 인증 후 ciphertext를 교환하고, HKDF로 대칭키를 파생해 실제 트래픽을 보호함.

---

## Ⅳ. 특징

| 구분 | 기존 ECDHE | ML-KEM | 판단 포인트 |
|:---|:---|:---|:---|
| 공격 모델 | 고전 컴퓨터 대상 | 양자컴퓨터 포함 | HNDL 데이터 보호 기간 10년 이상 |
| 표준 | RFC 8446, NIST P-256/X25519 | NIST FIPS 203 | ML-KEM-512/768/1024 |
| 메시지 크기 | X25519 공개키 32B | ML-KEM-768 pk 1184B, ct 1088B | MTU, TLS ClientHello 크기 |
| 운영 방식 | 단독 ECDHE | ECDHE+ML-KEM hybrid | 다운그레이드 탐지와 interop 테스트 |

> 요약: ML-KEM은 메시지 크기를 키우지만 양자 공격 모델을 반영하므로 장기 기밀 데이터에 우선 적용함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | ECDHE 단독 | X25519+ML-KEM-768 hybrid | 인터넷 TLS 전환기 상호운용성 |
| 비용/성능 | 32B 키 교환 | 1KB급 pk/ct 추가 | ClientHello MTU, CPU decaps p95 |
| 운영/위험 | 암호 민첩성 낮음 | crypto agility 전제 | 알고리즘 교체 주기 90일 이내 |

> 요약: 초기 도입은 hybrid TLS로 시작하고, 내부 KMS·VPN은 ML-KEM-768 이상을 표준 프로파일로 고정함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 다운그레이드 | 중간자에 의한 고전 KEX 강제 | TLS transcript binding, policy fail-close | PQC 미협상 차단률 100% |
| 구현 취약점 | decapsulation timing 차이 | constant-time 구현, Wycheproof/KAT | timing variance 임계치 이하 |
| 패킷 단편화 | ClientHello 1KB 이상 증가 | MTU 테스트, record sizing | handshake failure 0.1% 이하 |

> 요약: ML-KEM 운영 리스크는 다운그레이드, side-channel, MTU이며 정책·구현·네트워크 시험으로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 표준 적합성 | FIPS 203 KAT 100% 통과 | ACVP, 벡터 테스트 |
| 세션 수립 | TLS handshake p95 증가 20ms 이하 | APM, synthetic probe |
| 키 관리 | 개인키 HSM/KMS 보관, 접근 RBAC | 감사로그, key rotation 리포트 |

> 요약: ML-KEM 성공 여부는 FIPS 검증, handshake 지연, 키 접근 감사로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. crypto inventory로 TLS, VPN, SSH, 메시징의 RSA/ECDH 사용처를 식별하고 외부 노출 TLS부터 X25519+ML-KEM-768 hybrid 적용.
2. FIPS 203 KAT·ACVP 검증, constant-time decapsulation, HSM/KMS 기반 개인키 접근 RBAC와 감사로그 수집.
3. MTU 1500 환경, 프록시, WAF, CDN 구간에서 ClientHello 크기와 handshake p95 증가 20ms 이하 조건을 회귀 테스트.

**결론 (2줄):**
- 기술사 판단: 장기 기밀성 10년 이상 데이터는 hybrid ML-KEM-768을 우선 적용하고, 폐쇄망·고보안 구간은 ML-KEM-1024를 검토함.
- 향후 방향: CNSA 2.0과 NIST FIPS 203 기반으로 crypto agility와 자동 알고리즘 교체 절차를 표준 운영으로 전환해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ML-KEM을 설명하시오" | KeyGen/Encaps/Decaps와 FIPS 203 파라미터 | ECDHE 대비 양자내성·메시지 크기 |
| 요구사항 명시형 | "TLS 전환 방안을 제시하시오", "PQC와 비교하시오" | hybrid TLS 협상, HKDF 결합, 다운그레이드 차단 | MTU·지연·키관리·상호운용성 선택 기준 |

> 요약: 설명형은 KEM 원리, 방안형은 hybrid TLS 전환과 운영 검증 지표를 중심으로 전개함.
