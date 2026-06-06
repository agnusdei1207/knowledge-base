---
title: "540. 사고 관리 인시던트 대응 프로세스 (Incident Management Response Process)"
date: "2026-05-09"
tags:
  - "studynote-design-supervision"
---


## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 사고 관리 인시던트 대응 프로세스는 **ITIL 4 Incident Management**(서비스 조기 복구)와 **NIST SP 800-61 r2 Security Incident Handling**(침해 차단/근절/복구)을 통합한 다층 대응 체계로, `Detection -> Triage -> Containment -> Eradication -> Recovery -> Post-Incident Activity`의 6단계 라이프사이클을 가지며, **Incident Commander(INC)**, **Communication Lead**, **Operations Lead**의 3-Role 모델로 의사결정·전파·기술처리를 분리한다.
> 2. **가치**: 성숙한 인시던트 프로세스 도입 시 **MTTD(Mean Time To Detect) 70%v**, **MTTR(Mean Time To Resolve) 50~60%v**, **Alert Noise 80%v**(P1/P2 비율 5% 이내) 효과를 통해 **SLA 99.9% -> 99.99%**(Four 9s) 달성이 가능하며, Post-Mortem의 **Blameless 문화**는 동일 사고 재발률을 평균 65% 감소시킨다(Google SRE Book, 2017 기준 사례).
> 3. **판단 포인트**: 핵심 트레이드오프는 ①**자동화 범위**(SOAR Auto-Remediation vs Human-in-the-Loop), ②**Severity 분류 매트릭스**(Impact × Urgency의 4×4 셀 설계), ③**On-Call 피로도 관리**(주 1회 -> 격주 -> 7명 풀로 Pager Fatigue 방지), ④**War Room 개시 임계치**(P1 즉시 / P2 15분 / P3 SLA 내)이며, 기술사 논술에서는 **NIST CSF의 Detect/Respond/Recover 함수와의 정합성**과 **ISO/IEC 27035와의 매핑**을 반드시 입증해야 한다.

---

## Ⅰ. 개요 및 필요성

현대 정보시스템은 **마이크로서비스 아키텍처**, **멀티클라우드(AWS/Azure/GCP)**, **Kubernetes 기반 컨테이너 오케스트레이션**, **API Gateway**의 조합으로 구성되어 단일 장애점(SPOF)이 사실상 제거되었지만, **관측 가능성(Observability)**·**의존성 복잡도**·**공급망(Supply Chain) 위협**이 기하급수적으로 증가하면서 **"어디에서 사고가 터졌는지조차 모르는" Blind Spot**이 새로운 SPOF로 부상했다. Gartner(2023) 보고에 따르면 대규모 기업의 평균 장애 대응 시간은 **287분(약 4.8시간)**이며, 이 중 45%가 **인지(Detection) -> 인지 후 보고(Notification)** 구간에서 소요된다.

기존의 **"전화기 응대 + 수동 로그 분석"** 방식은 다음 3가지 한계를 갖는다:

| 기존 패러다임 | 한계 | 신규 패러다임의 대응 |
|:---|:---|:---|
| 사후 대응(Reactive) | 장애 발생 후 사용자 신고로 인지 | **Observability 3-Pillar**(Metrics·Logs·Traces) 기반 능동 탐지 |
| 단일 전문가 의존 | Hero Culture, 지식 사일로 | **3-Role Incident Command System + Blameless Post-Mortem** |
| 보안/서비스 분리 | IT 인시던트와 보안 인시던트를 별개 처리 | **Unified Incident Pipeline**(SIEM ↔ ITSM 양방향 연동) |

특히 **NIST CSF 2.0**(2024.02 발표)에서는 **GOVERN(거버넌스)** 함수가 신설되어 인시던트 대응이 **단순 운영 과제에서 거버넌스/리스크 관리의 핵심축**으로 격상되었으며, **DORA(Digital Operational Resilience Act, EU 2022/2554)**는 금융기관 대상 인시던트 분류(Class I/II) 및 분류별 보고时限(1시간/24시간/72시간)을 의무화하고 있어, **인시던트 분류 체계 자체가 컴플라이언스 요구사항**이 되었다.

```text
+----------------------------------------------------------------------+
|           인시던트 대응의 진화: 1세대 -> 4세대 패러다임               |
+----------------------------------------------------------------------+

[1세대: 1990s] 전화기 + Runbook        ->  평균 복구 24~72시간
   |  Hero형 대응, 지식 = 개인 소유
   v
[2세대: 2000s] ITSM 도구(ServiceNow)   ->  평균 복구 4~8시간
   |  티켓 기반 워크플로우, ITIL v3 도입
   v
[3세대: 2010s] Monitoring+PagerDuty     ->  평균 복구 30~60분
   |  SaaS 알림, DevOps 문화, ChatOps
   v
[4세대: 2020s] Observability + AIOps + SOAR  ->  평균 복구 5~15분
   |  자동 분류, Runbook Automation, War Room in Slack/Teams
   v
[5세대: 2024+] LLM-Aided Incident Response (예정)
   |  GPT-4/Claude 기반 로그 상관분석, RCA 자동 초안
   v
+----------------------------------------------------------------------+
|  변화의 핵심 축: MTTD/MTTR 단축 + 인지->전파 시간 Zero화에 집중      |
+----------------------------------------------------------------------+
```

- **📢 섹션 요약 비유**: 인시던트 대응은 **병원 응급실(ER)**과 같다. ①**Detection**= 환자가 응급실 도착(트리아지), ②**Triage**= 간호사가 중증도 분류, ③**Containment**= 생명 징후 안정화, ④**Eradication**= 원인 제거(수술), ⑤**Recovery**= 회복실, ⑥**Post-Incident**= 퇴원 후 Follow-up. **골든타임(통상 4~6시간)** 안에 치료하지 못하면 예후가 급격히 악화되는 것과 같이, **P1 인시던트의 Service Restoration Window**가 곧 고객 신뢰의 골든타임이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 1. 인시던트 대응 6단계 라이프사이클 (NIST SP 800-61 r2 + ITIL 4 통합)

```text
+-----------------------------------------------------------------------------+
|        Unified Incident Response Lifecycle (6-Phase)                       |
|                                                                             |
|  +--------------+    +--------------+    +--------------+                  |
|  |  1.Preparation|---->|2.Detection & |---->|3.Triage &    |                  |
|  |              |    |  Analysis    |    |  Classification|                 |
|  +--------------+    +--------------+    +--------------+                  |
|        ^                                         |                          |
|        |                                         v                          |
|  +--------------+                       +------------------+                |
|  | 6.Post-Incident|<---------------------|4.Containment &   |                |
|  |   Activity    |                       |   Eradication    |                |
|  +--------------+                       +------------------+                |
|                                               |                            |
|                                               v                            |
|                                     +------------------+                  |
|                                     |5.Recovery &      |                  |
|                                     |   Service Restore |                  |
|                                     +------------------+                  |
|                                                                             |
|  ---- 보안 인시던트 경로  ==== 서비스(IT) 인시던트 경로                    |
+-----------------------------------------------------------------------------+
```

### 2. 기술 아키텍처 및 데이터 플로우

```text
+--------------------------------------------------------------------------+
|              End-to-End Incident Response Architecture                  |
+--------------------------------------------------------------------------+
 [사용자/모니터링]         [Detection Layer]              [Orchestration]
 +------------+           +------------------+          +--------------+
 |  End User  |--신고---> |  Synthetic Mon.  |          |   PagerDuty  |
 |  Help Desk |          |  (Pingdom/Datadog|          |   Opsgenie   |
 +------------+          |   Synthetics)    |          |   VictorOps  |
                         +--------+---------+          +------+-------+
 +------------+                   |                            |
 | IoT/Edge   |                   v                            |
 | Device     |          +------------------+                 |
 +-----+------+          |   SIEM/Log Lake  |  <-----Security--+
       | 알람            | (Splunk/QRadar/  |   Event        |
       v                 |  Sentinel/Elastic)|                |
+------------+           +--------+---------+                |
|  APM Agent |                    |                           |
| (Datadog/  |-------------------->|  Alert Routing            |
|  New Relic)|                    |  (Rule Engine)            |
+------------+                    v                            v
                          +------------------+      +------------------+
                          | AIOps/Noise      |      | ITSM/ServiceNow  |
                          | Reduction        |      | Jira Service Mgmt|
                          | (BigPanda/Moogsoft)    +--------+---------+
                          +--------+---------+               |
                                   | 자동 매핑/중복제거      |
                                   v                          v
                          +------------------------------------------+
                          |       Incident Record (Single Pane)      |
                          |  +------------------------------------+  |
                          |  | Incident ID, Severity, Timeline,    |  |
                          |  | Affected CIs, Linked Alerts,        |  |
                          |  | Runbook, Communication Log          |  |
                          |  +------------------------------------+  |
                          +--------+------------------+--------------+
                                   |                  |
                                   v                  v
                          +--------------+   +------------------+
                          |  War Room    |   |  SOAR/Automation |
                          | (Slack/Teams |   | (XSOAR/Splunk    |
                          |  +Zoom/Meet) |   |  SOAR/Tines)     |
                          +------+-------+   +--------+---------+
                                 |                    |
                                 v                    v
                          +----------------------------------+
                          |   Resolution + Post-Mortem       |
                          |   - Action Items (Jira)          |
                          |   - Knowledge Base (Confluence)  |
                          |   - Runbook Update               |
                          +----------------------------------+
```

### 3. 핵심 구성 요소 및 책임

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
|:---|:---|:---|
| **Detection Source** (탐지 소스) | 이상 징후의 1차 포착 | **Prometheus/Thanos**(메트릭), **Fluentd/Vector**(로그), **Jaeger/Tempo**(분산 트레이싱), **eBPF**(커널 레벨), **Synthetic Monitoring**(Pingdom/Checkly), **Real User Monitoring(RUM)**(Datadog RUM/New Relic Browser) |
| **Correlation & Noise Reduction** (상관분석·잡음 감소) | 다수 알람의 그룹화·중복 제거·우선순위 산정 | **AIOps 플랫폼**: BigPanda, Moogsoft, ServiceNow AIOps, **PagerDuty Event Rules**(JSONPath 조건 매칭, 5분 윈도우 내 동일 fingerprint 알람 자동 머지), **Datadog Watchdog**(ML 기반 이상탐지) |
| **Incident Command System (ICS)** (지휘 체계) | 3-Role 모델로 의사결정·전파·기술 분리 | **Incident Commander(INC)**: 의사결정 총괄, **Communications Lead**: 임원/이해관계자/Status Page 업데이트, **Operations Lead(Scribe)**: 기술 조사·타임라인 기록, **Subject Matter Expert(SME)**: 도메인 전문가 |
| **Communication Channel** (전파 채널) | 실시간 협업·정보 공유 | **전용 War Room 채널**: Slack `/inc` 명령어로 자동 채널 생성(Incident Bot), **화상회의**: Zoom/Google Meet 자동 Join URL, **Status Page**: Statuspage.io, Better Uptime, Instatus(외부 고객용) |
| **Runbook / Playbook** (대응 절차서) | 표준화된 조사·복구 절차 | **Runbook**: 기술적 단계별 명령어(SQL, kubectl, API call), **Playbook**: 의사결정 트리(시나리오별 분기), 형상관리: Git에 Markdown으로 저장, **SOAR 연동 시 자동 실행** |
| **Post-Mortem System** (사후 분석) | 재발 방지 및 조직 학습 | **Blameless Post-Mortem** 문화, **5 Whys + Fishbone(Ishikawa) Diagram** 원인 분석, **Action Item**을 Jira/Linear에 자동 생성, **Incident Database**: Jeli.io, incident.io(타임라인·의사결정 기록 영구 보존) |
| **SOAR (Security Orchestration, Automation, Response)** | 반복 작업 자동화 | **Cortex XSOAR(Demisto)**, **Splunk SOAR(Phantom)**, **Tines**, **n8n**, **nuclei**(취약점 자동 스캔 -> 티켓 자동 생성) |
| **ITSM / Ticketing** (티켓 관리) | 인시던트의 영구 기록·SLA 추적 | **ServiceNow ITSM**, **Jira Service Management**, **Freshservice**, **Zendesk**, **PagerDuty Incident API**(양방향 동기화) |

### 4
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 540 / 600

<- **이전**: [539. 릴리스 관리 배포 전략 롤백](/studynote/11_design_supervision/06_exam_summary/539_release_management_deployment_rollback)
**다음**: [541. 문제 관리 근본 원인 분석 RCA](/studynote/11_design_supervision/06_exam_summary/541_problem_management_root_cause_analysis/) ->

---
