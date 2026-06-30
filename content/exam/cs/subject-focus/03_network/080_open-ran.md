---
title: "Open RAN (Open Radio Access Network)"
date: "2026-06-30"
weight: 80
tags:
  - "exam-cspe-network"
---

## Ⅰ. 정의
> 무선 접속망(RAN)의 구성 요소를 분리하고 개방형 표준 인터페이스로 연결하여 멀티벤더 상호운용과 가상화를 가능하게 하는 차세대 RAN 아키텍처이다.

## Ⅱ. 구성요소 / 원리
- RU/DU/CU 분리: 무선부(Radio Unit)·분산부(Distributed Unit)·중앙부(Centralized Unit) 기능 분할
- 개방형 인터페이스: O-RAN Alliance 표준(예: 프론트홀 7.2x)으로 벤더 간 연동
- RIC(RAN Intelligent Controller): Near-RT/Non-RT로 AI 기반 지능형 제어
- 멀티벤더: 특정 장비사 종속 탈피, 부품 단위 혼합 구성
- 가상화: 범용 서버에서 vDU/vCU 소프트웨어 구동

## Ⅲ. 흐름도 / 구조
```text
   [Non-RT RIC] (정책/AI 학습)
   [Near-RT RIC] (실시간 제어)
        |  개방형 인터페이스(O-RAN)
   CU ── DU ── RU ── 단말
   (가상화 + 멀티벤더 조합)
```

## Ⅳ. 핵심 특징
| 구분 | 내용 |
|:---|:---|
| 목적 | 개방·가상화로 멀티벤더 RAN 생태계 구축 |
| 장점 | 벤더 종속 완화, 비용 절감, 지능형 최적화 |
| 한계 | 상호운용 검증 복잡, 보안 표면 확대, 통합 책임 분산 |

## Ⅴ. 기술사적 적용
- 5G·6G 가상화 RAN(vRAN)의 핵심 추진 방향
- SDN/NFV·클라우드 네이티브와 결합한 RAN 자동화
- RIC를 통한 트래픽·에너지 최적화 등 AI 응용(xApp/rApp)
