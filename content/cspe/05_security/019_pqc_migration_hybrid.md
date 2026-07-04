---
title: "PQC 전환 로드맵·하이브리드 방식 (PQC Migration Hybrid)"
date: "2026-07-05"
author: "Claude Opus 4.6"
tags:
  - "cspe-security"
weight: 19
---

# 📖 【암기용】 개념 완전 이해

## 한눈에
- **개요**: PQC 전환 로드맵은 **양자내성 암호(PQC)** 표준(FIPS 203/204/205)으로 기존 RSA/ECC 암호자산을 단계적으로 교체하는 보안 프로그램이며, 하이브리드 방식은 전환 과도기에 기존 알고리즘과 PQC를 동시 사용하는 운영 전략임.
- **왜 필요한가**: RSA/ECC 키 교환·서명은 대규모 양자컴퓨터에 취약하고, HNDL(Harvest Now Decrypt Later) 공격은 현재 수집한 암호문을 미래 양자컴퓨터로 복호화할 수 있어, 보존 기간이 긴 데이터(의료·국방·개인정보)는 지금부터 전환을 준비해야 함.
- **핵심 직관**: 건물 전체 배선을 한 번에 뜯지 않고, 배선도(crypto inventory)를 먼저 만들어 위험 구역부터 임시 이중 배선(hybrid)을 깔고, 검증이 끝나면 구 배선을 제거하는 작업임.

## 핵심 용어 정리 (내부에 등장하는 것들)

| 용어/표기 | 의미 | 비유·예 |
|:---|:---|:---|
| PQC 전환 (상위 키워드) | RSA/ECC를 양자내성 알고리즘으로 교체하는 전체 프로그램 | 전 건물 배선 교체 프로젝트 |
| HNDL | 현재 암호문을 수집해 미래 양자컴퓨터로 복호화 | 편지를 모아뒀다 해독기 나오면 읽기 |
| Crypto Inventory | 시스템 내 모든 암호 알고리즘·키·인증서 사용처 목록 | 건물 배선도 |
| Hybrid TLS | 기존 키 합의(X25519)와 PQC KEM(ML-KEM-768)을 동시 수행 | 이중 배선 병행 운영 |
| Dual-sign | 기존 서명(ECDSA)과 PQC 서명(ML-DSA)을 동시 적용 | 두 종류 도장 병행 날인 |
| Crypto Agility | 설정·정책 변경만으로 알고리즘을 교체할 수 있는 아키텍처 역량 | 배선 규격을 커넥터 하나로 교환 |
| CNSA 2.0 | NSA의 상용 국가보안 알고리즘 스위트 2.0 전환 가이드 | 미국 정부 배선 규격 표준 |
| Risk Scoring | 데이터 보존 기간·외부 노출도·규제 등급으로 전환 우선순위 산정 | 위험 구역 표시 |
| KAT | Known Answer Test — FIPS 표준 적합성 검증 | 정답이 알려진 시험문제로 검증 |

## 깊이 이해
- **배경·문제의식**: 양자컴퓨터가 아직 범용 실용화 전이더라도 HNDL 공격은 현재부터 위험임. 보존 기간 10년 이상인 데이터는 2030년대 복호화 가능성까지 고려해야 하며, NIST는 2024년 FIPS 203/204/205를 확정해 전환 근거를 마련함. 015(PQC 개괄)에서 다룬 알고리즘 표준화가 완료된 뒤, '어떻게 전환할 것인가'가 이 키워드의 질문임.
- **작동 원리**: (1) crypto inventory로 RSA/ECDH/ECDSA 사용처(TLS·VPN·SSH·PKI·DB 암호화·코드서명)를 식별함. (2) 데이터 보호 기간·외부 노출도·규제 등급으로 risk scoring을 산정해 우선순위를 정함. (3) 외부 TLS는 X25519+ML-KEM-768 hybrid, 코드서명은 ECDSA+ML-DSA dual-sign으로 과도기 운영을 시작함. (4) canary 배포→성능/호환성 검증→단계 확대→단독 PQC 전환의 순서로 진행함. (5) crypto agility를 확보해 향후 알고리즘 변경 시 정책 flag만으로 교체함.
- **비유**: 낡은 다리를 폐쇄하기 전에 새 다리를 옆에 놓고 교통량을 나눠 보낸 뒤, 새 다리가 안전함이 확인되면 구 다리를 철거하는 것과 같음.
- **구체 예시**: 외부 TLS는 X25519+ML-KEM-768 hybrid로 canary 5%부터 시작하고, 코드서명은 ECDSA+ML-DSA dual-sign을 사용하며, 장기 보관 서명은 SLH-DSA(018) 적용성을 평가함. CNSA 2.0은 2030년까지 TLS 1.3 PQC 전환, 2035년까지 PKI 전환을 권고함.
- **흔한 오해·주의점**: PQC 전환은 라이브러리 업그레이드가 아님. 인증서 크기 증가(ML-DSA 공개키 1952B vs ECDSA 64B), MTU 초과, HSM 펌웨어 지원 여부, 감사 증적, 협력사 호환성을 포함한 생명주기 전환임. hybrid를 '이중 암호화'로 오해하면 안 됨 — 키 합의를 두 방식으로 동시 수행해 하나라도 안전하면 전체가 안전한 구조임.

## 연결 개념
- **ML-KEM(016)**: hybrid TLS의 PQC 키 합의 축
- **ML-DSA(017)·SLH-DSA(018)**: 인증서·코드서명 전환 시 PQC 서명 알고리즘
- **QKD(020)**: 물리 계층 키 분배 대안 — PQC와 적용 범위가 다름

---

# 📝 【답안용】 시험 답안 템플릿

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PQC 전환은 RSA/ECC 의존 암호자산을 FIPS 203/204/205와 hybrid 방식으로 단계 교체하는 보안 프로그램임.
> 2. **가치**: HNDL 위험·장기 서명 검증·규제 감사 요구를 crypto inventory와 crypto agility로 통제함.
> 3. **판단 포인트**: 자산 발견→위험 우선순위→hybrid 적용→검증→단독 전환의 5단계와 TLS·PKI·KMS·코드서명 영향 분석이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전환 전략 역량 확인 | crypto inventory, HNDL, risk scoring 우선순위 | 알고리즘 나열만 하고 로드맵 누락 |
| 하이브리드 설계 이해 | ECDHE+ML-KEM, ECDSA+ML-DSA dual-sign | hybrid를 이중 암호화로 단순화 |
| 운영 통제 판단 | crypto agility, KAT, rollback, 감사로그 | 서비스 영향·협력사 호환성 누락 |

> 요약: PQC 전환 답안은 알고리즘보다 자산 식별, 위험 우선순위, hybrid 운영, 검증 지표를 중심으로 작성해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: RSA/ECC 암호자산을 양자내성 표준으로 단계 전환하는 보안 프로그램임.
- 배경: RSA/ECC 키 교환·서명은 대규모 양자컴퓨터에 취약하고, HNDL 공격으로 장기 보관 데이터가 미래 복호화 위험에 노출됨.
- 필요성: NIST FIPS 203/204/205 확정과 CNSA 2.0 권고에 따라 crypto inventory·hybrid 프로토콜·crypto agility 기반 단계 전환이 필수임.

---

## Ⅱ. 구조 및 구성요소

```text
Crypto Inventory -> Risk Scoring -> Target Profile
  -> Hybrid TLS/PKI Pilot -> Interop Test -> Rollout
  / Crypto Agility -> Policy Update -> Audit Evidence
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Crypto Inventory | 알고리즘·키길이·인증서·라이브러리 사용처 식별 | TLS, VPN, SSH, PKI, DB 암호화, 코드서명 포함 |
| Risk Scoring | HNDL·데이터 보존기간·외부 노출도 기반 우선순위 산정 | 10년↑ 기밀 데이터 최우선 |
| Hybrid Profile | 기존 알고리즘+PQC 동시 운영 구성 | X25519+ML-KEM-768, ECDSA+ML-DSA |
| Crypto Agility | 정책 기반 알고리즘 enable/disable 자동화 | 90일 이내 교체 목표, rollback 지원 |

> 요약: PQC 전환 구조는 자산 식별→위험 평가→hybrid 적용→민첩한 교체→감사 증적의 순환으로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
자산 발견 -> RSA/ECC 의존도 평가 -> 보호기간 기반 Risk Scoring
  -> Hybrid Pilot(canary 5%) -> 성능·호환성 검증
  -> 단계 확대 -> 단독 PQC 전환 -> 지속 점검·감사
```

1. 자산 발견: TLS scan·SBOM·CMDB로 RSA/ECC 사용처를 자동·수동 조사, inventory coverage 95% 이상 확보함.
2. 위험 우선순위: HNDL 위험·외부 노출도·규제 등급으로 risk scoring을 산정하고 전환 대상 순서를 확정함.
3. Hybrid Pilot: 외부 TLS에 X25519+ML-KEM-768, 코드서명에 ECDSA+ML-DSA를 canary 5%부터 적용해 handshake 성공률 99.9% 이상·p95 지연 기준을 검증함.
4. 단독 전환·감사: FIPS KAT 100% 통과·rollback 30분 이내 절차를 확립한 뒤 hybrid에서 PQC 단독으로 전환하고, 변경 이력·정책 승인·감사 증적을 기록함.

> 요약: PQC 전환은 발견→우선순위→hybrid pilot→검증→단독 전환까지 반복 검증하며 장애율과 감사 증적을 함께 관리함.

---

## Ⅳ. 특징

- 단계적 위험 감소: 일괄 교체(Big-bang) 대비 canary→단계 확대→단독 전환으로 장애 격리와 rollback이 가능함.
- Hybrid 이중 보호: 기존 알고리즘과 PQC를 동시 수행해 하나라도 안전하면 전체가 안전한 구조를 제공함.
- Crypto Agility 필수: 알고리즘을 코드가 아닌 정책 flag로 교체해 향후 표준 변경에 90일 이내 대응함.
- 인증서·MTU 영향: ML-DSA 공개키 1952B·ML-KEM 캡슐 1088B로 패킷 크기가 증가해 TLS handshake 분할·MTU 조정이 필요함.
- 생태계 호환: 프록시·WAF·레거시 클라이언트·협력사 API의 PQC 지원 여부를 사전 검증해야 함.

---

## Ⅴ. 심화 비교 및 적용 판단

PQC hybrid 전환과 기존 RSA/ECC 유지를 전환 구조·비용·운영 축으로 비교함.

| 구분 | RSA/ECC 유지 | PQC Hybrid 전환 | 선택 기준 |
|:---|:---|:---|:---|
| 전환 방식 | 알고리즘 변경 없음 | 기존+PQC 병행 후 단독 전환 | HNDL 위험·데이터 보존 기간 |
| 비용·성능 | 변경 비용 없음 | 인증서 크기↑, handshake 지연↑ | MTU 1500 기준 p95 증가 20ms 이하 |
| 운영·위험 | 양자컴퓨터 출현 시 일괄 취약 | crypto agility로 90일 내 교체 | 감사 증적·rollback 30분 이내 |

> 요약: 외부 노출·장기 보관 데이터는 hybrid 우선, 내부 단기 데이터는 inventory와 agility 준비를 먼저 수행함.

**리스크·대응:**
- 누락 자산: shadow IT·내장 SDK에 숨은 RSA/ECC → SBOM·TLS scan·코드 검색으로 inventory coverage 95% 이상 확보 (지표: CMDB 대조 누락률)
- 상호운용 실패: 프록시·WAF·레거시 클라이언트의 PQC 미지원 → canary·allowlist·rollback으로 연결 실패율 0.1% 이하 유지 (지표: canary 실패율)
- 다운그레이드 공격: 공격자가 PQC 협상을 제거 → fail-close 정책·transcript binding으로 PQC 미협상 탐지 100% (지표: PQC 미협상 비율)

**도입 후 점검 지표:**
- 자산 식별: 알고리즘·키·인증서 coverage 95% 이상 — scanner·SBOM·CMDB 대조
- 서비스 영향: handshake p95 증가 20ms 이하 — APM·synthetic test 측정
- 감사·복구: 변경 승인·KAT 통과·rollback 30분 이내 — ITSM·CI 로그·DR drill

---

## Ⅵ. 실무 적용 및 결론

**적용 방안:**
1. 0~3개월: TLS scan·SBOM·HSM/KMS 조사로 crypto inventory coverage 95% 이상을 달성하고 HNDL 데이터 목록을 작성함.
2. 3~9개월: 외부 TLS에 X25519+ML-KEM-768, 코드서명에 ECDSA+ML-DSA dual-sign을 canary 5%부터 적용하고 p95 지연·MTU·호환성을 검증함.
3. 9~18개월: FIPS 203/204/205 KAT 통과·rollback 30분 이내 절차·알고리즘 policy flag 기반 crypto agility를 표준 운영에 반영함.

**결론:**
- 기술사 판단: PQC 전환은 알고리즘 교체가 아니라 inventory·hybrid·agility·감사 증적을 묶은 보안 프로그램으로 추진해야 함.
- 향후 방향: CNSA 2.0과 국내 KCMVP 규제에 맞춰 TLS·PKI·코드서명·KMS의 PQC 프로파일을 지속 갱신해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅱ·Ⅲ 강조 | Ⅴ·Ⅵ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PQC 전환을 설명하시오" | crypto inventory·hybrid 구조, 5단계 전환 흐름 | FIPS 표준·hybrid 특징·적용 사례 |
| 요구사항 명시형 | "로드맵을 제시하시오", "하이브리드 방식을 설계하시오" | 일정·pilot·rollback·감사 절차 | 위험 우선순위, MTU·지연·호환성 선택 기준 |

> 요약: 설명형은 전환 체계 전반을, 방안형은 단계 일정과 hybrid 운영 지표를 중심으로 구성함.
