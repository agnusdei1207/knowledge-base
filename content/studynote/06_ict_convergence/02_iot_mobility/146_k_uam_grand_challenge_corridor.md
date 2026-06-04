+++
title = "146. K-UAM 그랜드 챌린지 & 회랑(Corridor) - 한국 UAM 실증"
date = 2026-04-19

[taxonomies]
tags = ["studynote-ict-convergence"]

[extra]
tags = ["studynote-ict-convergence"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: [K-UAM](/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/368_k_uam/) 그랜드 챌린지는 <strong>한국 정부 주도로 <a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/">UAM</a> 운항 실증·<a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>을 단계적으로 추진</strong>하는 프로그램이며, [UAM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) 회랑(Corridor)은 <strong>기존 항공 교통과 분리된 전용 비행 경로</strong>이다.
> 2. **가치**: 도심 비행은 <strong>기존 항공법·소음·안전 규제</strong>를 만족해야 하며, 그랜드 챌린지를 통해 <strong>기체 <a href="/knowledge-base/studynote/04_software_engineering/05_devops_ci_cd/303_authentication_authorization_patterns/">인증</a>·<a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/147_utm_unmanned_aircraft_system_traffic_management/">UTM</a>·버티포트·운항 절차</strong>를 실증하여 상용화 기반을 마련한다.
> 3. **판단 포인트**: 1단계(2025, 유인 실증)->2단계(2027, 시범 운항)->3단계(2030+, 상용 운항)의 로드맵이며, 인천공항~잠실·김포~여의도 회랑이 후보이다.

---

## Ⅰ. 개요 및 필요성

```text
K-UAM 로드맵:
  2025: 그랜드 챌린지 (유인 실증 비행)
  2027: 시범 상용 서비스
  2030+: 본격 상용화
UAM 회랑: 고도 300~600m, 전용 비행 경로
  -> 기존 항공과 분리 -> 안전 확보
```

- **📢 섹션 요약 비유**: [UAM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) 회랑은 <strong>하늘의 고속도로</strong>이다. 자동차 전용도로처럼 UAM만 다닐 수 있는 하늘 길을 만든다.

---

## Ⅱ~Ⅴ. 결론

K-UAM은 <strong>한국 도심 항공의 실증·상용화 <a href="/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/">전략</a></strong>이며, 2025 그랜드 챌린지가 핵심 이정표이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| <strong><a href="/knowledge-base/studynote/13_cloud_architecture/05_data_engineering/368_k_uam/">K-UAM</a></strong> | 한국 [UAM](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/) [전략](/knowledge-base/studynote/04_software_engineering/04_testing_quality/268_strategy_pattern/) |
| **그랜드 챌린지** | 실증 프로그램 |
| **회랑** | 전용 비행 경로 |
| <strong><a href="/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/147_utm_unmanned_aircraft_system_traffic_management/">UTM</a></strong> | 교통 관리 |
| **버티포트** | 이착륙 인프라 |

### 📈 관련 키워드 및 발전 흐름도

```text
[UAM 로드맵 발표 (2020)] -> [K-UAM TF (2021)]
    -> [그랜드 챌린지 (2025)]
    -> [시범 운항 (2027)] -> [현재: 상용화 (2030+)]
```

### 👶 어린이를 위한 3줄 비유 설명
1. K-UAM은 <strong>하늘의 고속도로</strong>를 만드는 거예요.
2. 비행 택시가 <strong>정해진 하늘 길(회랑)</strong>을 따라 안전하게 날아요.
3. 2025년에 <strong>시험 비행</strong>을 하고, 2030년에 **누구나 탈 수** 있을 거예요!

---

## 🔗 이전/다음 글 (Navigation)

**진행 상황**: 146 / 552

<- **이전**: [145. UAM (Urban Air Mobility) - 도심 항공 모빌리티 & eVTOL](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/145_uam_urban_air_mobility_evtol/)
**다음**: [147. UTM (Unmanned Aircraft System Traffic Management) - 무인 비행체 교통 관제 시스템](/knowledge-base/studynote/06_ict_convergence/02_iot_mobility/147_utm_unmanned_aircraft_system_traffic_management/) ->

---
