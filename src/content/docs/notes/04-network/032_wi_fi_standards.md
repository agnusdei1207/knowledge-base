---
sidebar:
  order: 32
  label: "032. Wi-Fi 표준"
  badge: { text: "기출 • 50%", variant: note }
title: "Wi-Fi 표준"
date: "2026-08-13T16:40:00+09:00"
tags: ["notes-network"]
weight: 32
extra:
  question_no: "032"
  source_status: "기출"
  source_history: "125회, 134회"
  priority: 50
  priority_note: "125•134회 출제"
---

## Ⅰ. 개요

<details><summary>용어 설명</summary>

- **IEEE 802.11(Institute of Electrical and Electronics Engineers 802.11)**: 무선 프레임 전송 및 무선 매체 제어 기술 표준 규격 계열이다.
- **접근점(Access Point, AP)**: 무선 단말을 유선 분배 시스템 및 외부 네트워크와 연결하는 중앙 무선 접속 장치이다.

</details>

- 정의/개념: 무선 LAN의 PHY•MAC을 규정하는 **IEEE 802.11**
- 배경/필요성: 제조사별 무선 규격으로는 **상호운용•매체 공유 불가**

#### 한줄 요약

- 단말•AP의 무선 매체 공유와 프레임 전송 표준

## Ⅱ. 특징

<details><summary>용어 설명</summary>

- **하위 호환성(Backward Compatibility)**: 신규 세대 무선 장비가 구형 표준 장비의 신호를 식별하여 상호 통신할 수 있는 호환 능력이다.
- **실효 처리량(Effective Throughput)**: 프로토콜 오버헤드, 프레임 충돌, 전파 간섭을 제외한 응용 계층의 실제 데이터 전송 속도이다.
- **기가헤르츠(Gigahertz, GHz)**: 무선 주파수의 초당 진동 횟수를 10억 단위로 나타내는 주파수 단위이다.

</details>

- **하위 호환성 유지**: 세대별 상위 표준 기기가 하위 기기와 공통 기능 및 변복조 방식을 협상하여 통신을 유지한다.
- **주파수 대역별 특성 분리**: 2.4GHz(회절성·범용성), 5GHz(광대역·고속), 6GHz(초광대역·무간섭) 대역별 전파 특성이 상이하다.
- **실효 처리량 한계**: 무선 매체 특성상 CSMA/CA 경합 및 프레임 오버헤드로 인해 이론상 최고 속도 대비 실효 속도가 감소한다.

#### 한줄 요약

- 주파수 특성과 경합 오버헤드가 실효 처리량 결정

## Ⅲ. 구조 및 구성요소

<details><summary>용어 설명</summary>

- **분배 시스템(Distribution System, DS)**: 복수의 AP를 유선 백본망과 상호 연결하여 무선 프레임을 라우팅하는 네트워크 논리 구조이다.

</details>

```text
무선 단말
│
무선 매체 (비인가 주파수 대역)
│
접근점 (Access Point, AP)
│
분배 시스템 (Distribution System, DS)
```

선의 의미: 무선 단말과 접근점(AP)이 무선 매체를 공유하고, AP가 분배 시스템(DS)을 통해 상위 유선 네트워크와 연결되는 토폴로지 구조이다.

| 구성요소 | 책임 |
|:---|:---|
| 무선 단말 | AP 탐색, 보안 인증, 무선 데이터 프레임 송수신 |
| 무선 매체 | 비인가 대역(2.4/5/6GHz) 전파 채널 제공 및 공유 |
| 접근점(AP) | 무선 단말 접속 관리, 프레임 변복조 및 매체 접근 제어 |
| 분배 시스템(DS) | 복수 AP 간 트래픽 중계 및 유선 백본망 연결 인터페이스 제공 |

#### 한줄 요약

- 단말•AP가 무선 매체를 공유하고 DS와 연결

## Ⅳ. 흐름도

<details><summary>용어 설명</summary>

- **비콘(Beacon Frame)**: AP가 SSID, 지원 레이트, 보안 정책, 동기화 정보를 주변에 주기적으로 브로드캐스팅하는 관리 프레임이다.
- **서비스 세트 식별자(Service Set Identifier, SSID)**: 무선 LAN 네트워크를 식별하기 위해 AP가 제공하는 32바이트 고유 명칭이다.
- **인증 요청 및 응답(Authentication Request/Response)**: 단말과 AP 간 보안 키 교환 전 신원을 입증하는 상호 절차이다.
- **결합 요청 및 응답(Association Request/Response)**: 단말과 AP 간 물리 속도, 채널 폭, 보안 옵션 등 통신 파라미터를 최종 확정하는 절차이다.

</details>

```text
접근점(AP): 1. 비콘 프레임 전송 (SSID 및 무선 설정 광고)
      |
      v
무선 단말: 2. 접속 인증 요청 (Authentication Request)
      |
      v
접근점(AP): 3. 접속 인증 응답 (Authentication Response)
      |
      +-- 인증 실패 ---- 접속 차단 및 종료
      |
      `-- 인증 성공
             |
             v
무선 단말: 4. 결합 요청 (Association Request)
             |
             v
접근점(AP): 5. 결합 응답 (Association Response)
             |
             `-- 접속 식별자(AID) 및 파라미터 확정 후 데이터 전송 시작
```

### 동작 원리

1. **비콘 전송**: AP가 SSID, 지원 속도, 보안 정책 등을 포함한 비콘 프레임을 주기적으로 방송한다.
2. **접속 인증 요청**: 단말이 AP에 인증 방식(Open, WPA3 등)에 맞춘 인증 프레임을 전달한다.
3. **접속 인증 응답**: AP가 신원 및 보안 정책을 검증한 후 승인 여부를 회신한다.
4. **결합 요청**: 단말이 실제 무선 속도, 채널 폭, 보안 파라미터를 교환하기 위해 결합 프레임을 송신한다.
5. **결합 응답**: AP가 접속 식별자(AID)를 부여하고 공통 기능을 확정하여 무선 접속을 개시한다.

#### 한줄 요약

- 비콘 탐색•인증•결합 후 무선 통신 개시

## Ⅴ. 종류 및 비교

<details><summary>용어 설명</summary>

- **Wi-Fi 5(IEEE 802.11ac)**: 5GHz 대역 중심의 VHT(Very High Throughput) 및 하향링크 MU-MIMO 기술을 도입한 세대이다.
- **Wi-Fi 6(IEEE 802.11ax)**: OFDMA 및 양방향 MU-MIMO를 통해 고밀도 환경의 자원 효율을 극대화한 세대이다.
- **Wi-Fi 6E(IEEE 802.11ax Extended)**: Wi-Fi 6 기술을 6GHz 청정 대역으로 확장한 주파수 확장 규격이다.
- **직교 주파수 분할 다중 접속(Orthogonal Frequency Division Multiple Access, OFDMA)**: 채널을 리소스 유닛(RU) 단위로 서브 분할하여 동시 다중 접속을 지원하는 기술이다.
- **목표 기상 시간(Target Wake Time, TWT)**: 단말의 무선 송수신 스케줄을 사전 예약하여 단말 소비 전력을 절감하는 기능이다.
- **Wi-Fi 7(IEEE 802.11be)**: 320MHz 초광대역, 4096-QAM, MLO 기술을 적용하여 극저지연 초고속을 구현한 세대이다.
- **다중 링크 동작(Multi-Link Operation, MLO)**: 2.4/5/6GHz 대역의 다중 무선 링크를 동시에 결합·전환하는 기술이다.
- **다중 입력 다중 출력(Multiple-Input Multiple-Output, MIMO)**: 다수의 안테나 공간 스트림을 이용하여 통신 용량 및 신호 품질을 높이는 기술이다.
- **메가헤르츠(Megahertz, MHz)**: 무선 채널의 주파수 대역폭 크기를 나타내는 단위이다.

</details>

| 무선 LAN 세대 | **Wi-Fi 5 (802.11ac)** | **Wi-Fi 6/6E (802.11ax)** | **Wi-Fi 7 (802.11be)** |
|:---|:---|:---|:---|
| 주요 지원 대역 | 5GHz 전용 | 2.4GHz, 5GHz, 6GHz (6E) | 2.4GHz, 5GHz, 6GHz |
| 변조 기술 | 256-QAM | 1024-QAM | 4096-QAM |
| 최대 채널 폭 | 160MHz | 160MHz | 320MHz |
| 다중 접속 기술 | DL MU-MIMO | OFDMA, UL/DL MU-MIMO | Multi-RU OFDMA, 16x16 MU-MIMO |
| 핵심 특화 기능 | 5GHz 고속 전송 | TWT (전력 절감), BSS Coloring | MLO (다중 링크 중계/집성) |

> 요약: 고밀도 트래픽 환경에는 Wi-Fi 6/6E, 초저지연·초고속 대용량 트래픽 환경에는 Wi-Fi 7을 선택.

#### 한줄 요약

- Wi-Fi 6은 고밀도, Wi-Fi 7은 MLO•320MHz 강화

## Ⅵ. 실무 고려사항 및 대책

<details><summary>용어 설명</summary>

- **공간 재사용(Spatial Reuse, BSS Coloring)**: 동일 채널 내 BSS 식별 태그를 부여하여 인접 AP 간 전파 간섭 문턱값을 조절하는 기술이다.
- **Wi-Fi 보호 접속 3(Wi-Fi Protected Access 3, WPA3)**: SAE(Simultaneous Authentication of Equals) 기반 사전 암호화 및 192비트 보안을 제공하는 무선 보안 표준 규격이다.

</details>

| 고려 항목 | 문제점 | 실무 대응 대책 | 기대 효과 |
|:---|:---|:---|:---|
| 채널 간섭 | 인접 AP 간 동일 채널 채택으로 무선 충돌 급증 | 공간 재사용(BSS Coloring) 및 셀 크기 조정 | 동일 채널 전파 간섭 최소화 및 셀 용량 증대 |
| 보안 취약성 | WPA2 사전 공유 키(PSK)의 dictionary 공격 취약 | WPA3 Enterprise/SAE 적용 및 무선 IDS 연동 | 무선 섹션 암호화 강화 및 무단 접속 차단 |
| 단말 믹스 환경 | 구형 legacy 단말 점유로 전체 통신 속도 저하 | 대역 분리(Band Steering) 및 최저 송신 속도 제한 | 신형 단말 전송 기회 보장 및 네트워크 실효 속도 향상 |
| 셀 로밍 지연 | 이동 단말의 로밍 지연에 따른 음성/영상 끊김 | 802.11r(Fast Roaming) 및 802.11k/v 활성화 | AP 간 전환 지연 시간 50ms 이내 보장 |

#### 한줄 요약

- BSS Coloring•WPA3•고속 로밍으로 품질 확보

## Ⅶ. 결론

<details><summary>용어 설명</summary>

- **Wi-Fi 세대 선택(Wi-Fi Generation Selection)**: 접속 단말 밀도, 데이터 용량, 지연 시간, 주파수 대역 환경을 고려해 적합한 무선 LAN 표준 규격을 선정하는 의사결정 프로세스이다.

</details>

- 고밀도망은 **Wi-Fi 6**, 초고속•저지연은 **Wi-Fi 7** 선택

#### 한줄 요약

- 단말 밀도•지연•대역에 따라 Wi-Fi 세대 선택
