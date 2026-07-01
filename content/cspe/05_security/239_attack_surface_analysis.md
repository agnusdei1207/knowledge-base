---
title: "공격 표면 분석 (Attack Surface Analysis)"
date: "2026-07-01"
tags:
  - "cspe-security"
weight: 239
---

# 📖 【암기용】 개념 완전 이해

> 목적: 공격 표면 분석을 처음 봐도 완벽히 이해하게 만든다. 시험 답안 양식이 아니라, 이해를 위한 친절한 설명이다.

## 한눈에
- **개요**: 공격자가 접근 가능한 자산·API·계정·클라우드 노출 지점을 식별하고 줄이는 활동
- **왜 필요한가**: 기업 자산은 클라우드, SaaS, 외부 API, 개발자 저장소로 흩어져 있어 CMDB만으로 공개 노출을 파악하기 어렵다.
- **핵심 직관**: 내부 보안팀이 보는 자산 목록이 아니라, 인터넷에서 공격자가 실제로 볼 수 있는 입구 목록을 만드는 작업이다.

## 깊이 이해
- **배경·문제의식**: 공개 IP, DNS, API endpoint, S3 bucket, Git secret, SaaS OAuth 앱, 임시 계정은 배포와 조직 변경 때 빠르게 늘어난다. 공격자는 가장 약한 공개 노출 하나를 통해 초기 침투를 시도한다.
- **작동 원리**: EASM(External Attack Surface Management)은 외부에서 보이는 도메인·IP·인증서·포트·클라우드 리소스를 수집한다. CAASM(Cyber Asset Attack Surface Management)은 내부 자산·취약점·ID·EDR 데이터를 연결해 소유자와 조치 우선순위를 정한다.
- **비유**: 집 안 자물쇠만 확인하는 것이 아니라, 지도 앱과 거리 사진으로 보이는 창문, 지하 출입구, 우편함 열쇠까지 찾는 외부 관찰이다.
- **구체 예시**: 폐쇄된 프로젝트의 서브도메인이 외부 SaaS를 가리킨 채 남아 있으면 subdomain takeover가 가능하다. EASM은 DNS CNAME과 SaaS 응답을 대조해 조치 대상으로 표시한다.
- **흔한 오해·주의점**: 공격 표면 분석은 취약점 스캔과 같지 않다. 취약점 유무 이전에 자산이 존재하는지, 외부에서 접근 가능한지, 소유자가 누구인지부터 확정해야 한다.

## 연결 개념
- EASM — 외부 관점에서 인터넷 노출 자산을 지속 탐색
- CAASM — 내부 자산·ID·취약점 데이터를 통합해 소유자와 상태를 추적
- Attack Path — 노출 자산에서 핵심 자산까지 이어지는 침투 경로

---

# 📝 【답안용】 시험 답안 템플릿

> 목적: 시험장에서 25분에 그대로 쓰는 답안 양식. 작성방식(추상표현 금지·수치·도식·문제유형 전환)을 엄격히 지킨다.
> 핵심: 자산 목록 나열이 아니라 외부 노출, 소유자, 취약점, 공격 경로, 조치 우선순위를 연결해야 한다.

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 공격 표면 분석은 외부 공격자가 접근 가능한 asset, API, identity, cloud exposure, secret을 식별해 침투 가능 지점을 줄이는 활동이다.
> 2. **가치**: EASM·CAASM 기반으로 shadow IT, orphan domain, exposed secret, 공개 스토리지를 탐지해 초기 침투 가능성을 낮춘다.
> 3. **판단 포인트**: 단순 취약점 심각도보다 인터넷 노출 여부, 인증 필요성, 공격 경로, 자산가치, 조치 난이도를 함께 고려한다.

## 출제 의도 및 답안 포인트

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 공격자 관점 자산 식별 역량 확인 | asset/API/identity/cloud/public exposure | 내부 CMDB 자산 목록만 설명 |
| 운영형 보안 통제 판단 확인 | EASM, CAASM, attack path, owner, remediation priority | 취약점 스캔과 동일시 |
| 우선순위 산정 역량 확인 | 공개 노출, exploitability, business criticality | CVSS 점수만으로 순위 결정 |

> 요약: 이 문제는 공격자가 볼 수 있는 입구를 찾아 소유자·위험·조치 순서까지 닫는 운영 체계를 요구한다.

---

## Ⅰ. 개요 및 필요성

공격 표면 분석은 공격자가 접근 가능한 노출 지점을 식별·축소하는 활동이다. 클라우드와 SaaS 사용이 늘면 공개 자산이 배포 자동화, 테스트, 외주 개발 과정에서 누락될 수 있다. 지속 탐색과 우선순위 조치 없이는 취약점보다 먼저 자산 누락이 침투 원인이 된다.

---

## Ⅱ. 구조 및 구성요소

```text
외부 관찰(EASM) -> 자산 식별 -> 내부 매핑(CAASM)
              -> 취약점/ID/secret 연결 -> attack path 분석
              -> 우선순위 조치 -> 노출 축소
```

| 구성요소 | 역할 | 특이사항 |
|:---|:---|:---|
| Asset Discovery | 도메인, IP, 인증서, 포트 수집 | DNS, CT log, ASN, CSP API |
| Exposure Analysis | 공개 서비스·스토리지·API 노출 확인 | unauth API, public bucket |
| Identity Surface | 계정·권한·OAuth 앱 노출 분석 | orphan account, excessive privilege |
| Attack Path | 노출 지점에서 핵심 자산까지 경로 분석 | exploit chain, lateral movement |
| Remediation | owner 지정과 조치 우선순위 관리 | SLA, exception, 재검증 |

> 요약: 구조는 외부 노출 자산을 찾고 내부 소유자·취약점·권한 데이터와 연결해 공격 경로 기준으로 조치한다.

---

## Ⅲ. 동작원리 및 흐름도

```text
도메인/IP 수집 -> 서비스 fingerprint -> 공개 노출 판정
              -> 취약점/secret/ID 매핑 -> attack path 산정
              -> owner 할당 -> 조치/재스캔
```

| 단계 | 처리 내용 | 검증 기준 |
|:---:|:---|:---|
| 1 | DNS, CT log, CSP, Git, SaaS 데이터 수집 | 신규 자산 탐지 주기 24시간 이하 |
| 2 | 포트, 배너, 인증서, API 응답 fingerprint | 미승인 서비스 식별 |
| 3 | 취약점, secret, ID 권한, 데이터 등급 매핑 | CVE, leaked key, IAM policy |
| 4 | 공격 경로와 사업 영향 산정 | crown jewel 접근 가능성 |
| 5 | 소유자 할당, 조치, 재검증 | SLA, closure evidence |

> 요약: 흐름은 외부 탐색으로 시작해 내부 맥락을 붙이고, 공격 경로와 소유자 기준으로 노출을 줄이는 순서이다.

---

## Ⅳ. 특징

| 구분 | 취약점 스캔 | 공격 표면 분석 | 수치·기준 |
|:---|:---|:---|:---|
| 관점 | 알려진 자산의 CVE 탐지 | 알려지지 않은 노출 자산 발견 | unknown asset 비율 |
| 대상 | 서버·패키지 | 도메인, API, cloud, ID, secret | EASM, CAASM |
| 우선순위 | CVSS 중심 | 노출+경로+자산가치 | public exposure, exploitability |
| 산출물 | 취약점 리포트 | 자산 소유자·attack path·SLA | Critical 24~72시간 |

> 요약: 공격 표면 분석은 취약점 점검 이전에 외부 노출 자산과 침투 경로를 찾는 활동이다.

---

## Ⅴ. 심화 비교 및 적용 판단

| 비교 축 | 기존/대안 | 본 키워드 | 선택 기준 |
|:---|:---|:---|:---|
| 자산 관리 | CMDB 수동 등록 | EASM/CAASM 자동 발견 | 클라우드 계정·도메인 다수 |
| 위험 산정 | CVSS 점수 단독 | 노출, 자산가치, attack path 결합 | 인터넷 공개 서비스 우선 |
| 운영 통제 | 분기별 스캔 | 지속 탐색·SLA 조치 | 배포 빈도 주 1회 이상 |

> 요약: 공개 자산 변화가 큰 조직은 정적 CMDB보다 EASM·CAASM 기반 지속 분석이 필요하다.

| 리스크 | 원인 | 대응 방안 | 확인 지표 |
|:---|:---|:---|:---|
| Shadow IT | 미승인 클라우드·SaaS 사용 | 도메인·CSP·SaaS discovery | unknown asset 5% 이하 |
| Secret 노출 | Git·CI 로그·이미지에 키 포함 | secret scan, key rotation | exposed secret MTTR 24시간 이하 |
| 우선순위 오류 | CVSS만 보고 핵심 경로 누락 | attack path, business criticality 반영 | critical path 조치율 100% |

> 요약: 핵심 리스크는 미등록 자산, 비밀정보 노출, 우선순위 오류이며 탐색·회전·경로 분석으로 통제한다.

| 점검 항목 | 목표 기준 | 측정 방법 |
|:---|:---|:---|
| 자산 커버리지 | EASM 발견 자산 95% owner 지정 | EASM-CAASM 대조 |
| 노출 조치 | Critical public exposure 72시간 내 조치 | ticket SLA, 재스캔 |
| 비밀정보 대응 | leaked key 24시간 내 폐기 | secret scanner, KMS log |

> 요약: 성과는 발견 자산 수가 아니라 owner 지정률, 노출 조치 SLA, 비밀정보 폐기 시간으로 판단한다.

---

## Ⅵ. 실무 적용 및 결론

**적용 방안 3개:**
1. DNS, CT log, CSP API, Git 저장소, SaaS inventory를 EASM에 연결해 신규 공개 자산을 24시간 이내 탐지함
2. CAASM으로 CMDB, EDR, IAM, vuln scanner 데이터를 결합하고 owner 없는 자산은 배포 차단 대상으로 등록함
3. remediation priority는 public exposure, exploit availability, data sensitivity, attack path depth 4축으로 산정함

**결론 (2줄):**
- 기술사 판단: 인터넷 공개 자산과 클라우드 계정이 많은 조직은 취약점 스캔보다 공격 표면 분석을 선행 통제로 둔다
- 향후 방향: EASM·CAASM·CNAPP·ASM 데이터를 통합해 노출 발견에서 자동 조치까지 폐쇄 루프를 구성한다

---

### 🔀 문제 유형별 목차 전환 (이 키워드 출제 시)

| 유형 | 문제 신호어 | Ⅲ 강조 | Ⅳ 강조 |
|:---|:---|:---|:---|
| 포괄형 | "공격 표면 분석을 설명하시오", "기술하시오" | 발견, 매핑, 경로 분석, 조치 흐름 | 취약점 스캔과 차이 |
| 요구사항 명시형 | "도입 방안을 제시하시오", "운영 기준을 설계하시오" | EASM/CAASM 연계와 SLA 운영 | 우선순위 산정, 지표, owner 관리 |

> 요약: 설명형은 개념·구조를, 운영형은 지속 탐색·우선순위·SLA 지표를 중심으로 목차를 바꾼다.
