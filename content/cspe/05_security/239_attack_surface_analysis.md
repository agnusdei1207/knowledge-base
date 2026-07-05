---
title: "공격 표면 분석 (Attack Surface Analysis)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-security"
weight: 239
---

## 1. 한눈에 이해하기 (Core Intuition)
- **정의**: 회사의 공식 자산대장(CMDB)에 있는 서버만 지키는 것이 아니라, **해커의 눈(Internet-facing)**으로 밖에서 회사를 바라보며 "공격자가 뚫고 들어올 수 있는 모든 문과 창문(공격 표면)"을 지속적으로 식별하고 줄여나가는 선제적 방어 활동입니다.
- **필요성**: 클라우드 시대에는 개발자가 임시로 띄워놓은 AWS 테스트 서버, 버려진 하위 도메인(Orphan Domain), 깃허브에 실수로 올라간 API 키 등 보안팀이 모르는 '그림자 IT(Shadow IT)'가 넘쳐납니다. 해커는 철통같이 방어된 메인 서버가 아니라, 이처럼 방치된 뒷문 하나를 통해 내부망으로 침투합니다.
- **핵심 직관**: **"보안팀의 자산대장 vs 해커의 구글링 결과"**
  - 보안팀: "우리 회사 정문은 경비원(방화벽) 3명이 지키고 있으니 안전해."
  - 해커(EASM): "인터넷 지도로 보니, 너희 집 뒷마당에 개발자가 쓰다 버린 개구멍(오픈된 S3 버킷)이 하나 있고 열쇠(API 키)가 바닥에 떨어져 있던데?"

## 2. 깊이 이해하기 (In-Depth Comprehension)
- **배경**: 과거의 취약점 진단(CVE 스캐닝)은 "내가 아는 자산"만 점검했습니다. 하지만 최근 대형 해킹 사고의 70%는 "회사가 존재하는지도 몰랐던 자산"에서 시작됩니다. 이에 따라 자산 식별의 패러다임이 내부에서 외부(해커 관점)로 전환되었습니다.
- **작동 원리 (EASM과 CAASM의 결합)**:
  - **EASM (External Attack Surface Management)**: 밖에서 집을 관찰. DNS 기록, 인증서(CT Log), Shodan(다크웹 검색엔진) 등을 뒤져 우리 회사 소유로 보이는 모든 공개 IP, 도메인, 열린 포트를 24시간 자동 수집합니다.
  - **CAASM (Cyber Asset ASM)**: EASM이 밖에서 찾은 자산을 내부망의 취약점 데이터, 클라우드(CSPM) 정보, ID 정보와 결합(Mapping)하여 "이 개구멍의 진짜 주인이 누구인지(Owner)", "여기로 들어오면 회사 핵심 DB까지 갈 수 있는지(Attack Path)"를 분석합니다.
- **구체 예시 (서브도메인 탈취, Subdomain Takeover)**: 회사가 `event.company.com`을 외부 SaaS 서비스에 연동해 쓰다가 행사가 끝나 SaaS 결제만 취소하고 DNS 연결은 지우지 않았습니다. 해커가 해당 SaaS에 가입해 `event.company.com` 주소를 자기 계정으로 낚아채면, 고객들은 정상적인 회사 도메인으로 접속했지만 해커가 만든 피싱 사이트로 연결됩니다.
- **흔한 오해/주의점**: "공격 표면 분석은 취약점 점검(Vulnerability Scan)과 같은 것 아닌가요?" $\rightarrow$ 완전히 다릅니다. 취약점 점검은 '이미 알고 있는 자산'이 얼마나 아픈지(CVE) 진단하는 것이고, 공격 표면 분석은 **'내가 모르는 자산'을 발견(Discovery)**하여 해커에게 노출되어 있는지를 찾아내는 첩보 활동입니다.

## 3. 연결 개념 (Related Concepts)
- **Shadow IT (섀도우 아이티)**: 현업 부서나 개발자가 IT/보안팀 몰래 퍼블릭 클라우드(AWS, SaaS)를 개통하여 사용하는 현상 (주요 공격 표면).
- **OSINT (Open-Source Intelligence)**: 구글링, 깃허브 검색, Shodan 등 공개된 출처에서 위협 정보를 수집하는 기술 (EASM의 핵심 기술).
- **Attack Path (공격 경로)**: 발견된 개별 취약점들을 연결하여, 최종 목적지(DB)까지 도달하는 해커의 동선을 그리는 최신 위협 분석 기법.

---

# ✍️ 답안용 골격 (Exam Preparation)

### Ⅰ. 핵심 인사이트
- **본질**: 하이브리드 클라우드와 SaaS 도입으로 붕괴된 전통적 네트워크 경계(Perimeter) 환경에서, 내부의 정적인 자산대장(CMDB)에 의존하지 않고 외부 공격자 관점(Outside-In)에서 인터넷에 노출된 자산(Digital Footprint)과 섀도우 IT를 지속 식별/모니터링하는 **ASM(Attack Surface Management)** 체계.
- **가치**: "알려지지 않은 미식별 자산(Unknown Unknowns)의 가시성 확보". 공격자는 가장 약한 하나의 고리(단일 노출 지점)를 통해 침투합니다. EASM을 통해 방치된 하위 도메인, 공개된 S3 스토리지, 유출된 인증 정보(Credential)를 식별하고 선제 차단하여 1차 침해(Initial Compromise) 확률을 극적으로 낮춥니다.
- **판단 포인트**: EASM 도구를 도입한다고 끝나는 것이 아닙니다. 수만 개의 노출 지점 알람 속에서 보안팀이 지치지 않으려면, 외부 노출 자산을 내부의 문맥(Context)과 결합하는 **CAASM 아키텍처**를 구축하여, 취약점의 CVSS 점수가 아닌 '공격 가능성(Exploitability)과 비즈니스 중요도(Criticality)'를 기준으로 조치 우선순위(SLA)를 정교하게 타겟팅해야 합니다.

### Ⅱ. ASM 아키텍처의 2대 축 (EASM vs CAASM)
외부 첩보(EASM)와 내부 문맥(CAASM)의 통합 프레임워크.
| 비교 지표 | EASM (External ASM) | CAASM (Cyber Asset ASM) |
|---|---|---|
| **관찰 시점** | **Outside-In** (해커의 눈으로 밖에서 안을 봄) | **Inside-Out** (내부 시스템 연동 기반 가시성 확보) |
| **목적** | 알려지지 않은 인터넷 공개 자산(Shadow IT) 발견 | 기존 사일로화된 내부 자산 데이터의 통합 및 가시화 |
| **주요 수집원** | OSINT, DNS/CT 로그, Shodan, BGP 라우팅 정보 | AD, EDR, CSPM, 취약점 스캐너의 API 연동 |
| **핵심 산출물** | Exposed Port, Orphan Domain, Public Bucket 목록 | 자산별 소유자(Owner) 매핑, 조치 우선순위 도출 |

### Ⅲ. 공격 표면(Attack Surface)의 4대 핵심 위협 벡터
EASM이 지속적으로 모니터링해야 하는 블라인드 스팟(Blind Spot).
1. **버려진 인프라 (Orphaned / Abandoned Assets)**: 퇴사한 개발자가 남겨둔 AWS 테스트 서버(오래된 OS, 패치 미적용), 관리되지 않는 하위 도메인(Subdomain Takeover 위험).
2. **잘못된 클라우드 설정 (Misconfigurations)**: 인터넷에 '전체 공개(Public Read)'로 설정된 AWS S3 버킷, 패스워드 없이 노출된 Elasticsearch/Redis 데이터베이스.
3. **디지털 정보 유출 (Exposed Secrets)**: GitHub 퍼블릭 리포지토리에 하드코딩된 API Key, 다크웹에서 거래되는 임직원의 로그인 크레덴셜.
4. **그림자 IT (Shadow IT)**: 보안팀 승인 없이 부서 예산으로 몰래 가입하여 기밀을 올리고 있는 SaaS(Notion, Slack 등) 워크스페이스.

### Ⅳ. 조치 우선순위(Prioritization)와 Attack Path 도출
발견된 수만 개의 노출 지점 중 무엇부터 막을 것인가?
- **기존 방식 (CVSS 의존)**: CVSS 9.0인 내부망의 테스트 서버를 먼저 패치함. (비효율적).
- **ASM 기반 방식 (Attack Path Context)**: CVSS가 6.0이더라도 "인터넷에 포트가 열려 있고(Public Exposure) $\rightarrow$ 해당 서버에 관리자 권한 토큰이 있으며(Privilege) $\rightarrow$ 그 토큰으로 핵심 고객 DB에 접근할 수 있는(Attack Path)" 자산을 **Critical(0순위 조치 대상)**로 분류하여 선행 차단.

### Ⅴ. 결론 및 실무적 판단 포인트
- CISO는 "우리는 이미 취약점 스캐너(Scanner)가 있으니 안전하다"는 착각을 버려야 합니다. 스캐너는 IP 대역을 알려줘야만 동작합니다. EASM은 당신이 모르는 IP 대역을 찾아내는 레이더입니다.
- 실무 적용의 핵심은 **"발견된 자산의 소유자(Owner) 매핑 자동화"**입니다. 발견 즉시 CAASM 엔진을 통해 사내 인사 DB(HR)와 인프라 신청 이력을 대조하여 자산 소유자에게 Jira 티켓을 자동 발송하고, 72시간 내 조치(SLA)를 강제하는 폐쇄 루프(Closed-loop) 거버넌스가 구축되지 않으면 EASM은 그저 경고 알람(Noise) 발생기에 불과하게 됨을 명심해야 합니다.

### 💡 문제 유형별 목차 전환 포인트
- **[클라우드 및 재택근무 환경 확산에 따른 공격 표면 최소화(ASM) 전략]**: Ⅰ과 Ⅲ(4대 위협 벡터)을 전면에 세워, 전통적인 방화벽(경계 보안)이 붕괴된 상황에서 해커의 초기 침투(Initial Access)를 막기 위한 OSINT 기반 가시성 확보 논리 증명.
- **[보안 사일로(Silo) 타파 및 위험 기반(Risk-based) 취약점 관리 고도화 방안]**: Ⅱ(CAASM)와 Ⅳ(우선순위/Attack Path)를 엮어, "EASM이 찾아낸 수많은 외부 자산 데이터를 기존 보안 솔루션(EDR/SIEM)과 어떻게 통합하여 노이즈(오탐)를 줄이고 비즈니스 임팩트 기반의 대응(Remediation) 체계를 만들 것인가"에 대한 최상위 거버넌스 해법 전개.
