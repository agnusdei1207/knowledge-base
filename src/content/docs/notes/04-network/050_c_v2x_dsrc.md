---
sidebar:
  order: 50
  label: "050. C-V2X와 DSRC 비교 (C-V2X DSRC)"
  badge:
    text: "기출 · 30%"
    variant: note
title: "C-V2X와 DSRC 비교 (C-V2X DSRC)"
date: "2026-07-31T10:59:30+09:00"
tags:
  - "notes-network"
weight: 50
extra:
  question_no: "050"
  source_status: "기출"
  source_history: "138회"
  priority: 30
  priority_note: "비교형: 138회 C-V2X·DSRC 구성축"
---

## 미리 알고가기

- **셀룰러 차량사물통신(Cellular Vehicle-to-Everything, C-V2X)**: 3GPP 규격으로 차량 직접 통신과 이동통신망 경유 통신을 제공하는 기술
- **전용 단거리 통신(Dedicated Short-Range Communications, DSRC)**: IEEE 802.11p 계열의 차량 단거리 통신 기술
- **차량사물통신(Vehicle-to-Everything, V2X)**: 차량이 주변 대상·통신망과 주행 정보를 교환하는 통신 체계
- **3세대 파트너십 프로젝트(3rd Generation Partnership Project, 3GPP)**: LTE·5G 이동통신 규격을 제정하는 표준화 단체
- **전기전자공학자협회(Institute of Electrical and Electronics Engineers, IEEE)**: 802 계열 통신 표준을 제정하는 전문 단체
- **차량 환경 무선 접속(Wireless Access in Vehicular Environments, WAVE)**: IEEE 802.11p와 1609 계열로 구성된 차량 통신 체계
- **기본 서비스 집합 외부(Outside the Context of a Basic Service Set, OCB)**: 기본 서비스 집합 가입 절차 없이 차량이 데이터 프레임을 교환하는 방식
- **충돌 회피 반송파 감지 다중접속(Carrier Sense Multiple Access with Collision Avoidance, CSMA/CA)**: 채널 감지와 임의 대기로 동시 전송 충돌을 줄이는 접속 방식
- **PC5·Uu 인터페이스**: PC5는 차량끼리 직접 통신하고 Uu는 기지국 경유 통신에 쓰이는 3GPP 참조점
- **사이드링크(Sidelink)**: 이동통신 단말끼리 기지국을 통과하지 않고 직접 데이터를 교환하는 링크
- **차량 탑재 장치(On-Board Unit, OBU)·노변 장치(Roadside Unit, RSU)**: 차량과 도로 주변에서 각각 안전 메시지를 송수신하는 장치
- **공개키 기반구조(Public Key Infrastructure, PKI)**: 인증서와 공개키로 송신자 신원과 메시지 서명을 검증하는 체계
- **5G 기지국(next Generation NodeB, gNB)**: 5G 무선 접속과 자원 제어를 담당하는 기지국
- **최신성(Freshness)**: 생성 시각과 순서 정보로 오래된 메시지의 재전송 여부를 판단하는 성질
- **백분위수(Percentile)**: 측정값을 작은 순서로 나열했을 때 지정한 비율의 값이 그 이하가 되는 경계
- **백홀(Backhaul)**: RSU나 기지국의 트래픽을 V2X 서버·코어망으로 운반하는 전송 구간

## Ⅰ. 개요

- 정의/개념: 차량 안전 메시지를 **C-V2X·DSRC** 무선 접속으로 전달하는 **V2X 기술군**
- 배경/필요성: 단일 규격으로는 기존 **WAVE 호환**과 이동통신 진화 경로 동시 수용 곤란

### 쉽게 이해하기 (학습용)

- 두 기술 모두 차량 위험을 알리지만 이동통신 자원을 쓰는지 무선랜처럼 채널 경쟁을 하는지가 다르다

## Ⅱ. 특징

- C-V2X의 **PC5 직접·Uu 망 경유** 이중 경로
- DSRC의 **OCB·CSMA/CA** 기반 직접 접속
- 차량 밀도 증가 시 **채널 경쟁·충돌**로 DSRC 지연·손실 증가

### 쉽게 이해하기 (학습용)

- 규격 이름만 보고 고르지 말고 같은 주파수·차량 밀도·속도에서 위험 메시지가 제때 도착하는지 비교해야 한다

## Ⅲ. 구조 및 구성요소

```mermaid
block
    columns 1
    block:V2X["V2X 무선 체계"]
        columns 1
        OBU["차량 OBU"]
        ACCESS["무선 접속 제어"]
        PEER["수신 차량·RSU"]
        SERVER["광역망·V2X 서버"]
        PKI["V2X PKI"]
    end
    OBU --- ACCESS
    ACCESS --- PEER
    OBU --- SERVER
    PEER --- SERVER
    PKI --- OBU
    PKI --- PEER
```

| 구성요소 | 책임 |
|:---|:---|
| 차량 OBU | C-V2X 또는 DSRC **안전 메시지** 생성·수신 |
| 무선 접속 제어 | **PC5 자원 선택·OCB 채널 경쟁** 수행 |
| 수신 차량·RSU | 직접 무선 구간의 **위험 정보** 수신 |
| 광역망·V2X 서버 | Uu·RSU 백홀의 **광역 정보** 집계·배포 |
| V2X PKI | 두 방식의 **인증서** 발급·검증·폐기 |

### 쉽게 이해하기 (학습용)

- C-V2X 차량은 직접 링크와 이동통신망을 함께 쓰고 DSRC 차량은 OCB로 주변 차량·RSU와 직접 통신한다

## Ⅳ. 흐름도

```mermaid
sequenceDiagram
    participant 송신OBU
    participant 무선접속제어
    participant 수신OBU
    participant PKI as V2X PKI
    송신OBU->>무선접속제어: 1. 안전 메시지 전송 요구
    alt C-V2X
        무선접속제어->>수신OBU: 2. PC5 안전 메시지
    else DSRC
        무선접속제어->>수신OBU: 3. OCB 안전 메시지
    end
    수신OBU->>PKI: 4. 인증서 상태 요청
    PKI-->>수신OBU: 인증서 상태
```

**동작 원리**

1. **안전 메시지 전송 요구**: 송신 OBU가 위험 정보의 전송 기한 지정
2. **PC5 안전 메시지**: **사이드링크 자원** 선택·예약 후 전송
3. **OCB 안전 메시지**: **CSMA/CA** 채널 감지·임의 대기 후 전송
4. **인증서 상태 요청**: 서명·**최신성** 검증 후 메시지 수용

### 쉽게 이해하기 (학습용)

- C-V2X는 보낼 시간·주파수 자원을 고르고 DSRC는 채널이 비었는지 듣고 경쟁해서 보낸다

## Ⅴ. 종류 및 비교

| V2X 무선 방식 | C-V2X | DSRC |
|:---|:---|:---|
| 적용 기준 | 이동통신 진화·**광역망 연계**가 필요할 때 | 기존 WAVE·**RSU 호환**이 필요할 때 |
| 핵심 특징 | 3GPP의 **PC5·Uu 통신** | IEEE WAVE의 **OCB 직접 접속** |
| 한계 | 세대·모드 간 **호환 제약** | 고밀도 **채널 경쟁·충돌** |

> 요약: 기존 인프라와 진화 경로로 방식 선택

### 쉽게 이해하기 (학습용)

- 이동통신망과 함께 진화하려면 C-V2X, 이미 깔린 WAVE 장비를 유지하려면 DSRC를 우선 검토한다

## Ⅵ. 실무 고려사항 및 대책

| 고려사항 | 대책 | 효과 |
|:---|:---|:---|
| 규격명만으로 선택해 현장 **전달 성능** 미검증 | 동일 밀도·속도·대역의 **비교 시험** | 같은 조건의 수신률·지연 확보 |
| 기존 OBU·RSU와 **세대 호환** 누락 | 장비·단말·**인증서 생태계** 조사 | 교체 대상·전환 비용 사전 산정 |
| 혼잡 시 **안전 메시지 손실·지연** 증가 | 수신률·지연 **백분위수** 측정 | 안전 메시지의 기한 초과율 판정 |

### 쉽게 이해하기 (학습용)

- 같은 수의 차량이 동시에 경고를 보낼 때 두 방식 중 더 많이 제때 도착하는 쪽을 확인한다

## Ⅶ. 결론

- 기존 WAVE·RSU 호환이 우선이면 **DSRC**, 이동통신 진화·광역 연계면 **C-V2X** 선택

### 쉽게 이해하기 (학습용)

- 기존 장비 활용성과 붐비는 도로의 기한 내 전달 성능을 함께 비교해야 한다.
