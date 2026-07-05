---
title: "PUF (Physical Unclonable Function)"
date: "2026-07-05"
tags:
  - "cspe-hardware"
weight: 83
---

## Ⅰ. 개요
- **정의**: 반도체 제조 공정의 미세 물리적 편차를 이용해 복제 불가능한 고유 식별값을 생성하는 하드웨어 함수
- **배경/필요성**: 디지털 키는 복사가 가능하므로, 복제 자체가 물리적으로 불가능한 인증 수단이 필요함
- **비유**: 사람의 지문처럼 공정 편차가 칩마다 고유한 패턴을 만들어 복제가 불가능함

| 출제 의도 | 반드시 짚을 핵심 | 감점 회피 포인트 |
|:---|:---|:---|
| 하드웨어 고유성 기반 인증 원리 | Challenge-Response 메커니즘 | PUF와 Device DNA(084)의 관계 미기술 시 감점 |

> 요약: PUF는 제조 공정의 물리적 무작위성을 활용해 복제 불가능한 칩 고유 식별자를 생성함

## Ⅱ. 구성요소
```text
Challenge (입력 자극)
    |
    v
+-------------------+
| PUF Circuit       |
| (공정 편차 반영)  |
+-------------------+
    |
    v
Response (고유 출력)
    |
    v
+-------------------+
| Fuzzy Extractor   |
+-------------------+
    |
    v
Stable Key (안정화된 키)
```

| 구성요소 | 설명 | 비유 |
|:---|:---|:---|
| PUF Circuit | 공정 편차(게이트 지연, 임계전압 차이)를 반영하는 회로 | 지문의 융선 패턴 |
| Challenge | PUF 회로에 인가하는 입력 자극(비트 패턴) | 손가락을 스캐너에 대는 동작 |
| Response | Challenge에 대해 칩 고유의 물리적 특성이 반영된 출력값 | 스캔된 지문 이미지 |
| Fuzzy Extractor | 환경 변화(온도, 전압)로 인한 응답 노이즈를 보정하여 안정된 키 추출 | 지문 매칭 시 허용 오차 보정 |
| Helper Data | Fuzzy Extractor가 노이즈를 보정하는 데 사용하는 공개 보조 데이터 | 지문 정합용 기준점 좌표 |

> 요약: Challenge-Response 쌍과 Fuzzy Extractor로 환경 변동에도 안정된 고유 키를 추출하는 구조임

## Ⅲ. 절차
```text
Challenge 입력 --> PUF 회로 자극
  --> 물리적 편차 반영 Response 생성
    --> Fuzzy Extractor로 노이즈 보정
      --> 안정화된 키 출력 / CRP DB와 대조하여 인증
```
- 1단계: 검증 서버가 등록된 Challenge-Response Pair(CRP) 중 하나의 Challenge를 칩에 전송함
- 2단계: PUF 회로가 해당 Challenge에 대해 공정 편차가 반영된 고유 Response를 생성함
- 3단계: Fuzzy Extractor가 Helper Data를 참조하여 온도·전압 변동에 의한 비트 오류를 보정함
- 4단계: 보정된 Response를 서버 측 CRP DB와 비교하여 칩 정품 여부를 판정함

> 요약: Challenge 전송 → Response 생성 → 노이즈 보정 → CRP 대조의 4단계로 인증을 수행함

## Ⅳ. 문제점
- 환경 민감성: 온도·전압·노화에 따라 Response 비트가 변동 — 인증 실패율(FRR)이 증가함
- CRP 고갈: Weak PUF는 생성 가능한 CRP 수가 제한적 — 대규모 인증에 부적합함
- 모델링 공격: Strong PUF의 CRP를 수집하여 머신러닝으로 PUF 동작을 모사할 수 있음

> 요약: 환경 변동, CRP 고갈, 머신러닝 기반 모델링 공격이 PUF의 주요 한계임

## Ⅴ. 개선방안
1. 단기: 다수결 투표(Majority Voting)·ECC 기반 Fuzzy Extractor 고도화로 비트 에러율 저감
2. 중기: Controlled PUF(CPUF) 구조 도입으로 CRP 접근을 하드웨어 수준에서 제한하여 모델링 공격 차단
3. 장기: Reconfigurable PUF 기술 적용으로 CRP 풀을 재생성하여 고갈 문제 해소

> 요약: ECC 보정, CPUF 구조, 재구성 PUF로 환경·보안·용량 한계를 단계적으로 극복함

## Ⅵ. 전망
- 발전 방향: IoT 경량 디바이스의 Root of Trust로 PUF 채택 확대
- 기술사적 판단: PUF + Device DNA(084 참조) 결합을 통한 다중 계층 하드웨어 인증이 표준화 추세임
- 기술사 제언: PUF 도입 시 환경 스트레스 테스트와 CRP 관리 정책을 설계 단계에서 수립하는 것이 필요
