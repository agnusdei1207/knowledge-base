---
sidebar:
  order: 202
  label: "202. OPC UA 산업 표준 통신 (OPC Unified Architecture)"
  badge:
    text: "기출 · 70%"
    variant: note
title: "OPC UA 산업 표준 통신 (OPC Unified Architecture)"
date: "2026-07-25T03:31:00+09:00"
tags:
  - "notes-latest-tech"
weight: 202
extra:
  question_no: "202"
  source_status: "기출"
  source_history: "137회"
  priority: 70
  priority_note: "OPC UA 정보 모델·보안 통신이 최근 출제됨"
---

## 미리 알고가기

- **OPC UA**: 정보 모델과 보안을 포함한 산업 상호운용 표준
- **통신 방식**: Client-Server와 PubSub 방식을 모두 지원함
- **벤더 중립성**: 벤더 중립성과 의미 기반 주소공간이 핵심 차별점임



## Ⅰ. 개요

- **정의/개념**: 산업 데이터·의미를 교환하는 독립 상호운용 규격
- **배경/필요성**: 장비·플랫폼별 통신과 의미 단절을 해소

### 쉽게 이해하기 (학습용)

- 기계별 정보를 공통 사전과 보안 규격으로 주고받는 표준임

## Ⅱ. 특징

- AddressSpace가 값·구조·관계를 함께 표현한다.
- 정보 모델이 업종·장비 의미를 표준화한다.
- 서비스·매핑 분리가 전송 기술 종속을 낮춘다.
- 내장 보안·통신 모델이 안전한 교환을 지원한다.

### 쉽게 이해하기 (학습용)

- 공통 사전으로 주소록을 만들고 상황별 전달 방식과 보안을 선택함

## Ⅲ. 아키텍처 및 구성요소

| 설계 요소 | 설명 |
|:---|:---|
| Information Model | 데이터 형식 및 의미 규격 정의 |
| AddressSpace | 자산 정보의 동적 발견 및 표현 |
| Service Set | 상호작용 및 통신 서비스 정의 |
| Security | 인증 및 암호화 등 신뢰 관리 |
| Transport Mapping | 프로토콜 및 데이터 표현 방식 |

> 요약: 통합 모델과 주소공간으로 의미를 공유하고 표준을 통함

### 쉽게 이해하기 (학습용)

- 공통 기계 사전으로 주소록을 만들고 질문 창구나 방송을 쓰며, 봉투 형식·운송로와 신분증·방송 열쇠는 환경에 맞게 선택하는 구조임

## Ⅳ. 원리 및 절차 흐름도

모델합의
 ↓
trust설정
 ↓
정보발견
 ↓
정보교환
 ↓
키운영

| 절차 | 설명 |
|:---|:---|
| model·namespace 합의 | model·namespace 합의을 수행하고 결과를 검증함 |
| endpoint 발견·trust 설정 | endpoint 발견·trust 설정을 수행하고 결과를 검증함 |
| secure 연결·정보 발견 | secure 연결·정보 발견을 수행하고 결과를 검증함 |
| data·event·method 교환 | data·event·method 교환을 수행하고 결과를 검증함 |
| audit·certificate/key 운영 | audit·certificate/ke을 수행하고 결과를 검증함 |

> 요약: 모델 합의 후 인증된 보안 채널로 정보를 교환함

### 쉽게 이해하기 (학습용)

- 같은 사전을 정하고 상대 창구의 신분증을 승인한 뒤 주소록을 찾아 질문·방송하며, 출입기록과 만료된 신분증·방송 열쇠를 계속 관리함

## Ⅴ. 종류 및 비교

| 판단 기준 | OPC UA Client–Server | OPC UA PubSub | OPC Classic |
|:---|:---|:---|:---|
| 핵심 특징 | 요청·응답과 정보 모델 탐색 | 다대다 비동기 메시지 배포 | COM·DCOM 기반 태그 교환 |
| 적용 기준 | 장비 탐색·명령·상태 조회 | 대규모 telemetry·event 배포 | 기존 Windows 설비 연계 |
| 주요 위험 | 세션·서버 확장 병목 | QoS·키·broker 구성 복잡 | DCOM 보안·플랫폼 종속 |

> 요약: 유연한 보안 통신과 표준 모델을 제공함

### 쉽게 이해하기 (학습용)

- 담당 창구에 질문·명령하는 방식, 필요한 사람이 듣는 방송 방식, Windows 전용 옛 창구 방식의 차이임

## Ⅵ. 실무 사례

1. 대상 환경의 도입 조건과 설계를 검증함
2. 운영 위험과 성과 지표를 검증함

### 쉽게 이해하기 (학습용)

- 포장 설비 vendor의 OPC UA Companion Model을 gateway가 노출해 SCADA는 alarm·subscription, MES는 lot·machine state·method를 같은 semantic으로 연계함
- 다수 PLC·sensor의 telemetry는 OPC UA PubSub로 edge subscriber에 배포하고 SKS group key·network segmentation을 적용하되 안전 제어는 local PLC에 유지함

## Ⅶ. 결론

- 정보 모델·보안 프로파일로 OPC UA 연계 설계

### 쉽게 이해하기 (학습용)

- 선을 연결하는 데서 끝나지 않고 값의 뜻과 신분증·열쇠를 함께 맞추며, 시간과 안전 요구는 실제 환경에서 따로 검증해야 함
