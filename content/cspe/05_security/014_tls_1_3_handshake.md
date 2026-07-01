---
title: "TLS 1.3 핸드셰이크 (TLS 1.3 Handshake)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 14
---

# 📖 【암기용】 개념 완전 이해

> 목적: TLS 1.3 핸드셰이크를 처음 봐도 TLS 1.2와 무엇이 달라졌는지 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: TLS 1.3 핸드셰이크는 1-RTT로 서버 인증과 키교환을 완료하고 초기부터 주요 메시지를 암호화하는 절차
- **왜 필요한가**: TLS 1.2는 RSA key transport, CBC, 복잡한 cipher suite, 2-RTT 지연 등 운영 위험과 지연 비용이 있었음
- **핵심 직관**: TLS 1.3은 오래된 선택지를 삭제하고, 안전한 재료(ECDHE, AEAD, HKDF)만 남겨 협상을 단순화한 방식임

## 깊이 이해
- **배경·문제의식**: TLS 1.2는 구현 선택지가 많아 약한 암호군 허용, 다운그레이드, 핸드셰이크 지연 문제가 반복됨. TLS 1.3은 RFC 8446에서 구버전 암호군을 제거하고 PFS를 기본화함
- **작동 원리**: ClientHello에 key_share를 포함해 첫 메시지부터 키교환 재료를 보냄. 서버는 ServerHello와 key_share로 shared secret을 만들고, Certificate 이후 Finished까지 transcript hash로 검증함
- **비유**: 예전에는 회의 전에 규칙을 여러 번 주고받았지만, TLS 1.3은 첫 봉투에 가능한 규칙과 임시 공개키를 같이 넣어 왕복 횟수를 줄임
- **구체 예시**: TLS 1.2 풀 핸드셰이크는 일반적으로 2-RTT, TLS 1.3 풀 핸드셰이크는 1-RTT, 재개 시 0-RTT Early Data를 사용할 수 있음
- **흔한 오해·주의점**: 0-RTT는 재전송 공격(Replay)에 노출될 수 있으므로 결제·상태변경 요청에는 적용하지 않아야 함

## 연결 개념
- TLS·SSL 프로토콜 - TLS 1.3이 개선한 상위 주제
- ECDHE - TLS 1.3 PFS 제공의 기본 키교환 방식
- PQC 하이브리드 키교환 - 양자 위협 대응을 위해 TLS key_share에 PQC KEM을 결합하는 흐름

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: TLS 1.3은 지연 감소만 쓰면 감점이며, 제거된 취약 기능, 키 스케줄, 0-RTT 리스크까지 함께 써야 함.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: TLS 1.3 Handshake는 ECDHE key_share, HKDF key schedule, AEAD Record 보호로 1-RTT 인증 키교환을 수행하는 절차임.
> 2. **가치**: RSA key transport, CBC, SHA-1, static DH를 제거하고 PFS와 초기 핸드셰이크 암호화를 기본 제공함.
> 3. **판단 포인트**: 1-RTT, 0-RTT, downgrade sentinel, transcript hash, OCSP Stapling, Early Data 재전송 통제가 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| TLS 1.2 대비 차이 확인 | 2-RTT에서 1-RTT, cipher suite 단순화, PFS 기본 | "TLS 1.3은 암호화만 더함" 식 답안 금지 |
| 핸드셰이크 원리 설명 | ClientHello key_share, ServerHello, Certificate, Finished | Record 계층과 Handshake 계층 혼동 금지 |
| 운영 리스크 판단 | 0-RTT replay, 구버전 호환, 인증서 검증 | 0-RTT를 모든 API에 적용한다는 답안 금지 |

> 요약: TLS 1.3 답안은 메시지 흐름, 제거 기능, 키 스케줄, 0-RTT 통제를 함께 제시해야 함.

---

## Ⅰ. 개요 및 필요성

TLS 1.3은 RFC 8446 기반 핸드셰이크임.
TLS 1.2의 왕복 지연과 취약 암호군 선택 문제를 줄이기 위해 1-RTT 기본, PFS 필수, AEAD 중심으로 프로토콜을 단순화함. 웹·API·모바일 서비스에서 handshake latency와 다운그레이드 위험을 동시에 낮추는 표준임.

---

## Ⅱ. 구조 및 구성요소

```text
ClientHello/key_share -> ServerHello/key_share -> EncryptedExtensions
-> Certificate -> CertificateVerify -> Finished -> Application Data
                         +-> PSK/0-RTT Early Data 선택
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| ClientHello | 버전, cipher suites, key_share, SNI, ALPN 제안 | SupportedVersions로 TLS 1.3 표시 |
| ServerHello | 선택 버전·암호군·key_share 반환 | shared secret 생성 시작 |
| EncryptedExtensions | ALPN 등 추가 협상 정보 전달 | ServerHello 이후 암호화 |
| Certificate/Verify | 서버 인증서와 개인키 소유 증명 | X.509 체인, transcript 서명 |
| Finished | 전체 핸드셰이크 무결성 검증 | HKDF 기반 finished_key 사용 |

> 요약: TLS 1.3 구조는 key_share로 공유비밀을 조기 생성하고, 이후 핸드셰이크 메시지를 암호화해 검증함.

---

## Ⅲ. 동작원리 및 흐름도

```text
ClientHello 전송 -> ServerHello 수신 -> ECDHE shared secret 생성
-> HKDF key schedule -> 인증서/서명 검증 -> Finished 검증
-> AEAD application traffic key 사용
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 클라이언트가 key_share 포함 ClientHello 전송 | X25519, secp256r1 등 허용 그룹 |
| 2 | 서버가 key_share 선택 후 shared secret 생성 | supported_versions TLS 1.3 |
| 3 | HKDF로 handshake/application traffic key 파생 | transcript hash 일치 |
| 4 | 인증서와 CertificateVerify 검증 | SAN, EKU, CA 체인, 서명 알고리즘 |
| 5 | Finished 후 애플리케이션 데이터 송수신 | AES-GCM 또는 ChaCha20-Poly1305 |

> 요약: TLS 1.3은 첫 왕복에서 키교환을 끝내고 HKDF로 용도별 키를 분리해 Record 보호에 사용함.

---

## Ⅳ. 특징

| 구분 | TLS 1.2 | TLS 1.3 | 수치·표준 판단 |
|:---|:---|:---|:---|
| 왕복 횟수 | 풀 핸드셰이크 2-RTT | 풀 핸드셰이크 1-RTT, 재개 0-RTT 가능 | RFC 8446 |
| 키교환 | RSA, DHE, ECDHE 선택 | (EC)DHE·PSK 중심, PFS 기본 | static RSA 제거 |
| 암호군 | 키교환+인증+암호+해시 결합 | AEAD+Hash 중심 단순화 | TLS_AES_128_GCM_SHA256 |
| 메시지 보호 | 많은 핸드셰이크 평문 | ServerHello 이후 주요 메시지 암호화 | 트래픽 분석 노출 감소 |

> 요약: TLS 1.3은 왕복 횟수와 취약 선택지를 줄이고, PFS와 AEAD를 기본 구조로 고정함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | TLS 1.3 Handshake | 선택 기준 |
|:---|:---|:---|:---|
| 호환성 | TLS 1.2 유지 | TLS 1.3 우선, TLS 1.2 fallback | 구형 단말 비율 1% 이상이면 병행 운영 |
| 지연 | 2-RTT 풀 핸드셰이크 | 1-RTT, 0-RTT 재개 | 모바일 p95 handshake 100ms 목표 |
| 위험 | 다양한 암호군 | 제한된 AEAD cipher suite | 규제·레거시 연동 시 cipher 허용표 관리 |

> 요약: TLS 1.3은 기본 선택지이나, 레거시 단말과 규제 연동 여부에 따라 TLS 1.2 병행 기간을 정함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 0-RTT Replay | Early Data 재전송 가능 | GET·읽기 요청만 허용, anti-replay cache | 0-RTT state-changing 요청 0건 |
| Fallback 오류 | 중간장비 TLS 1.3 미지원 | TLS 1.2 fallback, canary 배포 | handshake_failure 비율 0.1% 이하 |
| 인증서 검증 누락 | 클라이언트 구현 오류 | hostname·SAN·OCSP 검증 강제 | 검증 우회 테스트 0건 |

> 요약: TLS 1.3 운영 리스크는 0-RTT 재전송, 레거시 호환, 검증 누락이며 정책과 관측 지표로 통제함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 적용률 | TLS 1.3 연결 비율 80% 이상 | LB 로그, JA3/JA4, APM |
| 지연 | handshake p95 100ms 이하 | synthetic test, RUM |
| 안전 설정 | RSA key transport·CBC·TLS 1.0/1.1 0건 | sslyze, nmap, CI 보안 스캔 |

> 요약: TLS 1.3 전환 성과는 연결 비율, 핸드셰이크 지연, 취약 설정 제거율로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 - 단계별 또는 항목별):**
1. 전환 설정: 서버·LB에서 TLS 1.3 우선, TLS_AES_128_GCM_SHA256·TLS_CHACHA20_POLY1305_SHA256 허용, TLS 1.0/1.1 차단
2. 0-RTT 통제: Early Data는 GET·HEAD 등 멱등 요청에만 허용, 결제·로그인·권한변경 API는 1-RTT 강제
3. 운영 검증: canary 5%부터 적용, handshake_failure·p95 지연·TLS version 분포를 24시간 단위로 확인

**결론 (2줄):**
- 기술사 판단: 신규 공개 서비스는 TLS 1.3 우선 적용이 원칙이며, 레거시 단말 요구가 있으면 TLS 1.2를 제한된 기간 병행함
- 향후 방향: PQC 하이브리드 KEM, Encrypted ClientHello, 자동 인증서 갱신과 결합해 암호 민첩성을 확보해야 함

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "TLS 1.3 핸드셰이크를 설명하시오" | ClientHello부터 Finished까지 메시지 흐름 | TLS 1.2 대비 제거 기능과 1-RTT |
| 요구사항 명시형 | "TLS 1.3 전환 방안을 제시하시오", "0-RTT 위험을 설명하시오" | 전환·fallback·anti-replay 흐름 | 0-RTT 제한, 지표, 호환성 선택 기준 |

> 요약: 설명형은 메시지와 키 스케줄, 방안형은 전환 절차와 0-RTT 통제를 중심으로 작성함.
