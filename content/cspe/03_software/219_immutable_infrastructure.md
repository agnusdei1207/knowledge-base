---
title: "불변 인프라 (Immutable Infrastructure)"
date: "2026-07-11"
tags:
  - "cspe-software"
weight: 219
extra:
  question_no: "219"
  exam_status: "미출제"
  exam_note: "전망"
---

## 미리 알고가기

- 불변 인프라는 배포 후 Server·VM·Container를 직접 수정하지 않고 새 Image·설정 Version으로 교체하는 운영 방식임
- Image에는 OS·Runtime·응용·의존성을 고정하고 Secret·업무 데이터·영속 상태는 외부 저장소에 둠
- Patch는 실행 Instance에 적용하지 않고 Base Image를 갱신해 시험·서명한 새 Artifact로 재배포함
- Rollback은 이전 Instance를 수동 복구하는 대신 이전 Image Digest·IaC Version으로 트래픽을 되돌림
- 불변성은 Artifact 경계에 적용되므로 Runtime Log·Cache·임시 파일의 수명과 삭제 정책은 별도로 정해야 함

## 작성 근거(검토용)

- 불변 인프라는 변경 단위, 배포·Patch, 구성 편차, 상태, Rollback, 감사, 적합 조건으로 비교함
- 구조와 절차는 Image Build·검증·서명·교체 배포·Health·전환·폐기를 하나의 흐름으로 설명함
- Auto Scaling 서버와 Batch Worker는 구성 편차·Rollback 시간·구 Image 잔존 수로 검증함

## Ⅰ. 개요

- **정의/개념**: 불변 인프라는 실행 Instance의 구성 변경을 금지하고 선언형 IaC와 Versioned Image로 새 Instance를 생성·검증·전환한 뒤 기존 Instance를 폐기하는 배포 모델임
- **배경/필요성**: 장기 운영 중 수동 Patch·설정 변경으로 Instance별 상태가 달라져 재현·복구·감사가 어려워지는 문제를 Build Artifact와 교체 배포로 통제해야 함

## Ⅱ. 특징

- Image Digest와 IaC Commit이 실행 환경의 OS·Package·Runtime·응용 Version을 식별함
- CI가 Base Image 갱신·취약점 검사·시험·SBOM·서명을 완료한 Artifact만 Registry에 게시함
- Rolling·Blue-Green·Canary로 새 Instance를 배치하고 Readiness·업무 지표 통과 후 트래픽을 전환함
- Config·Secret은 시작 시 주입하되 값 Version과 적용 대상 Image를 배포 기록에 연결함
- Database·Object Storage·Volume 같은 영속 상태를 Instance 수명에서 분리해 교체 중 데이터가 유지되게 함
- 긴급 Shell 수정은 Drift로 탐지하고 수정 내용을 Image Build Pipeline에 반영한 뒤 임시 Instance를 교체함

## Ⅲ. 종류 및 비교

| 판단 기준 | Mutable Infrastructure | Immutable Infrastructure |
|:---|:---|:---|
| 변경 단위 | 실행 Server의 Package·설정·파일 | 새 Image·IaC·Config Version |
| 배포 방식 | Instance에 Patch·명령 실행 | 새 Instance 생성 후 트래픽 전환 |
| 구성 편차 | 변경 이력 누락 시 Instance별 Drift 발생 | 같은 Digest로 생성한 Instance 구성 일치 |
| 상태 배치 | 응용과 영속 상태가 Server에 함께 남을 수 있음 | 영속 상태를 외부 DB·Volume·Object Store에 분리 |
| Rollback | 변경 명령의 역순·Backup 복원 | 이전 Image·IaC Version으로 Instance 재생성 |
| 감사 기준 | Server별 현재 상태·변경 Log 수집 | Artifact Digest·서명·Pipeline·배포 이력 추적 |
| 적합 조건 | 교체할 수 없는 Stateful Legacy·장비 연동 | Auto Scaling·VM Image·Container 기반 서비스 |

> 요약: Mutable은 실행 Server를 변경하고 Immutable은 새 Image·IaC Version의 Instance로 교체함.

## Ⅳ. 구성요소 및 구조

| 구성요소 | 설명 |
|:---|:---|
| Source·IaC·Image Definition | OS·Package·Runtime·응용·자원 구성을 선언함 |
| Build·Test·Scan·SBOM | 재현 가능한 Image를 만들고 기능·취약점·구성 정책을 검사함 |
| Signer·Artifact Registry | Digest·서명·Provenance와 승인된 Image를 보관함 |
| Deployment Controller | Rolling·Blue-Green·Canary로 새 Instance를 생성함 |
| Config·Secret·State Store | 환경별 값과 영속 데이터를 Instance 밖에서 관리함 |
| Health·Traffic Switch·GC | 새 Version을 검증·전환하고 기존 Instance·Image를 폐기함 |

```text
Source·IaC -> Build·Test·Sign -> Registry -> New Instances -> Health -> Traffic Switch
                                                             -> Old Instances Delete
```

> 요약: 서명된 Image와 IaC가 새 Instance를 생성하고 Health·트래픽 전환 후 기존 실행 환경을 폐기함.

## Ⅴ. 원리 및 절차 흐름도

```text
정의 변경 -> Image Build·검증 -> Registry 게시 -> 교체 배포 -> Health 확인 -> 전환·폐기
```

1. **정의 변경**: OS·의존성·응용·IaC·Config 참조를 Source Control에서 수정함
2. **Build·검증**: Image를 생성하고 기능 시험·취약점 Scan·Policy·SBOM·서명을 확인함
3. **Artifact 게시**: 변경 불가능한 Digest로 Registry에 저장하고 배포 승인을 연결함
4. **교체 배포**: Controller가 새 Instance를 만들고 Config·Secret·상태 저장소를 연결함
5. **전환·폐기**: Health·업무 지표 통과 후 트래픽을 전환하고 기존 Instance를 종료함

> 요약: 실행 환경 변경은 Image Build에서만 수행하고 검증된 새 Instance 전환과 기존 Instance 폐기로 반영함.

## Ⅵ. 실무 사례

1. Auto Scaling API 서버는 Image Digest 교체 배포를 적용하고 구성 편차 건수·Rollback 시간을 확인함
2. Batch Worker는 서명 Image와 IaC Version을 적용하고 구 Image 실행 수·교체 완료 시간을 확인함

## Ⅶ. 결론

- 불변 인프라는 상태 외부화·Image 재현성·서명·교체 Health·Rollback·Drift 금지를 배포 Pipeline으로 강제해야 함
