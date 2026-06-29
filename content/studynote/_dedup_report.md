---
title: "Study Note Dedup Report"
date: "2026-06-29"
tags:
  - "studynote-report"
---

## 대표 중복군 수작업 정리 보고

- 범위: `content/studynote/` 내 대표 중복군만 수작업 정리, `_index.md`·`keyword_list.md` 제외
- 처리 원칙: 대표 노트 1건 선정, 대표 노트 상단 `<!-- top-summary -->` 추가, 타 과목 관점 1~2줄 보강
- 링크 원칙: 비대표 노트 상단 인용블록에 `> 🔗 대표 정리: [[대표노트명]]` 포함

### 처리 목록

- TOGAF
  - 대표: `12_it_management/03_ea_isp/113_togaf.md`
  - 링크 처리: `12_it_management/03_ea_isp/897_togaf_the_open_group_architecture_framework.md`
  - 메모: EA 방법론 기준 노트로 통합, 비대표는 대표 노트로 유도

- EAMS
  - 대표: `12_it_management/03_ea_isp/124_eams_ea_management_system.md`
  - 링크 처리: `12_it_management/03_ea_isp/908_eams_enterprise_architecture_management_system.md`
  - 메모: EA 저장소·메타모델 관점의 기준 노트 유지

- EA Governance
  - 대표: `12_it_management/03_ea_isp/122_ea_governance.md`
  - 링크 처리: `12_it_management/03_ea_isp/906_ea_governance_arb_architecture_review_board.md`
  - 메모: ARB 포함 세부 설명은 대표 노트로 수렴

- CASB
  - 대표: `03_network/14_network_security_threats/741_casb_cloud_access_security_broker.md`
  - 링크 처리: `09_security/16_data_privacy/829_casb.md`
  - 링크 처리: `07_enterprise_systems/08_cloud_finops/340_it_casb_exam_07_enterprise.md`
  - 메모: 네트워크·보안·엔터프라이즈 관점을 대표 노트 기준으로 정리

- Distributed Tracing
  - 대표: `13_cloud_architecture/04_devops_observability/188_distributed_tracing_opentelemetry.md`
  - 링크 처리: `15_devops_sre/03_sre_observability/141_distributed_tracing_msa_request_flow.md`
  - 링크 처리: `04_software_engineering/11_testing_validation/961_distributed_tracing.md`
  - 메모: OTel 기반 설명이 가장 완결적이라 대표로 유지

- Service Mesh
  - 대표: `07_enterprise_systems/03_eai_esb_msa/181_service_mesh_istio_linkerd.md`
  - 링크 처리: `13_cloud_architecture/03_msa_serverless/144_service_mesh.md`
  - 링크 처리: `04_software_engineering/11_testing_validation/937_service_mesh.md`
  - 메모: 구조, 운영 부담, 도구 비교가 함께 정리된 노트를 대표로 유지
