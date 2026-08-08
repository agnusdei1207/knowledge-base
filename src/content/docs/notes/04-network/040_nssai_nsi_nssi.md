---
sidebar:
  order: 40
  label: "040. NSSAI•NSI•NSSI"
  badge: { text: "기출 • 50%", variant: note }
title: "네트워크 슬라이스 식별 체계"
date: "2026-08-06T23:27:50+09:00"
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

<details>
<summary>핵심 용어</summary>

- **네트워크 슬라이스 선택 지원 정보(Network Slice Selection Assistance Information, NSSAI)**: 단말이 요청하거나 망이 허용하는 슬라이스 식별자 목록이다.
- **네트워크 슬라이스 인스턴스(Network Slice Instance, NSI)**: 종단 서비스를 제공하는 논리망 운영 인스턴스이다.
- **네트워크 슬라이스 서브넷 인스턴스(Network Slice Subnet Instance, NSSI)**: NSI를 구성하는 영역별 하위망 인스턴스이다.

</details>

- 정의/개념: **NSSAI** 요청을 실제 **NSI**와 영역별 **NSSI**에 연결하는 체계이다.
- 배경/필요성: 식별자만으로는 실제 종단망을 선택할 수 없다.

#### 한줄 요약

- 요청 이름표를 실제 논리망과 하위망에 연결한다.

## Ⅱ. 특징

<details>
<summary>핵심 용어</summary>

- **단일 네트워크 슬라이스 선택 지원 정보(Single Network Slice Selection Assistance Information, S-NSSAI)**: 하나의 네트워크 슬라이스를 선택하는 식별자이다.
- **슬라이스•서비스 유형(Slice/Service Type, SST)**: 슬라이스의 서비스 유형을 나타내는 코드이다.
- **슬라이스 구분자(Slice Differentiator, SD)**: 같은 SST 내 슬라이스를 구분하는 선택 값이다.

</details>

- **SST**와 **SD**로 **S-NSSAI**를 구성한다.
- 가입•지역•가용성으로 NSI를 선택한다.
- 영역별 NSSI를 조립해 종단 NSI를 만든다.

#### 한줄 요약

- 같은 이름표도 지역과 정책에 따라 다른 망을 쓴다.

## Ⅲ. 구조 및 구성요소

<details>
<summary>핵심 용어</summary>

- **네트워크 슬라이스 선택 기능(Network Slice Selection Function, NSSF)**: 가입•지역•가용성을 바탕으로 요청에 맞는 네트워크 슬라이스를 선택하는 망 기능이다.
- **접속•이동성 관리 기능(Access and Mobility Management Function, AMF)**: 단말의 접속 정보를 받아 NSSF에 슬라이스 선택을 요청하는 망 기능이다.

</details>

```text
슬라이스 식별•인스턴스 구조
├─ 선택 정보
│  ├─ NSSAI
│  ├─ S-NSSAI(SST•SD)
│  └─ AMF•NSSF
└─ 종단 NSI
   ├─ 무선 NSSI
   ├─ 전송 NSSI
   └─ 코어 NSSI
```

가지의 의미: 선택 정보와 종단 NSI를 구성하는 영역별 NSSI의 소속을 뜻한다.

| 구성요소 | 책임 |
|:---|:---|
| NSSAI | **NSSAI**가 요청•허용 S-NSSAI 목록 제공 |
| S-NSSAI(SST•SD) | **S-NSSAI**가 서비스 유형과 슬라이스 구분자 결합 |
| AMF•NSSF | **AMF**가 요청하고 **NSSF**가 슬라이스 선택 |
| 종단 NSI | **NSI**가 서비스용 종단 논리망 제공 |
| 무선 NSSI | **NSSI**가 무선 접속 자원•기능 제공 |
| 전송 NSSI | NSSI가 영역 간 격리 경로 제공 |
| 코어 NSSI | NSSI가 세션•정책•사용자면 코어 기능 제공 |

#### 한줄 요약

- 종단 논리망은 영역별 하위망을 조립해 만든다.

## Ⅳ. 흐름도

<details>
<summary>핵심 용어</summary>

- **NSI 매핑**: 요청된 S-NSSAI를 조건에 맞는 NSI에 연결하는 과정이다.
- **NSSI 조합**: 영역별 NSSI를 연결해 종단 NSI를 구성하는 과정이다.
- **가입•지역 정보 전달**: AMF가 단말의 요청과 접속 조건을 NSSF에 제공하는 절차이다.
- **NSI 매핑 조회**: NSSF가 S-NSSAI와 조건에 맞는 종단망을 검색하는 절차이다.
- **NSSI 조합 구성**: 무선•전송•코어 하위망을 종단 NSI로 연결하는 절차이다.
- **NSI 가용 정보 제공**: 구성된 종단망의 지역과 정상 상태를 반환하는 절차이다.

</details>

```text
단말의 NSSAI 요청
        │
        ▼
1. 가입•지역 정보 전달
        │
        ▼
2. NSI 매핑 조회
        ├─ 매핑 없음: 요청 거절
        └─ 매핑 있음
              │
              ▼
3. NSSI 조합 구성
              │
              ▼
4. NSI 가용 정보 제공
              ├─ 사용 불가: 대체 NSI 조회
              └─ 사용 가능: 허용 S-NSSAI•NSI 반환
```

### 동작 원리

1. **가입•지역 정보 전달**: AMF가 단말 요청과 접속 정보를 NSSF에 제공한다.
2. **NSI 매핑 조회**: **NSI 매핑**으로 S-NSSAI에 맞는 종단망을 검색한다.
3. **NSSI 조합 구성**: **NSSI 조합**으로 무선•전송•코어 하위망을 연결한다.
4. **NSI 가용 정보 제공**: 구성된 종단망의 지역•상태 정보를 반환한다.

#### 한줄 요약

- 이름표가 있어도 가용한 실제 망이 필요하다.

## Ⅴ. 종류 및 비교

| 슬라이스 단위 | 역할 | 상호 관계 |
|:---|:---|:---|
| **NSSAI** | 접속 요청의 슬라이스 식별•선택 | 단말 요청을 허용 NSI로 매핑 |
| **NSI** | 종단 논리망 서비스 운영 | 하나 이상의 NSSI로 구성 |
| **NSSI** | 영역별 하위망 기능 제공 | 여러 NSI가 공유 가능 |

> 요약: NSSAI로 슬라이스를 선택하고 NSI를 NSSI 조합으로 운영이 핵심이다.

#### 한줄 요약

- 목록에서 고른 이름을 실제 논리망에 연결한다.

## Ⅵ. 실무 고려사항 및 대책

<details>
<summary>핵심 용어</summary>

- **고아 자원**: 상위 NSI와 연결이 끊긴 채 남은 NSSI 또는 자원이다.
- **매핑 불일치**: 허용 S-NSSAI가 의도한 NSI와 연결되지 않는 오류이다.
- **서비스 수준 협약(Service Level Agreement, SLA)**: 지역별 NSI가 보장해야 할 지연•용량•가용성 목표와 책임을 정한 협약이다.

</details>

| 문제 | 대책 | 효과 |
|:---|:---|:---|
| 가입•지역 **매핑 불일치** | S-NSSAI 허용표 자동 대조 | 오접속 방지 |
| NSI•NSSI 수명주기 단절 | 종단•도메인 인스턴스 연결 관리 | **고아 자원** 방지 |
| 동일 식별자의 품질 편차 | 지역별 NSI•**SLA** 지표 검증 | 서비스 일관성 확보 |

#### 한줄 요약

- 같은 식별 정보가 지역별로 의도한 종단 논리망에 연결되는지 확인한다.

## Ⅶ. 결론

<details>
<summary>핵심 용어</summary>

- **슬라이스 가용성**: 요청 S-NSSAI에 대응하는 NSI와 NSSI의 정상 제공 상태이다.

</details>

- **슬라이스 가용성**과 가입•지역 매핑이 일치하면 **S-NSSAI** 요청을 허용한다.

#### 한줄 요약

- 단말의 이름표가 가입과 지역에 맞는 실제 종단망과 하위망으로 이어지는지 확인해야 한다.
