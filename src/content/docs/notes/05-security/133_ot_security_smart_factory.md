---
sidebar:
  order: 133
  label: "133. 스마트팩토리 OT 보안 (OT Security Smart Factory)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "산업제어시스템 및 스마트팩토리 운영기술 보안 : OT 보안 (IEC 62443 & NIST SP 800-82)"
date: "2026-08-22T08:15:00+09:00"
tags:
  - "notes-security"
weight: 133
extra:
  question_no: "133"
  source_status: "기출"
  source_history: "126회"
  priority: 70
  priority_note: "126회 기출, 스마트팩토리 및 산업제어시스템(ICS/OT) 보안, Purdue 모델 계층화(Level 0~5), IEC 62443(영역 Zone & 통로 Conduit, 목표 보안수준 SL-T), IT(기밀성 중심) vs OT(안전성/가용성/실시간성 중심) 비교, 보상 통제(Compensating Control) 및 정비창(Maintenance Window) 패치 관리, NIST SP 800-82"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **스마트팩토리 OT 보안(Operational Technology Security / IEC 62443 & NIST SP 800-82)**: 발전소, 플랜트, 제조 스마트 공장에서 물리적 공정 설비(로봇 암, 터빈, 화학 반응기)를 제어하는 센서(Level 0), PLC/DCS(Level 1), SCADA/HMI(Level 2), MES(Level 3)로 구성된 산업제어시스템(ICS)을 사이버 위협과 랜섬웨어로부터 보호하고, 물리적 안전성(Safety)과 고가용성(Availability)을 보증하는 보안 체계.
- **IT 중심 보안 적용 시 공정 중단 및 물리적 폭발 결함(IT-OT Cultural Gap Defect)**: 일반 사무용 IT 환경처럼 무중단 가동 중인 PLC나 SCADA 서버에 사전 검증 없는 일괄 백신 패치나 방화벽 세션 리셋을 적용할 경우, 제어 패킷의 수 ms 지연(Latency)이나 프로세스 크래시로 인해 공정 라인이 전면 멈추거나 압력 밸브 오작동으로 대형 물리적 폭발 사고로 직결되는 구조적 결함.

</details>

- 정의/개념: 인명 안전과 생산 연속성을 보증하기 위해 **Purdue 엔터프라이즈 모델 기반 6계층 격리 $\rightarrow$ IEC 62443 영역(Zone) 및 통로(Conduit) 분할 $\rightarrow$ 산업 비무장지대(IDMZ Level 3.5) 중계 $\rightarrow$ 패치 불가 레거시 장비에 대한 보상 통제(Compensating Control) $\rightarrow$ 정비창(Maintenance Window) 기반 안전한 패치 배포** 를 집행하는 **산업 공정 복원력 아키텍처**
- 배경/필요성: IT-OT 융합 및 IIoT(산업용 사물인터넷) 확산으로 폐쇄망이었던 공장 제어망이 인터넷 및 클라우드에 연결됨에 따라, 랜섬웨어(Stuxnet, BlackEnergy) 감염 및 국가 기간시설 테러 위협에 대한 글로벌 표준 보안 프레임워크 요구

#### 한줄 요약
- IEC 62443 표준과 Purdue 모델 6계층 분할을 통해 안전성(Safety)과 고가용성 중심의 OT 보안을 확립한다.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **OT 보안의 3대 핵심 설계 원칙**:
  - **Safety & Availability 1순위 (AIC 모델)**: 데이터 기밀성(C)보다 물리적 인명 안전(Safety), 무중단 가용성(A), 데이터 무결성(I)을 절대 최우선으로 통제.
  - **Zone & Conduit 모델 (IEC 62443-3-2)**: 동일한 보안 요구수준을 가진 자산을 '영역(Zone)'으로 묶고, 영역 간 통신은 엄격히 통제된 '통로(Conduit)' 방화벽만 허용.
  - **보상 통제 (Compensating Control)**: 20년 이상 노후화되어 OS 패치가 불가능한 레거시 PLC/Windows XP 장비에 대해 네트워크 물리 격리 및 화이트리스트 접근통제로 위험 상쇄.

</details>

- **결정론적 초저지연(Deterministic Real-time) 보장**: 통신 지연이 10ms 이내로 제한되는 산업용 이더넷(Modbus/TCP, Profinet, EtherCAT) 트래픽의 암호화 및 딥 패킷 인스펙션(DPI) 수행
- **심층 방어 Purdue 모델 (Levels 0~5)**: 기업 IT망(Level 4/5)과 공장 OT망(Level 0~3) 사이에 산업용 DMZ(IDMZ Level 3.5)를 구축하여 다이렉트 통신 원천 차단
- **독립된 안전 계장 시스템 (SIS: Safety Instrumented System)**: 해커가 SCADA/PLC를 완전 장악하더라도 물리적으로 독립된 SIS가 한계치 초과 시 비상 차단(Emergency Shutdown) 집행

#### 한줄 요약
- 가용성/안전성 최우선, IEC 62443 Zone/Conduit 분할, IDMZ 완충 격리, SIS 비상 인터락을 제공한다.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **Purdue 엔터프라이즈 레퍼런스 모델(PERA) 6계층 구조**:
  - **Level 5/4 (Enterprise IT)**: ERP, 이메일, 본사 사무 업무망 (인터넷 연결).
  - **Level 3.5 (Industrial DMZ)**: IT-OT 간 데이터 교환용 이중화 프록시, 패치 서버, 점프 호스트.
  - **Level 3 (Operations Control)**: MES(제조실행시스템), 공정 이력 저장 서버(Historian).
  - **Level 2 (Supervisory Control)**: SCADA 서버, HMI(Human Machine Interface) 콘솔.
  - **Level 1 (Basic Control)**: PLC(프로그래머블 로직 제어기), DCS 제어기, RTU.
  - **Level 0 (Physical Process)**: 모터, 밸브, 펌프, 온도/압력 센서 및 액추에이터.

</details>

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ [ Level 5/4: 기업 IT 엔터프라이즈 계층 (Enterprise IT Network) ]         │
│  └─ 본사 ERP, 메일 서버, 클라우드 AI 분석 ➔ [ 인터넷 직접 노출 영역 ]   │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (다이렉트 통신 100% 차단)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ Level 3.5: 산업 비무장지대 (Industrial DMZ / 완충 벙커 계층) ]         │
│  ├─ 데이터 다이오드(단방향 전송), 이중 인터페이스 점프 호스트           │
│  └─ [ OT 데이터 복제 서버(Historian Mirror) ➔ IT-OT 직접 트래픽 단절 ] │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (Conduit 통로: 엄격한 화이트리스트 DPI)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ Level 3: 공장 제조 운영 제어 계층 (Operations Control: MES) ]          │
│  └─ MES 생산 계획 스케줄러, 공정 데이터베이스(Historian Server)          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (산업용 방화벽 분할)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ Level 2: 원격 감시 제어 계층 (Supervisory Control: SCADA & HMI) ]     │
│  └─ SCADA 마스터 서버, HMI 엔지니어링 워크스테이션                      │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ (실시간 제어 필드버스 통신: Modbus/Profinet)
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ [ Level 1 & 0: 기본 물리 제어 및 센서 계층 (PLC / Sensor / Actuator) ]  │
│  ├─ [ Level 1 ] PLC / DCS 컨트롤러 ➔ 0.1초 단위 로직 연산              │
│  ├─ [ Level 0 ] 용광로, 모터 밸브, 온도 센서                            │
│  └─ [ 독립 물리망 ] ➔ 안전 계장 시스템 (SIS: Safety Instrumented System) │
└─────────────────────────────────────────────────────────────────────────┘
```

선의 의미: IT망과 OT망 사이에 IDMZ(3.5)를 배치하여 트래픽을 단절하고, 각 계층을 Zone과 Conduit으로 분할하여 Level 0/1 물리 설비를 보호하는 구조

| 계층 (Purdue Level) | 주요 설비 및 자산 | 핵심 보안 통제 기술 | 비고 |
|:---|:---|:---|:---|
| **Level 4/5 (IT망)** | ERP, 그룹웨어, 클라우드 SaaS | EDR, WAF, IPS, 계정 접근 통제 (IAM) | Enterprise |
| **Level 3.5 (IDMZ)** | 이중화 Historian, 점프 호스트, 패치 WSUS | 단방향 데이터 다이오드(Data Diode), MFA 프록시 | Isolation |
| **Level 3 (MES)** | 제조실행시스템(MES), 생산 스케줄러 | 롤백 가능한 백업 스냅샷, 자산 인벤토리 | Operations |
| **Level 2 (SCADA/HMI)**| SCADA 서버, HMI 터치스크린 콘솔 | USB 포트 물리 봉인, 애플리케이션 화이트리스트 | Supervisory |
| **Level 1 (PLC/DCS)** | PLC 제어기, 원격 단말 장치(RTU) | 산업용 제어 프로토콜 DPI 방화벽, 펌웨어 서명 | Basic Control |
| **Level 0 & SIS** | 센서, 밸브, 모터, 독립 SIS 비상 정지 | 에어갭(Air-gapped) 물리 분리, 하드웨어 인터락 | Process & Safety|

#### 한줄 요약
- Purdue 6계층(0~5), IDMZ Level 3.5 완충 격리, IEC 62443 Zone/Conduit 통로, SIS 비상 인터락으로 구성된다.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **OT 보안 패치 및 변경 관리 5단계 수명주기**:
  1. IEC 62443 기반 공장 설비 자산 식별 및 취약점 평가
  2. 오프라인 디지털 트윈 테스트베드에서 패치 호환성 및 실시간성 사전 검증
  3. 패치 불가 레거시 장비에 대한 보상 통제(네트워크 격리/DPI) 적용
  4. 주말/야간 계획된 정비창(Maintenance Window)에 단계적 패치 배포
  5. 롤백 시나리오 확보 및 공정 무결성 모니터링

</details>

```text
1. [OT 자산 식별 및 위험 평가]
    ├─ 공장 내 500대 PLC/SCADA 자산 인벤토리 및 펌웨어 버전 전수 조사
    └─ [IEC 62443-3-2 기반 영역(Zone) 분할 및 목표 보안수준(SL-T 3) 수립]
            │
            ▼
2. [오프라인 테스트베드 사전 검증]
    ├─ 실제 공정과 1:1 동일한 디지털 트윈(Digital Twin) 복제 가상망 구축
    ├─ 신규 OS 보안 패치 적용 ➔ Modbus/TCP 제어 패킷 응답 지연(Latency) 실측
    └─ [지연시간 5ms 이하 및 공정 에러 0건 확인 ➔ 현장 배포 승인]
            │
            ▼
3. [보상 통제(Compensating Control) 수립]
    ├─ (패치 불가능한 구형 Windows XP HMI 장비 식별)
    └─ [HMI 전면에 산업용 DPI 방화벽 배치 ➔ 허용된 PLC 쓰기 명령 외 전면 차단]
            │
            ▼
4. [정비창(Maintenance Window) 단계적 배포]
    ├─ 공장 가동이 중단되는 주말 심야(일요일 01:00~04:00) 정비창 진입
    ├─ 현장 제어 관리자 입회 하에 1개 조립 라인씩 순차적 패치 적용
    └─ [이상 발생 시 즉각 1분 내 복구 가능한 이전 펌웨어 백업 롤백 준비]
            │
            ▼
5. [공정 가동 및 이상 징후 관제]
    ├─ 라인 재가동 ➔ 산업용 IDS(OT 패킷 미러링)로 비인가 제어 명령 실시간 감시
    └─ [이상 트래픽 미발생 확인 ➔ 정비창 종료 및 MES 정상 가동 확정]
```

**동작 원리**

1. **가용성 중심 사전 검증**: 라이브 공정에 패치를 즉시 적용하지 않고 오프라인 테스트베드에서 100% 가동성 검증
2. **비침습적 수동 관제**: OT 망에 부하를 주지 않기 위해 스위치 SPAN/TAP 포트 기반의 비침습적 수동형(Passive) 패킷 미러링 분석 적용
3. **엄격한 프로토콜 화이트리스트**: Modbus Function Code(예: Read Only 0x03 허용, Write 0x05 차단) 레벨까지 DPI 심층 필터링
4. **점진적 롤아웃과 즉시 가역성**: 1개 라인 단위로 순차 적용하며 실패 시 즉각 이전 펌웨어 이미지로 롤백
5. **물리적 안전망 유지**: 사이버 제어망이 완전 붕괴되더라도 SIS 계장 시스템이 물리적 한계 임계치를 통제

#### 한줄 요약
- 자산 식별, 테스트베드 검증, 보상 통제 적용, 정비창 단계적 배포, 이상 관제 및 롤백 확보 순으로 동작한다.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **IT 보안 vs OT 보안 핵심 비교**:
  - IT 보안: 기밀성(Confidentiality) 최우선, 잦은 패치, 웜/바이러스 차단 중심.
  - OT 보안: 인명 안전(Safety) 및 가용성(Availability) 최우선, 결정론적 실시간성, 패치 지연성.

</details>

| 비교 항목 | 기업 IT 보안 (Enterprise IT) | 산업제어 OT 보안 (Industrial OT) |
|:---|:---|:---|
| **최우선 목표** | **기밀성 (Confidentiality) ➔ 무단 유출 방지**| **안전성(Safety) & 가용성(Availability) ➔ 공정 유지** |
| **운영 중단 허용** | 수 분 ~ 수 시간 장애 허용 (재부팅 가능) | **0초 (수 초 중단 시 수십억 원 손실 및 폭발 위험)**|
| **실시간성 요구** | 수 초 (지연 허용, Best-effort) | **수 ms ~ 수십 ms (결정론적 Deterministic 요구)** |
| **패치 주기** | 정기/수시 자동 업데이트 (매주/매월) | **수개월~수년 단위 계획된 정비창(정기 보수)에만 수행**|
| **자산 수명주기** | 3 ~ 5년 (빈번한 교체) | **15 ~ 30년 (노후화된 레거시 시스템 다수 잔존)** |
| **주요 적용 표준** | ISO/IEC 27001, ISMS-P, NIST CSF | **IEC 62443, NIST SP 800-82, ISA-99** |

#### 한줄 요약
- IT는 기밀성 중심의 빈번한 패치, OT는 안전성/가용성 중심의 결정론적 실시간성 및 정비창 통제이다.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **IEC 62443 (IACS 보안 표준) 및 NIST SP 800-82 (ICS 보안 가이드)**: 산업자동화제어시스템 전주기 보안 및 IT-OT 융합 환경 구축 가이드라인.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 공장 내 IT망과 OT망이 단일 평면(Flat) 네트워크로 연결되어 **사무실 랜섬웨어가 1초 만에 공장 PLC 라인으로 확산되어 전 공장 셧다운 마비** | **Purdue 모델 기반 Level 3.5 IDMZ를 구축하고, IEC 62443-3-2 Zone & Conduit 분할 및 단방향 데이터 다이오드 적용** | IT 발 랜섬웨어의 OT 제어망 침투 100% 원천 차단 |
| 20년 된 레거시 Windows XP HMI 및 노후 PLC에 보안 패치 적용 시 **호환성 충돌로 인한 블루스크린 크래시 및 공정 폭발 위험 발생** | **패치 대신 산업용 방화벽 기반의 보상 통제(Compensating Control)를 적용하고 화이트리스트 Modbus DPI 제어 통제 구현** | 설비 가용성 100% 유지 및 레거시 취약점 완벽 상쇄 |
| OT 환경에 액티브 네트워크 스캐닝 툴(Nmap 등)을 구동하여 **민감한 PLC 통신 스택 오작동으로 인한 설비 다운 장애 발생** | **SPAN/TAP 기반의 비침습적 수동형(Passive) OT 네트워크 트래픽 미러링 및 이상 행위 분석 솔루션(Nozomi, Claroty) 도입** | 제어망 패킷 부하 0% 및 실시간 침해 위협 탐지 달성 |

#### 한줄 요약
- IDMZ로 랜섬웨어 전파를 막고, 보상 통제로 레거시 설비를 보호하며, 수동형 미러링으로 무부하 관제를 달성한다.

## Ⅶ. 결론

- 국가 핵심 기간시설과 스마트 제조 생태계의 실질적 안전성을 좌우하는 **스마트팩토리 OT 보안 아키텍처**는 물리 세계와 사이버 세계를 아우르는 절대적 방어 체계이며, 실무 구현 시 **IEC 62443 및 NIST SP 800-82 국제 표준 기반의 거버넌스 확립**, **Purdue Level 3.5 IDMZ를 통한 IT-OT 완전 분리**, **레거시 자산에 대한 화이트리스트 기반 보상 통제(Compensating Control) 내재화**, **정비창(Maintenance Window) 중심의 가용성 보장 패치 관리 체계 구축**을 통합 완성하여 최고 수준의 산업 안전성과 생산 연속성을 완성

#### 한줄 요약
- IEC 62443 표준과 Purdue IDMZ 완충 격리 및 보상 통제를 통해 완벽한 스마트팩토리 OT 보안을 완성한다.
