---
title: "PQC 전환 로드맵·하이브리드 방식 (PQC Migration Hybrid)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 19
---

# 📖 【암기용】 개념 완전 이해

> 목적: PQC 전환 로드맵·하이브리드 방식을 처음 봐도 완전하게 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 설명이다.

## 한눈에
- **개요**: 기존 RSA/ECC 암호를 NIST PQC 표준으로 단계 전환하는 실행 체계
- **왜 필요한가**: 암호 알고리즘은 애플리케이션, 인증서, HSM, 프로토콜, 협력사 API에 숨어 있다. 한 번에 교체하면 장애가 커지므로 inventory, 위험 우선순위, hybrid TLS, crypto agility가 필요하다.
- **핵심 직관**: 건물 전체 배선을 한 번에 뜯지 않고, 배선도를 먼저 만들고 위험 구역부터 임시 이중 배선 후 표준 배선으로 바꾸는 작업이다.

## 깊이 이해
- **배경·문제의식**: 양자컴퓨터가 아직 모든 환경에 실용화되지 않았더라도 HNDL 공격은 현재부터 위험이다. 보존 기간이 긴 개인정보·의료·국방 데이터는 2030년 이후 복호화 가능성까지 고려해야 한다.
- **작동 원리**: 먼저 RSA/ECDH/ECDSA 사용처를 crypto inventory로 찾는다. 데이터 보호 기간과 외부 노출도를 기준으로 우선순위를 정하고, TLS는 X25519+ML-KEM-768 같은 hybrid 방식으로 운영한다. 이후 인증서·KMS·코드서명·VPN을 FIPS 203/204/205 기반으로 전환한다.
- **비유**: 낡은 다리를 폐쇄하기 전에 새 다리를 옆에 놓고 교통량을 나눠 보낸 뒤, 검증이 끝나면 구 다리를 철거하는 방식이다.
- **구체 예시**: 외부 TLS는 X25519+ML-KEM-768 hybrid로 시작하고, 코드서명은 ECDSA+ML-DSA dual-sign을 사용하며, 장기 보관 서명은 SLH-DSA 적용성을 평가한다.
- **흔한 오해·주의점**: PQC 전환은 라이브러리 업그레이드가 아니다. 인증서 크기, MTU, HSM 지원, 감사 증적, 협력사 호환성을 포함한 생명주기 전환이다.

## 연결 개념
- ML-KEM — hybrid TLS의 PQC 키 합의 축
- ML-DSA·SLH-DSA — 인증서·코드서명 전환 축
- crypto agility — 알고리즘 교체를 설정·정책으로 수행하는 역량

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: PQC 전환은 RSA/ECC 의존 암호자산을 FIPS 203/204/205와 hybrid 방식으로 단계 교체하는 프로그램임.
> 2. **가치**: HNDL 위험, 장기 서명 검증, 규제 감사 요구를 crypto inventory와 crypto agility로 통제함.
> 3. **판단 포인트**: 발견, 우선순위, hybrid 적용, 검증, 단독 전환의 5단계와 TLS·PKI·KMS·코드서명 영향 분석이 핵심임.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 전환 전략 역량 확인 | crypto inventory, HNDL, 우선순위 | PQC 알고리즘 나열만 하고 로드맵 누락 금지 |
| 하이브리드 설계 이해 | ECDHE+ML-KEM, ECDSA+ML-DSA | hybrid를 이중 암호화로 단순화 금지 |
| 운영 통제 판단 | crypto agility, KAT, rollback, 감사로그 | 서비스 영향·협력사 호환성 누락 금지 |

> 요약: PQC 전환 답안은 알고리즘보다 자산 식별, 위험 우선순위, hybrid 운영, 검증 지표를 중심으로 작성해야 함.

---

## Ⅰ. 개요 및 필요성

- 개요: 양자내성 암호 전환 프로그램
- 배경: RSA/ECC 기반 키 교환·서명은 대규모 양자컴퓨터에 취약하고, 장기 보관 데이터는 HNDL 위험을 가짐.
- 필요성: NIST FIPS 203/204/205, CNSA 2.0, 하이브리드 프로토콜, crypto agility 기준으로 자산 식별·우선순위·단계 전환을 수행함.

---

## Ⅱ. 구조 및 구성요소

```text
Crypto Inventory -> Risk Scoring -> Target Profile
-> Hybrid TLS/PKI Pilot -> Interop Test -> Rollout
/ Crypto Agility -> Policy Update -> Audit Evidence
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Crypto inventory | 알고리즘·키길이·인증서·라이브러리 식별 | TLS, VPN, SSH, PKI, DB 암호화 포함 |
| Risk scoring | HNDL, 데이터 보존 기간, 외부 노출도 평가 | 10년 이상 기밀 데이터 우선 |
| Hybrid profile | 기존+PQC 동시 사용 | X25519+ML-KEM-768, ECDSA+ML-DSA |
| Crypto agility | 알고리즘 교체 자동화 | 정책 기반 enable/disable, rollback |

> 요약: PQC 전환 구조는 자산 식별, 위험 평가, hybrid 적용, 민첩한 교체, 감사 증적으로 구성됨.

---

## Ⅲ. 동작원리 및 흐름도

```text
자산 발견 -> RSA/ECC 의존도 평가 -> 보호기간 산정
-> hybrid pilot -> 성능·호환성 검증
-> 단계 배포 -> 단독 PQC 전환 -> 지속 점검
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | 암호자산 자동·수동 조사 | inventory coverage 95% 이상 |
| 2 | 위험 우선순위 산정 | HNDL, 외부 노출, 규제 등급 |
| 3 | hybrid 프로토콜 적용 | TLS handshake 성공률 99.9% 이상 |
| 4 | 운영 검증·롤백 | p95 지연, MTU, 장애율 기준 |
| 5 | 표준화·감사 | FIPS KAT, 변경 이력, 정책 승인 |

> 요약: PQC 전환은 발견에서 단독 전환까지 반복 검증하며 장애율과 감사 증적을 함께 관리함.

---

## Ⅳ. 특징

| 구분 | Big-bang 교체 | Hybrid migration | 판단 포인트 |
|:---|:---|:---|:---|
| 전환 방식 | 일괄 알고리즘 변경 | 기존+PQC 병행 | 상호운용성·장애 격리 |
| 적용 범위 | 일부 라이브러리 중심 | TLS, PKI, KMS, 코드서명 | 전체 crypto inventory |
| 위험 통제 | 장애 발생 후 대응 | canary, rollback, policy flag | p95 지연·실패율 기준 |
| 감사 대응 | 변경 사유 추적 부족 | 승인·KAT·로그 증적 | FIPS 203/204/205 매핑 |

> 요약: Hybrid migration은 전환 위험을 낮추기 위해 기존 암호와 PQC를 병행하고 검증 지표 충족 후 단독 전환함.

---

## Ⅴ. 심화 비교 및 적용 판단

| 구분 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 구조 | RSA/ECC 단독 | ECDHE+ML-KEM, ECDSA+ML-DSA | 외부 노출·장기 기밀성 |
| 비용/성능 | 작은 메시지 | KB급 키·서명 증가 | MTU 1500, handshake p95 |
| 운영/위험 | 암호 하드코딩 | crypto agility | 90일 내 알고리즘 교체 |

> 요약: 외부 TLS와 장기 보관 데이터는 hybrid 우선, 내부 단기 데이터는 inventory와 정책 준비를 먼저 수행함.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| 누락 자산 | shadow IT, 내장 SDK | SBOM, TLS scan, 코드 검색 | inventory coverage 95% 이상 |
| 상호운용 실패 | 프록시·WAF·레거시 클라이언트 | canary, allowlist, rollback | 연결 실패율 0.1% 이하 |
| 다운그레이드 | PQC 협상 제거 | fail-close, transcript binding | PQC 미협상 탐지 100% |

> 요약: 전환 실패는 누락 자산과 호환성에서 발생하므로 inventory와 canary 지표를 선행 관리함.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자산 식별 | 알고리즘·키·인증서 coverage 95% 이상 | scanner, SBOM, CMDB 대조 |
| 서비스 영향 | handshake p95 증가 20ms 이하 | APM, synthetic test |
| 감사·복구 | 변경 승인, KAT, rollback 30분 이내 | ITSM, CI 로그, DR drill |

> 요약: PQC 전환 성공 여부는 자산 식별률, 서비스 지연, 감사·복구 증적으로 판단함.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개 (필수 — 단계별 또는 항목별):**
1. 0~3개월: TLS scan, SBOM, HSM/KMS 조사로 crypto inventory coverage 95% 이상 달성하고 HNDL 데이터 목록화.
2. 3~9개월: 외부 TLS에 X25519+ML-KEM-768, 코드서명에 ECDSA+ML-DSA dual-sign을 canary 5%부터 적용.
3. 9~18개월: FIPS 203/204/205 KAT, rollback 30분 이내 절차, 알고리즘 policy flag 기반 crypto agility를 표준 운영에 반영.

**결론 (2줄):**
- 기술사 판단: PQC 전환은 알고리즘 교체가 아니라 inventory, hybrid, agility, 감사 증적을 묶은 보안 프로그램으로 추진해야 함.
- 향후 방향: CNSA 2.0과 국내 규제 요구에 맞춰 TLS·PKI·코드서명·KMS의 PQC 프로파일을 지속 갱신해야 함.

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "PQC 전환을 설명하시오" | discovery부터 rollout까지 단계 흐름 | FIPS 203/204/205와 hybrid 특징 |
| 요구사항 명시형 | "로드맵을 제시하시오", "하이브리드 방식을 설계하시오" | 일정·pilot·rollback·감사 절차 | 위험 우선순위, MTU·지연·호환성 선택 기준 |

> 요약: 설명형은 전환 체계, 방안형은 단계 일정과 hybrid 운영 지표를 중심으로 구성함.
