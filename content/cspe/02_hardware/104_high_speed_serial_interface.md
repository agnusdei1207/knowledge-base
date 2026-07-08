---
title: "고속 직렬 인터페이스 — USB·Thunderbolt (High-Speed Serial Interface)"
date: "2026-07-08"
tags:
  - "cspe-hardware"
weight: 104
extra:
  question_no: "104"
  exam_status: "미출제"
---

## 미리 알고가기

- USB는 범용 장치 연결과 전력 공급을 지원하는 직렬 인터페이스임
- Thunderbolt는 PCIe와 DisplayPort를 터널링하는 고성능 직렬 인터페이스임
- 같은 커넥터라도 지원 속도와 전력과 기능은 다를 수 있음

## Ⅰ. 개요

- **정의/개념**: 고속 직렬 인터페이스는 USB와 Thunderbolt처럼 차동 lane과 프로토콜 협상을 이용해 데이터와 전력과 영상 신호를 단일 외부 포트로 전송하는 연결 기술임
- **배경/필요성**: 병렬 버스는 핀 수와 신호 왜곡 문제로 고속화 한계가 크고 사용자 기기는 얇은 폼팩터와 통합 포트를 요구하므로, 외부 확장성과 전송 효율을 높이는 고속 직렬 구조가 필요함

## Ⅱ. 특징

- 적은 수의 lane으로 높은 전송률과 포트 통합을 제공함
- 데이터 전송뿐 아니라 충전과 영상 출력과 확장 장치 연결을 함께 다룰 수 있음
- 케이블과 장치와 포트가 모두 같은 기능을 지원해야 실제 성능이 나옴
- Thunderbolt 계열은 PCIe 터널링 특성 때문에 DMA 보안 검토가 중요함

## Ⅲ. 종류 및 비교

| 판단 기준 | USB | Thunderbolt |
|:---|:---|:---|
| 핵심 목적 | 범용 장치 연결과 충전 | 고성능 확장과 영상 및 PCIe 터널링 |
| 호환성 | 폭넓고 대중적임 | 성능은 높지만 인증과 케이블 조건 영향 큼 |
| 성능 특성 | 버전별 속도와 alternate mode 다양 | 높은 대역폭과 도킹 및 daisy chain 지원 |
| 보안 고려 | 장치 승인과 데이터 접근 통제 | DMA 보호와 IOMMU 연계 중요 |

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Host Controller | 장치 탐지와 프로토콜 협상과 트랜잭션 제어를 담당해 실제 기능 노출 범위를 결정함 |
| PHY and Lane | 링크 훈련과 신호 보정과 전기 전송 품질을 담당해 negotiated speed를 좌우함 |
| Protocol Layer | 데이터와 영상과 터널링 패킷 규칙을 처리해 인터페이스별 기능 차이를 만듦 |
| Power and Cable | PD 협상과 케이블 인증이 전력 공급과 속도와 안정성 한계를 결정함 |

## Ⅴ. 원리 및 절차 흐름도

```text
+-------------+     +-------------+     +-------------+     +-------------+
| 연결 감지      | --> | 기능 협상      | --> | 데이터 전송    | --> | 오류/보안 처리 |
+-------------+     +-------------+     +-------------+     +-------------+
```

1. **연결 감지**: 포트가 장치와 케이블과 전력 역할을 인식함
2. **기능 협상**: 속도와 lane 수와 alternate mode와 전력 수준을 결정함
3. **데이터 전송**: 데이터와 영상과 제어 메시지를 프로토콜 규칙에 따라 전송함
4. **오류 및 보안 처리**: CRC와 link retry와 장치 승인과 DMA 보호를 수행함

## Ⅵ. 문제점 및 해결 방안

1. 문제: 같은 USB-C 형태라도 속도와 전력과 영상 지원이 달라 사용자가 실제 기능을 오해할 수 있음
   - 해결방안: 포트별 지원 기능과 승인 케이블 목록을 표준화하고 compatibility matrix와 helpdesk incident count로 검증함
2. 문제: 케이블 품질과 EMI와 retimer 조건이 맞지 않으면 고속 링크 오류가 증가할 수 있음
   - 해결방안: SI 시험과 인증 케이블 적용을 수행하고 link error rate와 negotiated speed success rate로 검증함
3. 문제: Thunderbolt 같은 PCIe 터널링 포트는 외부 장치 DMA 공격 경로가 될 수 있음
   - 해결방안: IOMMU와 device authorization 정책을 활성화하고 unauthorized DMA block rate와 port policy compliance로 검증함

## Ⅶ. 적용 사례

- 업무용 노트북 도킹 표준화에서는 승인 독과 케이블만 허용하고 확인 지표는 compatibility matrix와 helpdesk incident count임
- 외장 고속 스토리지 구성에서는 link training 결과를 점검하고 확인 지표는 negotiated speed와 link error rate임
- 보안 구역 단말에서는 Thunderbolt 포트를 제한 정책으로 운영하고 확인 지표는 unauthorized DMA block rate와 policy compliance rate임

## Ⅷ. 결론

고속 직렬 인터페이스 평가는 최대 전송률 숫자보다 실제 협상 속도와 전력 조건과 외부 DMA 보안 통제를 함께 보는 것이 맞음.
