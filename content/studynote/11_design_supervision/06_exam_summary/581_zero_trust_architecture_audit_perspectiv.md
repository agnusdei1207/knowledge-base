---
title: "581. 제로 트러스트 아키텍처 감리 관점 (Zero Trust Architecture Audit Perspective)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 제로 트러스트(ZTA)는 "Never Trust, Always Verify" 원칙 하에 네트워크 위치·IP·세션 일관성을 신뢰 요소에서 배제하고, NIST SP 800-207의 PE(Policy Engine)/PA(Policy Administrator)/PEP(Policy Enforcement Point) 3요소로 식별·기기·행위·데이터·환경 속성을 지속 평가하는 구조로, 감리에서는 정책결정 근거(신뢰 알고리즘 점수)와 제어점(PEP) 설정의 일관성을 검증하는 것이 핵심이다.
> 2. **가치**: IBM 2023 데이터 침해 보고서에 따르면 제로 트러스트 도입 기업은 침해 식별·제거 평균 277일->182일로 34% 단축, 침해 비용 평균 435만 달러->324만 달러(25% 절감), 정책 자동화로 운영비용 약 30% 감소 효과를 보이며, KISA 클라우드 보안 인증제(CSAP) 및 ISMS-P 1.2.3(네트워크 분리), 2.5.4(접근통제), 2.6.2(정보보호 위험 평가) 통제항목과 직접 매핑되어 통제 중복 제거 및 감사 대응성 향상에 기여한다.
> 3. **판단 포인트**: 감리 관점의 핵심은 "Zero Trust"라는 용어 자체가 아니라 ①신뢰 결정을 위한 **명시적 정책 모델**(ABAC/OPA/Rego), ② **Identity Provider(IdP)·PEP·SIEM 간 로그 정합성**, ③ **마이크로세그멘테이션 동적 정책**의 변경 이력 추적성, ④ 레거시 시스템의 에이전트리스(Agentless) 검사 범위, ⑤ 클라우드-온프레미스 하이브리드 환경의 **신뢰 앵커(Trust Anchor) 일관성** — 다섯 가지가 정책-기술-운영 관점에서 모두 정합되어야 효과적 제로 트러스트로 인정된다는 점이다.

---

## Ⅰ. 개요 및 필요성

### 1. 정의 및 등장 배경

제로 트러스트 아키텍처(Zero Trust Architecture, ZTA)는 2010년 Forrester Research의 John Kindervag가 처음 개념을 제시하고, 2019년 Google의 BeyondCorp(내부 직원 90% 이상이 VPN 없이 운영), 2020년 NIST SP 800-207 표준화, 2021년 미국 행정명령 14028(EO 14028) "Improving the Nation's Cybersecurity"로 연방정부 의무 도입, 2022년 한국 디지털정부혁신추진위원회 보안가이드라인 반영, 2024년 KISA 「클라우드·원격근무 제로트러스트 도입 가이드」 발간을 거치며 공공·금융·제조 전 분야로 확산되고 있다.

전통적 **Castle-and-Moat(성벽형) 모델**은 내부망 진입 시 일단 신뢰하고 모든 자원에 접근을 허용했으나, SolarWinds(2020), Colonial Pipeline(2021), KISA·국정원 주기적 해킹사고 통계(2023년 공공기관 침해사고 35건 중 71%가 내부横向 이동(Lateral Movement) 단계에서 발견) 등에서 보듯 **자격증명 탈취 -> 내부 횡이동 -> 데이터 유출**의 3단계 침해 패턴에 무력했다. ZTA는 네트워크 경계 자체를 신뢰 경계로 보지 않고 모든 요청을 "출처 불문 잠재적 위협"으로 간주하여 매 접근마다 정책 기반 검증을 수행한다.

### 2. 기술사 감리 관점의 특수성

일반 SI(System Integration) 프로젝트에서 ZTA는 도입·구축 관점이 중심이지만, **감리(Supervision)** 관점에서는 다음 세 가지가 다르다.

| 관점 | SI(구축) 관점 | 감리(Audit) 관점 |
|:---|:---|:---|
| **핵심 질문** | "어떻게 구축하는가?" | "구축된 ZTA가 진짜 ZTA인가?" |
| **평가 대상** | 설계서·구성도·테스트 결과 | 정책결정 로그, 신뢰 점수 산출 근거, 통제항목 매핑, 변경이력 |
| **기준 프레임** | NIST SP 800-207, CISA Zero Trust Maturity Model v2.0 | ISMS-P 통제항목, 클라우드 보안인증(CSAP), 개인정보보호법, 전자금융감독규정 |
| **증적 수집** | 구성도, 시험성적서 | 정책 변경 이력, IdP 인증로그, PEP 차단로그, SIEM 상관분석 결과 |
| **합격 기준** | 기능/성능 요구사항 충족 | 통제 누락 0건, 정책 일관성 100%, 로그 무결성, 책임추적성 확보 |

### 3. 감리 필요성: 정량 데이터로 보는 위협 변화

```text
+------------------------------------------------------------------------+
|                  제로 트러스트 감리 필요성 정량 지표                     |
+------------------------------------------------------------------------+
|                                                                        |
|  [침해 패턴 변화]            [제로트러스트 도입 효과]                   |
|                                                                        |
|  외부 침투  21% ━━━+        평균 침해 식별 시간                         |
|  자격증명  16% ━━━+    +- 277일(ZT 미적용)                             |
|  내부 횡이동 35%━┿━-> |  vs 182일(ZT 적용) -> 95일(34%) 단축            |
|  데이터탈취  28%━━━┯+   평균 침해 비용                                  |
|                     +-- 435만$ -> 324만$ (25% 절감)                     |
|                          (출처: IBM Cost of Data Breach 2023)          |
|                                                                        |
|  [감리 실패 사례 5대 패턴]                                              |
|                                                                        |
|  ❶ PEP 우회(Bypass) ------ 35%  정책결정 ≠ 실제 차단                    |
|  ❷ 로그 비정합성 ---------- 22%  IdP·PEP·SIEM 시간차/필드 불일치         |
|  ❸ 신뢰 점수 블랙박스 ---- 18%  알고리즘 비공개, 재현 불가               |
|  ❹ 레거시 에이전트 부재 --- 15%  旧 시스템 정책 미적용                   |
|  ❺ 마이크로세그멘트 정적 - 10%  동적 정책 미갱신, 초기설정 그대로         |
|                                                                        |
+------------------------------------------------------------------------+
```

### 4. 기존 경계보안 vs 제로 트러스트 패러다임

```text
[기존 경계보안 (Perimeter Security)]           [제로 트러스트 (Zero Trust)]
                                                  +------------------+
   +------------------+                          |  Policy Engine   |
   |   신뢰영역 (LAN)  |  <-- 내부 = 신뢰          |  +------------+  |
   |   +--+--+--+    |                          |  |Trust Algo  |  |
   |   |서버|DB|APP|  |                          |  |(점수산출)  |  |
   |   +--+--+--+    |                          |  +-----+------+  |
   +------+-----------+                          |        |결정     |
          |FW/VPN                                |   +----+----+   |
   +------+-------+                              |   |   PA    |   |
   |   비신뢰(외부)|                              |   +----+----+   |
   +--------------+                              |        |명령    |
                                                 |   +----+----+   |
   ❌ 한번 통과 = 모든 자원 접근                  |   |  PEP    |---+--> 자원
   ❌ 내부 횡이동 자유                           |   +---------+   |  (자원별
   ❌ IP/MAC 기반 고정 정책                      |                 |  재검증)
                                                 +------------------+
   ✅ 위치·IP 일관성 신뢰                         ✅ 매 요청 속성기반 재평가
   ✅ 단순 구성                                   ✅ 횡이동 차단 + 마이크로세그먼트
   ❌ 내부 위협 무력                               ✅ 最小권한 + 지속 모니터링
```

- **📢 섹션 요약 비유**: 전통 보안이 "회사 사원증이 있으면 모든 층 출입 가능"이라면, 제로 트러스트는 **"매 층마다 신분증·지문·소속·행동 패턴을 다시 확인하는 고급 빌딩 보안"** 과 같으며, 감리는 그 **보안 체크리스트 항목이 빠짐없이 실행되는지 CCTV·출입기록을 대조 검증**하는 일이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. NIST SP 800-207 논리 컴포넌트(Logical Components)

```text
                     제로 트러스트 아키텍처 핵심 제어 흐름

   +----------+   ①접근요청    +-------------------------------------+
   |          |  ---------->   |           제어 평면(Control Plane)  |
   |  사용자   |               |                                     |
   | (Subject)|               |   +--------------+  +------------+ |
   |  + 자원   |               |   |     PE       |  |     PA     | |
   |(Resource)|               |   | Policy Engine|<--|  Policy    | |
   |          |               |   |              |  |Administrator| |
   |  자산     |               |   | +----------+ |  |            | |
   |(Asset)   |               |   | |신뢰 알고 | |  | ④허용/거부 | |
   |          |               |   | |리즘(Trust| |  |   명령전달  | |
   |          |               |   | |Algorithm)| |  |            | |
   +----+-----+               |   | +----+-----+ |  +-----+------+ |
        | ②의도전달            |   +------+-------+        |        |
        | (Session)            |          | ③결정           |        |
        v                      |          v                 |        |
   +----------+               |   +--------------+          |        |
   |   PEP    |  -------------+--> |   정책결정    |  <--------+        |
   |(Policy   |   ③검증요청    |   |   (Yes/No)   |  ⑤구성/통지       |
   |Enforce.) |                |   +--------------+                    |
   +----+-----+                +-------------+------------------------+
        | ⑥허용 시 자원 연결                   | 정책 피드백/갱신
        v                                      v
   +----------+                       +--------------+
   |  자원    |                       |    SIEM      |
   |(Database,|  <-⑦로그 수집->         |  + 거버넌스  |
   | API, 등) |                       |  + 신뢰피드백 |
   +----------+                       +--------------+
```

### 2. 핵심 구성요소별 역할 및 기술

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **PE (Policy Engine)** | 접근 허용/거부 결정 | OPA(Open Policy Agent) + Rego 정책언어, AWS IAM Access Analyzer, Azure AD Conditional Access Policy. 입력 속성: Subject(사용자), Action(HTTP Method), Resource(ARN/URI), Environment(시간·IP·Device Posture), Risk Score(MFA·디바이스 상태·지리). 결정 시간 < 50ms p99 목표 |
| **PA (Policy Administrator)** | PE 결정에 따라 PEP 명령 발급·세션 관리 | SCIM v2.0(계정 프로비저닝), OAuth 2.0 + PKCE(인가 위임), SAML 2.0(SSO), FIDO2/WebAuthn(패스워드리스 인증). 세션 토큰 TTL ≤ 4시간(Google BeyondCorp), 정책 위반 시 세션 즉시 revoke |
| **PEP (Policy Enforcement Point)** | 데이터 경로상 정책 시행 게이트웨이 | mTLS 상호인증, TLS 1.3(전송구간 암호화), IKEv2/IPsec(네트워크 터널), SDP(Software-Defined Perimeter) 게이트웨이(예: Waverley Labs, Zscaler ZIA/ZPA), 서비스 메시(Istio Envoy Sidecar), API Gateway(Kong, Apigee), NAC(802.1X + MAB) |
| **신뢰 알고리즘 (Trust Algorithm)** | PE 내부에서 다중 속성 점수화 | Beyesian Inference, Random Forest, Neural Net 기반 UEBA(User Entity Behavior Analytics) - Exabeam, Securonix, Microsoft Cloud App Security. 출력: 0~1000점 척도, 임계치 미만 시 MFA Challenge/거부 |
| **데이터 평면 (Data Plane)** | 실제 자원 처리 | 마이크로서비스별 사이드카 프록시(Envoy), DB 접근 시 동적 마스킹(Protegrity, Vault Dynamic Secrets), 파일 DLP(Symantec DLP, Forcepoint) |
| **관리/거버넌스 평면** | 정책·로그 통합 | SIEM(Splunk, Elastic, IBM QRadar) + SOAR(Phantom, Demisto), 정책 버전관리(GitOps + ArgoCD/Flux), 신뢰 점수 피드백 루프 |

### 3. 제로 트러스트 5대 핵심 원칙 (감리 검증 포인트)

```text
   NIST SP 800-207 + CISA Zero Trust Maturity Model v2.0 5대 원칙
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ① 자원(Resource)은 논리적 단위로 분할(Logical Segmentation)
      +- 감리 검증: 네트워크 ACL, 서비스 메시 VirtualService, VPC Security Group
                   정책 행/열이 실제 통신흐름과 1:1 매핑되는지 확인

   ② 모든 통신은 위치 무관 암호화 + 인증
      +- 감리 검증: TLS 1.2 이하 구간 존재 시 부적합, 인증서 만료/자가서명 비율
                   mTLS 적용률 = (상호인증 구간) / (전체 내부 통신) × 100

   ③ 세션별/자원별 접근 결정 (Per-Session, Per-Resource)
      +- 감리 검증: 동일 사용자 1시간 내 5회 거부->허용 패턴 분석(UEBA)
                   자원이 변경될 때 재인증 요구 여부 (예: B2B->B2C 이동)

   ④ 동적 정책 결정 (Dynamic Policy)
      +- 감리 검증: 정책 변경 이력(PR/CR), 긴급 차단 시 평균 적용시간(MTTR)
                   사용자 위험 점수 변화 추적 (예: 해외IP 출현 시 +200점)

   ⑤ 지속 모니터링 + 상태 피드백 (Continuous Monitoring)
      +- 감리 검증: SIEM 수집률 > 99.5%, 로그 보관기간 ≥ 1년(전자금융감독규정)
                   정책결정-적용-결과 평균 지연시간 ≤ 1초
```

### 4. 신뢰 점수(Trust Score) 산출 예시 및 임계치

```
  Trust Score = w1 × Identity_Assurance
              + w2 × Device_Posture
              + w3 × Network_Location_Risk
              + w4 × Behavioral_Anomaly
              + w5 × Data_Sensitivity_Match

  ※ 가중치 합 = 1.0, 각 요소 0~100점

  +----------+----------+---------+--------------------------+
  |  점수대역 |  결정    | 정책반영 |  예시 시나리오           |

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 581 / 600

<- **이전**: [580. 컴포저블 아키텍처 모듈화 재사용](/studynote/11_design_supervision/06_exam_summary/581_composable_architecture_modular_reuse/)
**다음**: [582. 데이터 옵스 데이터 파이프라인 자동화](/studynote/11_design_supervision/06_exam_summary/582_dataops_data_pipeline_automation/) ->

---
