---
sidebar:
  order: 40
  label: "040. NSSAI•NSI•NSSI"
  badge: { text: "기출 • 50%", variant: note }
title: "네트워크 슬라이스 식별 체계"
date: "2026-08-13T16:56:00+09:00"
tags: ["notes-network"]
weight: 40
extra:
  question_no: "040"
  source_status: "기출"
  source_history: "137회"
  priority: 50
  priority_note: "137회 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **네트워크 슬라이스 선택 지원 정보(Network Slice Selection Assistance Information, NSSAI)**: 단말 접속 시 원하는 5G 가상 슬라이스를 지정하거나 허용받기 위해 주고받는 식별자 집합이다.
- **네트워크 슬라이스 인스턴스(Network Slice Instance, NSI)**: 특정 서비스 SLA를 충족시키기 위해 생성된 종단(End-to-End) 가상 네트워크 운용 객체이다.
- **네트워크 슬라이스 서브넷 인스턴스(Network Slice Subnet Instance, NSSI)**: 무선, 전송, 코어 등 개별 도메인 내에서 NSI를 구성하기 위해 실체화된 하위 가상 자원 객체이다.

</details>

- 정의/개념: **NSSAI, NSI, NSSI**는 5G 네트워크 슬라이싱 아키텍처의 식별 및 운용 핵심 체계로, 단말의 서비스 요청 식별자(**NSSAI/S-NSSAI**), 종단 가상망 운용 객체(**NSI**), 무선/전송/코어 영역별 하위 자원 객체(**NSSI**) 간 바인딩 구조를 정의한다.
- 배경/필요성: 가입자 단말이 요구하는 서비스 식별자를 실제 무선, 전송, 코어망의 가상 인프라 자원 및 인스턴스와 일관되게 연결하고 수명주기를 관리하기 위해 제정되었다.

#### 한줄 요약

- 슬라이스 요청 식별자(NSSAI)를 종단 가상망 인스턴스(NSI) 및 영역별 하위 인스턴스(NSSI)로 연동 매핑하는 5G 슬라이싱 식별·운용 체계.

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **단일 네트워크 슬라이스 선택 지원 정보(Single Network Slice Selection Assistance Information, S-NSSAI)**: 하나의 표준화된 슬라이스를 유일하게 식별하는 32비트 제어 식별자 파라미터이다.
- **슬라이스·서비스 유형(Slice/Service Type, SST)**: eMBB(1), URLLC(2), mMTC(3) 등 5G 표준 슬라이스 서비스 특성을 나타내는 8비트 구별자이다.
- **슬라이스 구분자(Slice Differentiator, SD)**: 동일한 SST 서비스 내에서 사업자별, 고객별 개별 슬라이스를 세부 구별하기 위한 24비트 추가 식별자이다.

</details>

- **S-NSSAI 구조 표준화**: SST(8bit)와 SD(24bit)의 결합으로 구성되며, 단말당 최대 8개의 S-NSSAI를 포함하는 Requested/Allowed NSSAI를 운용한다.
- **계층적 인스턴스 구조**: 1개의 종단 NSI는 무선(RAN NSSI), 전송(Transport NSSI), 코어(Core NSSI) 등 복수의 하위 NSSI 결합으로 실체화된다.
- **자원 유연성 및 공유성**: NSSI는 특정 NSI 전용으로 할당(Dedicated)되거나, 효율성을 위해 타 NSI 간에 공유(Shared)되어 배정될 수 있다.

#### 한줄 요약

- SST+SD 결합 구조의 S-NSSAI 식별자를 기반으로 종단 NSI와 영역별 NSSI 하위망을 조립·격리·공유 운용.

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **네트워크 슬라이스 선택 기능(Network Slice Selection Function, NSSF)**: 가입자의 S-NSSAI 식별자를 분석하여 접속할 NSI 매핑 정보를 AMF에 회신하는 코어 NF이다.
- **접속·이동성 관리 기능(Access and Mobility Management Function, AMF)**: 단말의 NAS 요청 메시지에서 NSSAI를 수신하고 NSSF와 연동하여 슬라이스 접속을 처리하는 NF이다.

</details>

```text
네트워크 슬라이스 식별 및 인스턴스 계층 아키텍처
├─ 서비스 제어 및 선택 계층 (Control & Selection Layer)
│  ├─ 단일 슬라이스 선택 지원 정보 (S-NSSAI = SST + SD)
│  ├─ 슬라이스 선택 정보 집합 (NSSAI / Requested / Allowed)
│  └─ 접속 관제 및 슬라이스 선택 (AMF / NSSF)
└─ 종단 가상 인스턴스 운용 계층 (End-to-End Instance Layer)
   └─ 종단 네트워크 슬라이스 인스턴스 (NSI)
      ├─ 무선망 슬라이스 서브넷 (RAN NSSI)
      ├─ 전송망 슬라이스 서브넷 (Transport NSSI)
      └─ 코어망 슬라이스 서브넷 (Core NSSI)
```

선의 의미: 제어 계층의 S-NSSAI/NSSAI 식별자가 AMF와 NSSF를 통해 종단 NSI 및 무선, 전송, 코어 도메인의 NSSI 하위 인스턴스로 동적 바인딩되는 아키텍처 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| S-NSSAI (SST + SD) | 8비트 SST(eMBB/URLLC/mMTC)와 24비트 SD를 결합하여 개별 슬라이스를 유일하게 식별 |
| NSSAI (Requested/Allowed) | 단말이 연결 요청 시 제출하는 Requested NSSAI 및 망이 인가한 Allowed NSSAI 목록 관리 |
| AMF / NSSF | 단말 접속 시 Requested S-NSSAI를 수신하고 NSSF 조회를 통해 접속할 NSI 매핑 회신 |
| 종단 NSI (Network Slice Inst.) | SLA를 충족시키기 위해 3대 영역 NSSI를 총괄 통합한 E2E 가상 네트워크 객체 |
| 무선 NSSI (RAN Subnet Inst.) | 기지국 PRB 자원, 무선 베어러(DRB) 및 RRM 기능을 수용하는 무선 하위 객체 |
| 전송 NSSI (TN Subnet Inst.) | 프론트홀/백홀 패킷 라우팅 및 FlexE/SRv6 가상 유선 채널을 보장하는 전송 하위 객체 |
| 코어 NSSI (Core Subnet Inst.) | AMF, SMF, UPF 등 가상화된 코어망 NF 인스턴스를 수용하는 코어 하위 객체 |

#### 한줄 요약

- S-NSSAI 식별자를 기반으로 AMF와 NSSF가 접속을 중계하고 종단 NSI와 3대 도메인 NSSI가 조립 결합되는 계층 구조.

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **NSI 매핑(NSI Mapping)**: 수신된 S-NSSAI를 기반으로 가입자 프로필과 위치 조건을 대조하여 대상 NSI를 검색하는 알고리즘이다.
- **NSSI 조합(NSSI Composition)**: 대상 NSI를 구동하기 위해 필요한 도메인별 NSSI의 가용 상태를 검증하고 통합 연동하는 절차이다.

</details>

```text
1. 단말(UE)의 Requested NSSAI 요청 전송 (RRC / NAS Registration)
      │
      v
2. AMF -> NSSF: 가입자 프로필 및 위치 정보 전달 (Slice Selection Request)
      │
      v
3. NSSF: S-NSSAI 대비 가용 NSI 매핑 조회 (NSI Mapping Lookup)
      │
      ├─ 매핑 실패 ---- 요청 거절 (Registration Reject)
      └─ 매핑 성공
            │
            v
      4. 무선/전송/코어 NSSI 하위 자원 결합 상태 확인 (NSSI Assembly)
            │
            v
      5. Allowed NSSAI 및 전용 NSI 바인딩 정보 반환 및 PDU 세션 확립
```

### 동작 원리

1. **단말(UE)의 Requested NSSAI 요청 전송**: S-NSSAI 전달
2. **AMF -> NSSF: 가입자 프로필 및 위치 정보 전달**: 선택 요청
3. **NSSF: S-NSSAI 대비 가용 NSI 매핑 조회**: 정책 대조
4. **무선/전송/코어 NSSI 하위 자원 결합 상태 확인**: 상태 검증
5. **Allowed NSSAI 및 전용 NSI 바인딩 정보 반환**: 세션 확립

#### 한줄 요약

- 단말의 S-NSSAI 요청 수신, NSSF의 NSI 매핑 조회, 영역별 NSSI 조합 확인 및 Allowed NSSAI 회신을 통한 세션 연결 절차.

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **가입·지역 정보 전달(Registration & Location Provisioning)**: AMF가 NSSF에 접속 단말의 위치와 가입 정보를 전달하는 세션 제어 절차이다.

</details>

| 슬라이스 구분 | **NSSAI (S-NSSAI)** | **NSI (Network Slice Instance)** | **NSSI (Slice Subnet Instance)** |
|:---|:---|:---|:---|
| 핵심 개념 | 5G 슬라이스를 식별하는 32bit 제어 파라미터 | 엔드투엔드(E2E) 가상 네트워크 운용 객체 | 무선/전송/코어 각 영역별 가상 자원 객체 |
| 구성 형태 | SST (8bit) + SD (24bit) 결합 코드 | 1개 이상의 RAN, TN, Core NSSI 통합체 | NFV VNF/CNF, PRB, FlexE 채널 자원 묶음 |
| 주요 역할 | 단말 접속 요청 식별 및 NSSF 매핑 | 서비스 SLA 목표와 E2E 트래픽 수용 | 도메인별 자원 제어 및 독립•공유 할당 |
| 관리 주체 | 단말(UE), AMF, NSSF (제어 평면) | NSMF (Network Slice Management Func.) | NSSMF (Slice Subnet Management Func.) |

> 요약: NSSAI는 식별 코드, NSI는 E2E 가상망 실체, NSSI는 도메인별 자원 조립 단위.

#### 한줄 요약

- NSSAI로 요청 식별, NSI로 E2E 가상망 운용, NSSI로 도메인별 가상 자원 조립 수행.

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **고아 자원(Orphan Resource)**: 상위 NSI 인스턴스가 해제되었음에도 수명주기 통제 실패로 회수되지 않고 잔류하는 NSSI 자원이다.
- **매핑 불일치(Mapping Mismatch)**: S-NSSAI 식별자와 NSI/NSSI 매핑 테이블 설정 오차로 접속에 실패하는 오류 현상이다.
- **서비스 수준 협약(Service Level Agreement, SLA)**: 슬라이스가 고객에게 약속한 최저 보장 성능 지표 수치이다.

</details>

| 문제점 | 발생 원인 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| S-NSSAI 매핑 오차 | 코어망 NSSF와 로밍 망 간 S-NSSAI 매핑 설정 불일치 | NSSF 매핑 테이블 자동화 및 3GPP 표준 SST 바인딩 | 로밍 및 타사 슬라이싱 접속 실패 예방 |
| NSSI 고아 자원 발생 | NSI 삭제 시 하위 NSSI 인스턴스 수명주기 회수 누락 | 오케스트레이터(NSMF-NSSMF) 간 자원 연쇄 회수 자동화 | 불필요 자원 점유 차단 및 인프라 효율성 향상 |
| 동일 S-NSSAI 품질 변동 | 지역별 NSI 및 무선 NSSI 자원 수용 한계 직면 | AI 기반 Closed-loop NSI 자원 오토스케일링 적용 | 전 지역 동일한 SLA 지속 유지 |
| S-NSSAI 오남용 보안 | 불인가 단말의 특수 S-NSSAI(URLLC) 위장 접속 시도 | NSSF 및 UDM 가입자 2차 슬라이스 인가(Secondary Auth) | 불법 인가 슬라이스 접속 원천 차단 |

#### 한줄 요약

- NSSF 매핑 테이블 자동화, NSSMF 오케스트레이션을 통한 고아 자원 회수, 도메인별 SLI 모니터링으로 슬라이싱 체계 안정화.

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **슬라이스 가용성(Slice Availability)**: NSSF가 S-NSSAI 요청을 수신했을 때 이에 대응하는 NSI와 NSSI 자원이 정상 가동되어 즉시 할당 가능한 상태이다.

</details>

- 접속 선택은 **NSSAI**, E2E 운용은 **NSI•NSSI**로 관리

#### 한줄 요약

- S-NSSAI 식별 체계 확립 및 NSI/NSSI 동적 오케스트레이션 자동화 체계 구현 필수.
