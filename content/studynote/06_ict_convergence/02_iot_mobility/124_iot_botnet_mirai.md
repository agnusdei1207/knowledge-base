---
title: "124. IoT 봇넷 & Mirai - IoT 디바이스 대상 DDoS 봇넷 공격"
date: "2026-04-19"
tags:
  - "studynote-ict-convergence"
---


## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)은 <strong>보안이 취약한 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 디바이스(IP 카메라·공유기 등)를 악성코드로 감염시켜 <a href="/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/">봇넷</a>을 구성</strong>하고, 이를 이용해 대규모 DDoS 공격을 수행하는 사이버 위협이다.
> 2. **가치**: Mirai [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)(2016)은 <strong>기본 비밀번호(admin/admin)를 사용하는 수십만 대 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 디바이스</strong>를 감염시켜 Dyn DNS에 1.2Tbps DDoS를 가해 트위터·넷플릭스 등 주요 서비스를 마비시켰다.
> 3. **판단 포인트**: [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스는 <strong>업데이트 어려움·기본 비밀번호·리소스 제한(보안 SW 설치 불가)</strong>으로 취약하며, 네트워크 세그먼테이션·[펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 자동 업데이트(FOTA)·기본 비밀번호 변경 의무화가 대응 방안이다.

---

## Ⅰ. 개요 및 필요성

```text
+-------------------------------------------------------+
|    Mirai 봇넷 공격 흐름                               |
+-------------------------------------------------------+
|  1. Mirai 스캔: Telnet(23) 포트 열린 IoT 디바이스 탐색|
|  2. 기본 비밀번호(admin/admin) 무차별 대입 -> 감염    |
|  3. 수십만 대 봇넷 구성 (C&C 서버 제어)              |
|  4. C&C 명령 -> 타겟 서버에 대규모 DDoS 공격         |
|  5. 2016년: Dyn DNS 공격 -> 주요 인터넷 서비스 마비  |
+-------------------------------------------------------+
```

- **📢 섹션 요약 비유**: Mirai는 비밀번호를 안 바꾼 수십만 개의 현관문([IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/))을 열고 들어가서, 좀비 군대([봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/))를 만들어 건물(서버)을 공격하는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 보안 취약점

| 취약점 | 설명 |
|:---|:---|
| **기본 비밀번호** | admin/admin, root/1234 |
| **업데이트 불가** | FOTA 미지원 |
| **리소스 제한** | 백신·[IDS](/studynote/02_operating_system/10_security/601_ids_ips_syscall_tracing/) 설치 불가 |
| **장기 방치** | 설치 후 관리 없음 |

- **📢 섹션 요약 비유**: [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 디바이스는 잠금장치가 없는 자전거(기본 비밀번호)와 같다. 도둑(해커)이 쉽게 훔쳐서(감염) 범죄(DDoS)에 사용한다.

---

## Ⅲ. 비교 및 연결

| 비교 | 전통 [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) ([PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)) | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) |
|:---|:---|:---|
| **대상** | [PC](/studynote/01_computer_architecture/04_instruction_set_architecture/164_pc/)·서버 | **IP 카메라·공유기** |
| **규모** | 수천~수만 | **수십만** |
| **방어** | 백신 가능 | **리소스 제한** |

---

## Ⅳ. 실무 적용 및 기술사 판단

### [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) 대응 방안
1. **기본 비밀번호 변경 의무화** (법률·표준).
2. **네트워크 세그먼테이션**: [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 전용 [VLAN](/studynote/09_security/05_web_app_security/224_vlan_virtual_lan_broadcast_domain/) 분리.
3. **FOTA**: [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 자동 보안 업데이트.
4. **트래픽 모니터링**: 이상 트래픽 탐지·차단.

---

## Ⅴ. 기대효과 및 결론

[IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)은 <strong>연결된 디바이스 수 증가와 비례</strong>하여 위험이 커지며, 기본 비밀번호 금지·FOTA 의무화·네트워크 분리가 핵심 대응 전략이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Mirai** | 2016년 [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) DDoS [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/) |
| **DDoS** | [봇넷](/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/)의 주요 공격 목적 |
| **기본 비밀번호** | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 최대 취약점 |
| **FOTA** | [펌웨어](/studynote/02_operating_system/01_overview_architecture/032_firmware/) 원격 업데이트 (보안 패치) |
| **네트워크 세그먼테이션** | [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 트래픽 격리 |

### 📈 관련 키워드 및 발전 흐름도

```text
[전통 PC 봇넷 (2000s)]
    |
    v
[Mirai IoT 봇넷 (2016) — 1.2Tbps DDoS]
    |
    v
[IoT 보안 표준화 (NIST, 2018~)]
    |
    v
[기본 비밀번호 금지법 (영국 PSTI Act, 2024)]
    |
    v
[현재: AI 기반 IoT 이상 트래픽 탐지]
```

### 👶 어린이를 위한 3줄 비유 설명
1. Mirai는 비밀번호를 안 바꾼 <strong>수십만 대의 <a href="/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/">IoT</a> 기기를 좀비(<a href="/studynote/03_network/19_frequent_topics_terms/990_botnet_cnc/">봇넷</a>)</strong>로 만들었어요.
2. 좀비 군대가 한 곳을 <strong>한꺼번에 공격(DDoS)</strong>해서 트위터·넷플릭스가 멈췄어요.
3. 비밀번호를 **반드시 바꾸고**, [IoT](/studynote/06_ict_convergence/02_iot_mobility/101_iot_concept/) 기기도 <strong>업데이트(FOTA)</strong>해야 안전하답니다!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 124 / 552

<- **이전**: [123. OCF (Open Connectivity Foundation) - IoT 상호운용성 표준](/studynote/06_ict_convergence/02_iot_mobility/123_ocf_open_connectivity_foundation/)
**다음**: [125. 무선 스니핑 & 리플레이 공격 - IoT/무선 환경 도청·재전송 위협](/studynote/06_ict_convergence/02_iot_mobility/125_wireless_sniffing_replay_attack/) ->

---
