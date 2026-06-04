+++
title = "399. 사고 대응 IR 포렌식 분석 절차 (Incident Response IR Forensics Analysis)"
date = 2026-05-09

[taxonomies]
tags = ["studynote-it-management"]

[extra]
tags = ["studynote-it-management"]
+++

# 399. 사고 대응 IR 포렌식 분석 절차 (Incident Response IR Forensics Analysis)

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: NIST SP 800-61 rev.2의 6단계(Preparation->Identification->Containment->Eradication->Recovery->Lessons Learned)와 RFC 3227의 휘발성 순서(Register/Memory->Routing Table->Process->File system->Remote logs->Physical config) 기반의 체계적 증거 수집·분석 체계. 휘발성 데이터(Volatile Artifact)의 손실 최소화, 무결성 해시(SHA-256), Chain of Custody(연계 보관 서류) 유지를 통해 법적 효력 있는 디지털 증거를 확보한다.
> 2. **가치**: 평균 침해사고 분석 시간(MTTR)을 60% 이상 단축하며, MITRE ATT&CK 매핑을 통한 TTP(Tactics, Techniques, Procedures) 식별로 재발 방어 룰(EDR/SIEM) 자동 생성 가능. 감염 경로·범위·유출 데이터 0.1% 이내 정밀 분석은 보험·규제 대응·법적 공방에서 핵심 결정 근거가 된다.
> 3. **판단 포인트**: "전원 차단(Pull-the-plug) vs Live Forensics" 트레이드오프, 클라우드/EDR 기반 원격 포렌식 vs 전통적 이미지 기반 포렌식, 메모리 포렌식 도구 검증(Volatility 3 Offset Profile vs MemProcFS) 선택, 한국 정보통신망법·통신비밀보호법·개인정보보호법 등 3법 충돌 시 증거 인용 가능성 사전 검토.

---

## Ⅰ. 개요 및 필요성

현대 엔터프라이즈 환경은 랜섬웨어·공급망 공격(Supply Chain Attack)·내부자 위협이 결합된 복합 침해사고(Full-Scope Compromise)가 주류가 되었다. 2023년 이후 클라우드·SaaS·Kubernetes 환경의 비중이 70%를 넘으면서 전통적 디스크 이미지 기반 포렌식(Dead Forensics)만으로는 휘발성 메모리·컨테이너 오버레이 파일시스템·IaC(Infrastructure as Code) 흔적을 포착하기 어려워졌다. 또한 한국에서는 「정보통신망법」 제48조의2, 「개인정보보호법」 제29조(안전조치의무), 「통신비밀보호법」 제3조(통신사실 확인자료 제공)의 3법이 IR 절차에 동시에 적용되어, 한국형 IR Playbook이 필요하다.

NIST SP 800-61 r2는 6단계(Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned)를, ISO/IEC 27035는 5단계(Plan & Prepare, Detection & Reporting, Assessment & Decision, Response, Lessons Learnt)를 제시하며, SANS는 PICERL(Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned) 모델을 운영한다. 단순 침해 탐지가 아닌, **법적 증거력 있는 사고 재구성(Reconstruction)**이 IR 포렌식의 핵심 가치다.

```text
+----------------------------------------------------------------------+
|   NIST SP 800-61 r2 Incident Response Lifecycle (6 Phases)            |
|   +------------------------------------------------------------+    |
|   | 1) Preparation        2) Identification    3) Containment  |    |
|   |    - 자산 식별             - IoC/TTP 탐지         - 단기 격리 |    |
|   |    - Playbook             - Scope 산정           - 네트워크  |    |
|   |    - Tool kit             - 초기 침해 시점(K)     - 봉쇄      |    |
|   |                                                            |    |
|   | 4) Eradication        5) Recovery            6) Lessons    |    |
|   |    - Malware 제거         - 복구 검증            - 재발방지  |    |
|   |    - 백도어 점검          - 모니터링 강화         - 보고서    |    |
|   |    - 계정/키 회전          - 사용자 통보         - Playbook  |    |
|   +------------------------------------------------------------+    |
|                                                                       |
|   -- Forensic Trigger Points (★) ---------------------------------    |
|     • Identification 단계 : 휘발성 증거 수집(Live Response)           |
|     • Containment 단계    : 디스크 이미지(DD/E01/AFF4) 확보            |
|     • Eradication 단계    : 메모리/디스크 정밀 분석 (Root Cause)        |
+----------------------------------------------------------------------+
```

**Old Paradigm (전통 IR)**: 정적 분석 -> 오프라인 디스크 이미지 -> 수동 타임라인 -> 전문가 수개월 소요
**New Paradigm (현 IR)**: EDR/XDR 기반 원격 Live Response -> 메모리 포렌식(Volatility 3) -> TTP 기반 위협 헌팅(Hunting) -> SOAR 자동 플레이북 -> MITRE ATT&CK 매핑 보고서 자동화

- **📢 섹션 요약 비유**: 사고 대응은 응급실(Emergency Room)과 같다. "정보가 빨리 사라지는 순서"대로 진찰하고(Live Triage), 환부를 채증(Biopsy)하여 진단(Attribution) 후 치료(Recovery)한다.

---

## Ⅱ. 아키텍처 및 핵심 원리

IR 포렌식의 핵심 원리는 **휘발성 순서(Order of Volatility, RFC 3227)**와 **무결성 보전(Integrity Preservation)**의 2축이다. 운영 중단(Production Outage)을 최소화하면서도 증거 인용 가능성이 있는 자료를 수집해야 한다.

```text
+----------------------------------------------------------------------+
|        Incident Response Forensics Architecture (Modern EDR-Native)  |
|                                                                       |
|  +--------------+    +-----------------+   +----------------------+ |
|  |  Tier-1 SoC  |---->|  IR Orchestrator |--->|  Forensic Backbone   | |
|  | (Detection)  |    |  (SOAR: Tines,  |   |  - Velociraptor      | |
|  |  Splunk/QR   |    |   XSOAR, Splunk |   |  - KAPE               | |
|  |  Sentinel    |    |   SOAR)         |   |  - CyLR/PEASS         | |
|  +--------------+    +-----------------+   |  - PowerForensics     | |
|            |                                |  - DFIR-ORC           | |
|            v                                +----------+-----------+ |
|  +----------------------+                              |             |
|  |   Endpoint Layer     |  EDR Agent (MDE, S1, CrowdStrike)            |
|  |  +----------------+  |                              |             |
|  |  | Live Response  |--+---> Memory Dump + Disk Image |             |
|  |  | Memory: 0-300s |  |   (to Remote Collector)      |             |
|  |  +----------------+  |                              |             |
|  +----------------------+                              |             |
|                                                          v             |
|  +-----------------------------------------------------------------+  |
|  |            Forensic Storage & Analysis Pipeline                |  |
|  |  +------------+   +-------------+   +---------------------+   |  |
|  |  | Acquisition|--->| Preservation |--->|  Analysis Engine    |   |  |
|  |  |  FTK Imager|   |  Hash SHA256 |   |  - Autopsy/Sleuth   |   |  |
|  |  |  X-Ways    |   |  E01/AFF4    |   |  - Volatility 3     |   |  |
|  |  |  Guymager  |   |  WORM Storage|   |  - Plaso/Log2t      |   |  |
|  |  +------------+   +-------------+   |  - Timeline Explorer |   |  |
|  |                                      +---------------------+   |  |
|  +-----------------------------------------------------------------+  |
|                                    |                                   |
|                                    v                                   |
|                          +------------------+                          |
|                          |  Report & TTPs   |                          |
|                          |  MITRE ATT&CK    |                          |
|                          |  Navigator       |                          |
|                          +------------------+                          |
+----------------------------------------------------------------------+
```

### 핵심 수집 우선순위 (RFC 3227 Order of Volatility)

| 우선순위 | 대상 | 평균 휘발 시간 | 수집 도구 |
| :--- | :--- | :--- | :--- |
| **P0** | CPU/Register, Cache | ns | Live Debugger (WinDbg) |
| **P1** | Routing Table, ARP Cache, Process List, Netstat | 1~10초 | netstat -ano, arp -a, tasklist |
| **P2** | Kernel Statistics, 환경변수, Mount Points, Scheduled Tasks | 10~60초 | WMIC, `systeminfo`, `schtasks` |
| **P3** | **Memory (RAM Full Dump)** | 수 분 | WinPmem, Magnet RAM Capture, LiME(Linux), AVML |
| **P4** | **Disk File System (Logical/Physical Image)** | 수 시간~일 | FTK Imager, X-Ways, dcfldd, `dd` |
| **P5** | 원격 로그(SIEM, Firewall, Proxy, VPN, DNS) | 수 일~수 주 | Splunk SPL, KQL, Zeek |
| **P6** | 물리적 환경(서버룸, USB, 케이블링) | 수 월 | 사진, 도면 |

| 구성 요소 | 역할 | 핵심 기술 및 동작 방식 |
| :--- | :--- | :--- |
| **Acquisition** | 비트 단위 복제(Disk/Image) | `dd if=/dev/sda bs=4M \| gzip` -> SHA-256 검증, E01(Expert Witness Format), AFF4(Advanced Forensic Format) 메타데이터 포함, 쓰기 차단기(Tableau, WiebeTech) 사용. 논리적(L logical partitions) vs 물리적(Physical bitstream) 수집 구분. |
| **Live Response** | 운영 중 휘발성 데이터 수집 | Velociraptor(VQL 기반), KAPE(Modules: Registry, Prefetch, EVTX, Amcache), PowerForensics(PowerShell NTFS 분석), CyLR(NTFS MFT/디렉터리 수집), DFIR-ORC. **원격 EDR API(MDE Live Response, S1 RTR) 우선 사용**, 미설치 시 USB 부팅(Knoppix, Caine, Paladin) |
| **Memory Forensics** | 메모리 덤프 분석 | Volatility 3 (Python3, OS Profile 자동 식별), Rekall(엔터프라이즈 통합), MemProcFS(FUSE 기반 가상 FS), R2 + Cutter GUI. 분석 대상: 프로세스 트리, Code Injection, Hooking, Unlinked DLL, Network Connection, Registry in Memory, AMSI/ETW 흔적 |
| **Disk Forensics** | 파일 시스템/아티팩트 분석 | Autopsy + The Sleuth Kit(TSK), X-Ways Forensics, FTK, EnCase. **Windows 아티팩트**: $MFT, $UsnJrnl, $LogFile, $Secure, Registry Hives(SAM/SECURITY/SOFTWARE/SYSTEM/NTUSER.DAT), Prefetch, Amcache, Shimcache, SRUM, BAM, Jumplist, LNK, Recycle Bin, Shadow Copy, Event Log(EVTX), Sysmon |
| **Timeline Analysis** | 초·밀리초 단위 통합 타임라인 | Plaso(`log2timeline`) -> 200+ 파서 -> 통합 timeline.csv -> Timesketch(협업 분석) 또는 Timeline Explorer. **Super-Timeline**은 5W1H(Who/What/When/Where/Why/How) 시각화 |
| **Threat Intel Correlation** | IoC/TTP 매핑 | MISP(Malware Information Sharing Platform), YARA 룰, Sigma 룰(SIEM 검색식), MITRE ATT&CK Navigator JSON, VirusTotal, Mandiant Advantage, KISA 보호나라·KrCERT |

### 핵심 알고리즘/파라미터

- **해시 알고리즘**: SHA-256(권장), SHA-1(과도기), MD5(충돌 취약, 보조용). NSRL(National Software Reference Library) 해시셋으로 Known Good/Unknown 파일 분류.
- **엔트로피 분석**: 7.0 이상 시 패킹/암호화 의심(예: UPX, VMProtect, XOR Loop).
- **YARA 패턴**: `PE Section Name`, `String Hash`, `API Sequence`, `Byte Sequence at Offset` 4종 결합. 메모리 전용(Memory-only) YARA는 `Volatility 3 -yara-scan` 플러그인 활용.
- **Carving**: 시그니처 기반(Header/Footer), 트리 구조(NTFS $I30 슬랙), 중복 제거 후 Assembly.

- **📢 섹션 요약 비유**: 포렌식은 "흔적을 따라가며 그림 맞추기"이다. 메모리(지금 이 순간), 디스크(어제), 로그(지난주) 순서로 퍼즐 조각을 모으면, 해커가 언제·어떤 문으로 들어왔는지 명확해진다.

---

## Ⅲ. 비교 및 연결

| 구분 | **전통적(Dead) 포렌식** | **EDR/클라우드 기반(Live) 포렌식** | **메모리 포렌식** |
| :--- | :--- | :--- | :--- |
| **데이터 소스** | 디스크 이미지(Offline) | EDR 원격 API, KAPE 원격 실행 | RAM Full Dump |
| **휘발성 보존** | 거의 불가(전원 OFF 후) | 가능(Live 프로세스) | 부분 가능 |
| **파일
## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 399 / 800

<- **이전**: [398. 랜섬웨어 대응 전략 백업 복구](/knowledge-base/studynote/12_it_management/05_security_compliance/398_ransomware_response_strategy_backup_recovery/)
**다음**: [400. 보안 아키텍처 디자인 원칙 심층 방어](/knowledge-base/studynote/12_it_management/05_security_compliance/400_security_architecture_defense_in_depth/) ->

---
