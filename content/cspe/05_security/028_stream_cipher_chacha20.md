---
title: "스트림 암호 ChaCha20 (Stream Cipher ChaCha20)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-security"
weight: 28
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: ChaCha20은 **스트림 암호**의 하나로, 256비트 키·96비트 nonce·32비트 counter를 입력으로 64바이트 키스트림 블록을 생성하고 평문과 XOR하여 암호화하는 ARX(Add-Rotate-XOR) 기반 알고리즘임.
- **왜 필요한가**: AES-GCM은 AES-NI 하드웨어 가속이 있는 CPU에서 고속이지만, 모바일·임베디드·소프트웨어 전용 환경에서는 가속 없이도 constant-time으로 동작하는 ChaCha20-Poly1305가 TLS 1.3·QUIC·WireGuard에서 널리 채택됨.
- **핵심 직관**: 같은 비밀 키와 일회용 번호(nonce)로 긴 난수 테이프를 만들고, 평문에 겹쳐 암호문을 만드는 방식임. 테이프를 재사용하면(nonce 재사용) 두 평문의 관계가 노출됨.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| 스트림 암호 (상위 키워드) | 키스트림을 생성해 평문과 XOR하는 대칭키 암호 방식 | 난수 필름으로 문서 덮기 |
| ARX | Add(덧셈)·Rotate(비트 회전)·XOR 세 연산만 사용하는 구조 | 테이블 조회 없는 단순 연산 |
| 256비트 키 | 키스트림 생성의 비밀값 | 난수 필름의 비밀 씨앗 |
| 96비트 nonce | 메시지별 유일성을 보장하는 일회용 번호 | 주문번호 — 재사용 금지 |
| 32비트 counter | 64바이트 블록의 순번 | 페이지 번호 |
| Quarter Round | ChaCha20의 핵심 연산 단위 — 4개 워드에 ARX 적용 | 카드 한 벌 섞기 동작 |
| 20라운드 | quarter round을 20회 반복해 키스트림 블록 생성 | 카드를 20번 섞기 |
| Poly1305 | ChaCha20과 결합해 128비트 인증 태그를 생성하는 MAC | 봉인 도장 |
| AEAD | Authenticated Encryption with Associated Data — 기밀성+무결성+AAD 인증 | 암호화+봉인+추가 정보 인증 |
| Keystream | 키·nonce·counter로 생성된 의사 난수열 | 난수 필름 |
| Nonce 재사용 금지 | 같은 키에서 nonce를 반복하면 keystream이 동일해져 평문 XOR 관계 노출 | 같은 필름 두 번 쓰면 원문 비침 |

## 깊이 이해
- **배경·문제의식**: 이전 스트림 암호 RC4는 통계적 편향이 발견되어 TLS에서 금지됨(RFC 7465). ChaCha20은 Salsa20 계열의 개선판으로, 2008년 Daniel Bernstein이 설계함. ARX 구조라 테이블 조회(AES의 S-box)가 없어 캐시 타이밍 side-channel에 강함.
- **작동 원리**: (1) 512비트(16×32비트) 초기 상태를 구성함: 상수 128비트("expand 32-byte k") + 키 256비트 + counter 32비트 + nonce 96비트. (2) 이 상태에 20라운드의 quarter round(column round 4회 + diagonal round 4회 = 8 double-round)을 적용해 512비트(64바이트) 키스트림 블록을 생성함. (3) counter를 1씩 증가시키며 블록 단위로 키스트림을 생성하고, 평문과 XOR해 암호문을 만듦. (4) Poly1305가 1회용 키(ChaCha20 counter=0 블록에서 파생)로 AAD+암호문의 128비트 인증 태그를 생성함 — 이것이 ChaCha20-Poly1305 AEAD(RFC 8439)임.
- **비유**: 금고 비밀번호(키), 주문번호(nonce), 페이지 번호(counter)로 매 페이지마다 다른 난수 필름을 만들어 문서에 덧씌움. 주문번호를 재사용하면 같은 필름이 생겨 두 문서를 겹치면 원문이 비침.
- **구체 예시**: TLS 1.3에서 TLS_CHACHA20_POLY1305_SHA256 cipher suite가 지원됨. counter 32비트이므로 한 키·nonce 쌍으로 최대 약 256GiB(2^32 × 64B)를 처리할 수 있고, 이를 초과하면 rekey가 필요함. Google Chrome은 AES-NI 없는 모바일에서 ChaCha20-Poly1305를 우선 협상함.
- **흔한 오해·주의점**: (1) ChaCha20 단독은 기밀성만 제공함 — 무결성·인증은 Poly1305 태그를 결합한 AEAD로 사용해야 함. (2) nonce 96비트가 "충분히 크니 랜덤 생성해도 된다"고 생각하면 위험 — 2^48 메시지에서 50% 충돌 확률이므로 단조 증가(monotonic counter)를 권장함. (3) 블록 암호 모드(CBC, CTR)와 혼동하면 안 됨 — ChaCha20은 블록 암호가 아닌 스트림 암호임.

## 연결 개념
- **블록 암호 운영 모드 CBC·CTR·GCM(029)**: AES 기반 블록 암호 AEAD와 비교 대상
- **TLS 1.3(014)**: ChaCha20-Poly1305를 표준 cipher suite로 지원
- **대칭 암호화 AES(001)**: AES-GCM과 환경별 선택 기준 비교

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: ChaCha20은 256비트 키·96비트 nonce·32비트 counter로 64바이트 키스트림을 생성하는 ARX 기반 스트림 암호임.
> 2. **가치**: AES 가속기 없는 환경에서 테이블 조회 없는 constant-time 구현과 TLS 1.3·QUIC AEAD cipher suite 적용성을 제공함.
> 3. **판단 포인트**: nonce 1회성·counter overflow 방지·Poly1305 128비트 tag 검증 실패 시 평문 폐기가 운영 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 스트림 암호 구조 이해 | 키스트림 생성·XOR·nonce/counter | 블록 암호 모드(CBC, CTR)로 설명 |
| AEAD 적용 판단 | ChaCha20 기밀성 + Poly1305 무결성 | ChaCha20 단독으로 인증 제공 서술 |
| 운영 리스크 통제 | nonce 재사용 금지·counter 한계·tag 검증 | nonce를 IV처럼 재사용 가능 처리 |

> 요약: ChaCha20 답안은 키스트림 원리와 AEAD 인증, nonce 운영 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 256비트 키·96비트 nonce 기반 ARX 스트림 암호로, Poly1305와 결합해 AEAD를 제공함.
- 배경: RC4는 편향 문제로 금지(RFC 7465)되었고, AES 가속 없는 모바일·임베디드에서 constant-time 스트림 암호가 필요함.
- 필요성: ChaCha20-Poly1305는 TLS 1.3·QUIC·WireGuard에서 AEAD로 채택되어 기밀성·무결성을 제공함.

---

## Ⅱ. 구조 및 구성요소

```text
256-bit Key + 96-bit Nonce + 32-bit Counter
  -> ChaCha20 Block Function(20 rounds) -> 64B Keystream
Plaintext XOR Keystream -> Ciphertext
AAD + Ciphertext -> Poly1305 -> 128-bit Tag
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| 256비트 키 | 키스트림 생성의 비밀값 | 세션별 KDF(HKDF)로 파생 |
| 96비트 nonce | 메시지별 유일성 보장 | 같은 키에서 재사용 금지(단조 증가 권장) |
| 32비트 counter | 64바이트 블록 순번 | 최대 약 256GiB 처리 한계 |
| Poly1305 tag | AAD+암호문의 무결성·인증 검증 | 128비트, 실패 시 평문 폐기 |

> 요약: ChaCha20-Poly1305는 키스트림 XOR 기밀성과 128비트 인증 태그를 결합한 AEAD 구조임.

---

## Ⅲ. 동작원리 및 흐름도

```text
세션 키 파생(HKDF) -> 96비트 nonce 생성 -> counter=0 초기화
  -> 20라운드 block function -> Keystream XOR -> Ciphertext
  -> Poly1305 tag 생성(AAD 포함) -> 수신 측 tag 검증 -> 복호화/폐기
```

1. 키·nonce 준비: HKDF 등으로 256비트 세션 키를 파생하고, 메시지별 96비트 nonce를 단조 증가로 생성함 — 동일 키 내 nonce 중복 0건을 보장함.
2. 키스트림 생성: 512비트 초기 상태(상수+키+counter+nonce)에 20라운드 quarter round을 적용해 64바이트 키스트림 블록을 생성하고, counter를 1씩 증가시키며 반복함.
3. 암호화·태그: 평문과 키스트림을 XOR해 암호문을 생성하고, Poly1305가 AAD+암호문의 128비트 인증 태그를 산출함.
4. 복호화·검증: 수신 측이 태그를 먼저 검증하고, 검증 성공 시에만 복호화를 수행함 — 태그 실패 시 평문 반환을 금지함.

> 요약: 복호화 전 인증 태그를 검증하고 nonce 중복을 0건으로 유지하는 것이 운영 핵심임.

---

## Ⅳ. 특징

- Constant-time 구현: ARX(Add-Rotate-XOR) 구조라 테이블 조회(S-box)가 없어 캐시 타이밍 side-channel에 강함.
- AEAD 필수 결합: ChaCha20 단독은 기밀성만 제공하므로 반드시 Poly1305와 결합한 AEAD(RFC 8439)로 사용해야 함.
- Nonce 재사용 치명적: 같은 키에서 nonce를 재사용하면 keystream이 동일해져 두 평문의 XOR 관계가 노출됨 — 단조 증가 nonce가 권장됨.
- Counter 한계: 32비트 counter로 한 키·nonce 쌍에서 최대 약 256GiB를 처리할 수 있고, 초과 시 rekey가 필요함.
- 표준 채택: TLS 1.3(TLS_CHACHA20_POLY1305_SHA256)·QUIC·WireGuard에서 AEAD cipher suite로 채택됨.

---

## Ⅴ. 심화 비교 및 적용 판단

ChaCha20-Poly1305(스트림 AEAD)와 AES-GCM(블록 AEAD)을 구조·성능·운영 축으로 비교함.

| 구분 | AES-GCM | ChaCha20-Poly1305 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | 블록 암호(AES) + GCM 모드 | 스트림 암호(ARX) + Poly1305 MAC | 암호 프리미티브 유형 |
| HW 가속 | AES-NI 활용 시 고속 | 가속 불필요, SW constant-time | AES-NI 존재 여부 |
| 인증 태그 | GHASH 128비트 | Poly1305 128비트 | 둘 다 128비트 |
| Nonce 위험 | 재사용 시 tag 위조 가능(catastrophic) | 재사용 시 평문 관계 노출 | nonce 관리 역량 |

> 요약: AES-NI가 있는 서버는 AES-GCM을, 모바일·임베디드·SW 전용 환경은 ChaCha20-Poly1305를 선택함.

**리스크·대응:**
- Nonce 재사용: 난수 품질 부족·카운터 초기화 오류 → 세션별 키 파생·단조 증가 nonce (지표: 동일 키 nonce 중복 0건)
- 무결성 누락: ChaCha20 단독 사용 → Poly1305 AEAD 강제·tag 검증 실패 시 평문 반환 금지 (지표: tag 미검증 복호화 0건)
- Counter 초과: 대용량 메시지를 단일 키로 처리 → 메시지 분할·rekey 정책 (지표: 키당 처리량 256GiB 미만)

**도입 후 점검 지표:**
- 기밀성: 키 256비트·nonce 중복 0건 — 암호 로그·중복 탐지
- 무결성: Poly1305 tag 검증 100% — 실패 케이스 테스트
- 구현 검증: RFC 8439 test vector 100% 통과 — CI Known Answer Test

---

## Ⅵ. 실무 적용 및 결론

**적용 방안:**
1. AEAD 강제: ChaCha20 단독 사용을 금지하고 RFC 8439 ChaCha20-Poly1305를 TLS 1.3·QUIC 설정에 적용함.
2. Nonce 정책: 세션 키별 96비트 nonce 중복 0건을 보장하고, 프로세스 재시작 시 카운터 복구 또는 rekey 절차를 수립함.
3. 검증 자동화: RFC 8439 test vector·tag 실패 테스트·counter overflow 테스트를 CI에 포함함.

**결론:**
- 기술사 판단: AES-NI 서버는 AES-GCM을, 모바일·임베디드·SW 전용 환경은 ChaCha20-Poly1305를 선택함.
- 향후 방향: QUIC·VPN·메신저에서 AEAD 기본값으로 유지되며, nonce 관리 자동화와 키 수명 통제가 운영 핵심임.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "ChaCha20을 설명하시오" | 키·nonce·counter·키스트림·Poly1305 AEAD 흐름 | AES-GCM 대비 구조와 적용 환경 비교 |
| 요구사항 명시형 | "AEAD 적용 방안을 제시하시오" | tag 검증·nonce 중복 방지·rekey 절차 | 운영 리스크와 검증 지표 |

> 요약: 설명형은 ARX 암호 구조를, 방안형은 nonce·tag·counter 운영 통제를 중심으로 전개함.
