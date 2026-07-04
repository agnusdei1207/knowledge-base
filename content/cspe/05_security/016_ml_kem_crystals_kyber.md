---
title: "ML-KEM 양자내성 키 캡슐화 (ML-KEM CRYSTALS-Kyber)"
date: "2026-07-04"
tags:
  - "cspe-security"
weight: 16
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: **ML-KEM은 격자 난제(Module-LWE)에 기반한 NIST FIPS 203 키 캡슐화 표준(KEM)으로, 공개 채널에서 32바이트 공유키를 합의하는 양자내성 키교환 부품임**. 양자위협·PQC 전반은 (015 참조).
- **왜 필요한가**: 기존 TLS 키교환인 ECDH(006·007)는 Shor 알고리즘으로 무력화되는데, ML-KEM은 양자컴퓨터도 못 푸는 격자 난제로 같은 역할(세션키 합의)을 대체하기 때문임.
- **핵심 직관**: 누구나 넣을 수 있지만 개인키 주인만 열 수 있는 "공개 우편함"에 비밀 상자를 넣어 보내고, 양쪽이 같은 세션키를 얻는 방식임 — ECDH의 "양쪽 지수 곱" 대신 "격자 위 잡음 낀 계산"을 씀.

## 핵심 용어 정리 (내부에 등장하는 것들)

답안(Ⅰ~Ⅵ·표)에 나오는 표기·연산·계산식을 비유와 함께 먼저 풀어 둠. 상위 핵심 키워드는 **KEM(Key Encapsulation Mechanism, 키 캡슐화)** 으로, 암호문 하나를 주고받아 양쪽이 동일한 공유키를 얻는 방식임.

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| KEM | 공개키로 공유키를 "캡슐화"해 합의하는 메커니즘 | 공개 우편함에 비밀 상자 투입 |
| Module-LWE | 잡음 낀 선형식 복원의 어려움에 기반한 격자 난제 | 오차 낀 방정식 되풀기 |
| KeyGen | 공개키·개인키 쌍 생성 연산 | 우편함과 열쇠 제작 |
| Encaps | 공개키로 ciphertext + shared secret 생성 | 상자를 넣고 사본 비밀 보관 |
| Decaps | 개인키로 ciphertext에서 shared secret 복원 | 주인이 상자 열어 같은 비밀 획득 |
| ciphertext(ct) | 캡슐화 결과로 전송되는 암호문 | 봉인된 비밀 상자 |
| shared secret | 양쪽이 얻는 32바이트 공유키 | 상자 속 최종 비밀번호 |
| ML-KEM-512/768/1024 | 보안강도별 파라미터(범주 1/3/5) | 자물쇠 등급 하/중/상 |
| FO 변환 | 복호 실패를 역이용한 공격을 막는 변환(IND-CCA2 달성) | 가짜 상자 넣어도 안 새게 봉인 강화 |
| HKDF | shared secret을 세션키로 파생하는 키유도함수 | 원재료를 실제 열쇠로 가공 |
| AEAD | 인증·암호를 동시 제공하는 대칭 암호(AES-GCM 등) | 실제 데이터 자물쇠 |
| 하이브리드 | X25519와 ML-KEM 공유키를 함께 결합(X25519MLKEM768) | 이중 자물쇠 병용 |

## 깊이 이해
- **배경·문제의식**: 인터넷 세션키는 대부분 ECDHE로 합의하는데, 공격자가 지금 암호문을 저장해 두고 미래 양자컴퓨터로 복호하는 HNDL(015) 때문에 장기 기밀 데이터는 지금부터 양자내성 키교환이 필요함. ML-KEM은 원래 공모명 CRYSTALS-Kyber였고 2024년 8월 FIPS 203으로 확정됨.
- **작동 원리(어떻게+왜)**: 수신자가 KeyGen으로 키쌍을 만들어 공개키를 배포하면, 송신자는 Encaps로 ciphertext와 shared secret을 만들어 ct만 전송하고, 수신자는 Decaps로 개인키를 써서 같은 shared secret을 복원함. 안전성은 Module-LWE의 어려움에서 나오며, 복호 실패를 악용한 공격을 막기 위해 FO(Fujisaki-Okamoto) 변환으로 IND-CCA2를 달성함 — 그래서 정적 키에도 안전함.
- **비유**: 공개키는 아무나 편지를 넣을 수 있는 우편함, ciphertext는 봉인된 비밀 상자, 개인키는 우편함 주인의 열쇠임. 상자를 넣은 사람과 꺼낸 주인만 같은 비밀번호(shared secret)를 가짐.
- **구체 예시**: ML-KEM-768은 공개키 1184B, ciphertext 1088B, shared secret 32B로, 최신 브라우저·서버가 TLS에서 X25519와 묶은 하이브리드 X25519MLKEM768로 이미 씀. ECDH의 32B 공개키에 비하면 약 1KB가 커져 ClientHello 크기·MTU를 검토해야 함.
- **흔한 오해·주의점**: (1) ML-KEM은 데이터 본문을 직접 암호화하지 않음 — 세션키 합의용 KEM이고 실제 보호는 AES-256-GCM·ChaCha20-Poly1305가 함. (2) 서명 기능은 없음(그건 ML-DSA 017). (3) "Kyber"만 쓰고 FIPS 203을 빠뜨리면 표준 인지 부족으로 보임.

## 연결 개념
- ECDH 키교환 — ML-KEM이 대체하는 기존 키합의 방식 (006·007 참조)
- TLS 1.3 핸드셰이크 — ML-KEM shared secret을 HKDF 입력으로 결합 (014 참조)
- ML-DSA — 키교환이 아닌 서명을 담당하는 격자 표준 (017 참조)

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ML-KEM은 CRYSTALS-Kyber 기반 NIST FIPS 203 격자(Module-LWE) 키 캡슐화 표준으로, 32바이트 공유키를 합의함.
> 2. **가치**: Shor에 취약한 ECDH를 대체해 TLS·VPN·메시징의 세션키 합의를 양자내성으로 바꾸고 HNDL 위험을 낮춤.
> 3. **판단 포인트**: 전환기엔 X25519+ML-KEM-768 하이브리드로 시작하고, FIPS 203 KAT·상수시간 구현·MTU를 함께 검증함이 관건임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| PQC 키교환 이해 확인 | FIPS 203·Module-LWE·KeyGen/Encaps/Decaps | ML-KEM을 전자서명으로 서술 |
| 표준·파라미터 판단 | ML-KEM-512/768/1024·shared secret 32B | Kyber만 쓰고 FIPS 203 표준번호 누락 |
| 전환 운영 역량 | 하이브리드·상수시간·crypto agility | 단독 전면 교체만 제시·상호운용성 누락 |

> 요약: ML-KEM 답안은 표준번호(FIPS 203)·KEM 3연산·파라미터·하이브리드 전환을 함께 정확히 써야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 격자 난제로 공유키를 합의하는 양자내성 KEM임.
- 배경: ECDH 키교환은 Shor 알고리즘에 무력화되며, 장기 데이터는 HNDL로 현재부터 미래 복호 위험이 있음(015).
- 필요성: NIST FIPS 203 표준으로 공개 채널에서 32B 공유키를 만들어 TLS·VPN·메시징의 PQC 키합의를 제공함.
- 전제: 양자위협·PQC 개괄은 (015 참조)로 위임하고 Module-LWE 기반 키캡슐화에 집중함.

---

## Ⅱ. 구조 및 구성요소

```text
Parameter Set(512/768/1024) -> KeyGen -> 공개키 배포 / 개인키 보관
공개키 -> Encaps -> ciphertext + shared secret
개인키 + ciphertext -> Decaps -> 동일 shared secret
  -> HKDF -> AEAD 세션키 -> TLS/VPN 트래픽 보호
  / 전환기: X25519 공유키 + ML-KEM 공유키 -> 하이브리드 결합
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| KeyGen | 공개키·개인키 생성 | DRBG seed 품질, FIPS 140-3 모듈 |
| Encaps | 공개키로 ct·shared secret 생성 | ct 768/1088/1568B |
| Decaps | 개인키로 shared secret 복원 | FO 변환으로 복호실패 악용 차단 |
| Parameter set | 보안강도(범주 1/3/5) 선택 | ML-KEM-768이 일반 TLS 기본 후보 |
| 하이브리드 결합 | 기존+PQC 공유키 병용 | X25519MLKEM768, 다운그레이드 방지 |

> 요약: ML-KEM은 KeyGen·Encaps·Decaps 3연산으로 shared secret을 만들고 HKDF로 세션키에 연결하며, 전환기엔 하이브리드로 병용함.

---

## Ⅲ. 동작원리 및 흐름도

```text
수신자 KeyGen -> 공개키 전달(인증) -> 송신자 Encaps
  -> ciphertext 전송 -> 수신자 Decaps -> shared secret 일치
  -> HKDF 파생 -> AEAD 통신
```

1. 수신자가 ML-KEM 키쌍을 생성하고 공개키를 X.509 등으로 인증해 배포함.
2. 송신자가 그 공개키로 Encaps를 수행해 ciphertext와 자신 쪽 shared secret을 얻고 ct만 전송함.
3. 수신자가 개인키로 Decaps를 수행해 동일한 shared secret을 복원하며, FO 변환이 복호실패 악용을 차단함.
4. 양쪽이 shared secret을 HKDF에 넣어 AES-256-GCM 세션키를 파생하고 실제 트래픽을 보호함.

> 요약: 공개키 인증 후 ciphertext 하나만 교환해 양쪽이 같은 shared secret을 얻고, HKDF로 대칭키를 파생해 트래픽을 보호함.

---

## Ⅳ. 특징

- 난제 전환: 이산로그가 아닌 격자 Module-LWE에 안전성을 둬 Shor 알고리즘에 견딤.
- KEM 전용: 세션키 합의만 담당하며 본문 암호화·서명은 하지 않음(대칭 AEAD·ML-DSA와 역할 분리).
- CCA 안전: FO 변환으로 IND-CCA2를 달성해 정적 공개키 재사용 환경에서도 안전함.
- 크기 증가: 공개키·ct가 약 1KB급이라 ECDH 대비 ClientHello·MTU 부담이 있음.
- 하이브리드 우선: 전환기엔 X25519MLKEM768로 병용해 신규 알고리즘 결함 위험을 분산함.
- 표준 확립: 2024년 FIPS 203 확정으로 KAT·ACVP 기반 적합성 검증 근거가 있음.

---

## Ⅴ. 심화 비교 및 적용 판단

기존 키교환 ECDH(X25519)와 ML-KEM을 안전근거·양자내성·크기 축으로 비교함(다대상×다축이므로 표 사용).

| 구분 | ECDH(X25519) | ML-KEM-768 |
|:---|:---|:---|
| 안전 근거 | 타원곡선 이산로그 | 격자 Module-LWE |
| 양자내성 | Shor로 파훼 | 현재까지 양자내성 |
| 공개키/ct 크기 | 32B / 32B | 1184B / 1088B |
| 합의 방식 | 양쪽 스칼라곱(대화형) | 캡슐화 1왕복(KEM) |
| 성숙도 | 수년간 검증 | 2024 표준화, 상대적 신생 |

> 요약: ML-KEM은 크기가 커지지만 양자내성을 확보하므로 장기 기밀 데이터에 우선 적용하고, 신생 우려는 하이브리드로 흡수함.

리스크는 불릿으로 정리함.
- 리스크: 다운그레이드 — 원인: 중간자가 고전 KEX 강제 — 대응: TLS transcript binding·fail-close, PQC 미협상 차단률 100%.
- 리스크: 사이드채널 — 원인: Decaps 타이밍·전력 편차 — 대응: 상수시간 구현·Wycheproof/KAT, timing variance 임계 이하.
- 리스크: 단편화 — 원인: ClientHello 1KB↑ 증가 — 대응: MTU·record sizing 시험, handshake 실패 0.1% 이하.

지표는 불릿으로 정리함.
- 지표: 표준 적합성 — 목표: FIPS 203 KAT 100% 통과 — 측정: ACVP·테스트 벡터.
- 지표: 세션 수립 — 목표: handshake p95 증가 20ms 이하 — 측정: APM·synthetic probe.
- 지표: 키 관리 — 목표: 개인키 HSM/KMS 보관·RBAC — 측정: 감사로그·rotation 리포트.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. crypto inventory로 TLS·VPN·SSH·메시징의 RSA/ECDH 사용처를 식별하고, 외부 노출 TLS부터 X25519+ML-KEM-768 하이브리드 적용.
2. FIPS 203 KAT·ACVP 검증, 상수시간 Decaps, HSM/KMS 기반 개인키 접근 RBAC와 감사로그 수집.
3. MTU 1500·프록시·WAF·CDN 구간에서 ClientHello 크기와 handshake p95 증가 20ms 이하를 회귀 테스트.

**결론 (2줄):**
- 기술사 판단: 장기 기밀성 10년↑ 데이터는 하이브리드 ML-KEM-768을 우선 적용하고, 폐쇄망·고보안 구간은 ML-KEM-1024를 검토함.
- 향후 방향: CNSA 2.0·FIPS 203 기준으로 하이브리드에서 순수 PQC로의 이행과 알고리즘 자동 교체(crypto agility)를 표준 운영화함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ML-KEM을 설명하시오" | KeyGen/Encaps/Decaps·FIPS 203 파라미터 | ECDH 대비 양자내성·크기 |
| 요구사항 명시형 | "TLS PQC 전환 방안 제시" | 하이브리드 협상·HKDF 결합·다운그레이드 차단 | MTU·지연·키관리·상호운용성 |

> 요약: 설명형은 KEM 3연산 원리, 방안형은 하이브리드 TLS 전환과 운영 검증 지표를 중심으로 전개함.
