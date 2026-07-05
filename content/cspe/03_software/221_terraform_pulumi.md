---
title: "테라폼과 풀루미 (Terraform vs Pulumi)"
date: "2026-07-05"
author: "Claude Opus 4.6 (Enhanced by Gemini 3.5)"
tags:
  - "cspe-software"
weight: 221
---

## 핵심 인사이트 (3줄 요약)
- **Terraform(테라폼)**은 전 세계 IaC(코드로서의 인프라) 시장을 장악한 HashiCorp의 괴물 같은 툴. HCL이라는 전용 언어(약간 JSON 같음)를 써서 인프라를 선언형으로 매우 안정적으로 찍어냄.
- **Pulumi(풀루미)**는 "아니, 왜 인프라 코드를 짜는데 생전 처음 보는 HCL 문법을 배워야 해? 그냥 내가 잘하는 Python이나 TypeScript로 반복문(for) 쓰면서 인프라를 짜게 해 줘!"라며 테라폼에 도전장을 내민 차세대 IaC 툴.
- 테라폼은 수많은 레퍼런스와 극강의 안정성으로 'DevOps 엔지니어'들의 사랑을 받고, 풀루미는 친숙한 프로그래밍 언어로 짤 수 있어 '일반 앱 개발자'들의 압도적 지지를 받는 경쟁 구도임.
---

### 🔑 핵심 용어 정리

| 용어 | 뜻 | 비유 |
|:---|:---|:---|
| **개요** | 클라우드 인프라 리소스를 프로비저닝하고 관리하기 위한 오픈소스 기반의 Infrastructure as Code (IaC) 도구들 | "핵심 기술 요소" |
| **필요성** | AWS CloudFormation은 AWS에서만 쓸 수 있어서 멀티 클라우드(AWS+GCP)를 쓰면 멘붕이 옴 | "전기처럼 빌려 쓰는 컴퓨팅" |
| **1. Terraform (테라폼) - 선언형 HCL의 마스터피스** | - `main.tf`라는 파일에 **HCL(HashiCorp Configuration Language)**이라는 언어로 "EC2 1대 만들... | "지문" |
| **2. Pulumi (풀루미) - 진짜 코딩으로 인프라 굽기** | - HCL을 버리고, **TypeScript, Python, Go** 같은 일반 프로그래밍 언어를 그대로 씀 | "인터넷 주소" |
| **3. Provider (플러그인 생태계)** | - 두 도구 모두 '프로바이더'라는 플러그인을 다운받아 씀 | "핵심 기술 요소" |
| **State File (상태 파일) 관리 아키텍처의 중요성** | 테라폼이나 풀루미나 가장 골치 아픈 건 현실 클라우드와 코드 사이의 간극을 기록해 두는 'State 파일'임 | "핵심 기술 요소" |
| **CDK (Cloud Development Kit)와의 관계** | 풀루미처럼 진짜 언어로 인프라를 짜는 트렌드가 거세지자, HashiCorp도 'CDKTF(CDK for Terraform)'를, AWS도 ... | "지문" |

---


## Ⅰ. 개요 및 필요성
- **개요**: 클라우드 인프라 리소스를 프로비저닝하고 관리하기 위한 오픈소스 기반의 Infrastructure as Code (IaC) 도구들.
- **필요성**: AWS CloudFormation은 AWS에서만 쓸 수 있어서 멀티 클라우드(AWS+GCP)를 쓰면 멘붕이 옴. **"클라우드 벤더에 종속되지 않고, AWS든 Azure든 똑같은 도구로 인프라를 찍어낼 수 있는 글로벌 표준 툴(Terraform)이 필요해!"** 이후, **"근데 테라폼 전용 언어(HCL)로 100개의 서버를 만들려니까 너무 노가다야. 진짜 프로그래밍 언어로 짜면 안 돼?(Pulumi)"**라는 니즈가 연이어 발생함.
---
## Ⅱ. 아키텍처 및 핵심 원리
- **1. Terraform (테라폼) - 선언형 HCL의 마스터피스**:
  - `main.tf`라는 파일에 **HCL(HashiCorp Configuration Language)**이라는 언어로 "EC2 1대 만들어줘"라고 적음.
  - `terraform plan`을 치면 "이렇게 만들 예정이야"라고 미리 보기(Dry-run)를 보여줌 (이게 테라폼 최고의 킬러 기능).
  - `terraform apply`를 치면 AWS API를 찔러서 실제 인프라를 만들어내고, 결과를 `.tfstate`라는 상태 파일에 저장해 둠.
- **2. Pulumi (풀루미) - 진짜 코딩으로 인프라 굽기**:
  - HCL을 버리고, **TypeScript, Python, Go** 같은 일반 프로그래밍 언어를 그대로 씀.
  - `for i in range(10): create_server()` 처럼 개발자에게 익숙한 반복문과 if 문을 써서 다이나믹하게 인프라를 찍어냄. (테라폼은 이게 더럽게 힘듦).
- **3. Provider (플러그인 생태계)**:
  - 두 도구 모두 '프로바이더'라는 플러그인을 다운받아 씀. AWS 프로바이더를 받으면 AWS를 조종하고, Kubernetes 프로바이더를 받으면 K8s를 조종할 수 있는 무한한 확장성을 가짐.

```text
[ Terraform 코드(HCL) vs Pulumi 코드(Python) 비교 ]

 🏗️ [ Terraform (HCL 언어 - 구조적이고 뻣뻣함) ]
 resource "aws_instance" "web" {
   count         = 3  # 반복문을 count라는 특수한 문법으로 처리함
   ami           = "ami-12345"
   instance_type = "t2.micro"
 }

 🐍 [ Pulumi (Python 언어 - 매우 유연하고 친숙함) ]
 import pulumi_aws as aws
 
 for i in range(3):  # 파이썬의 진짜 for 문을 씀!
     aws.ec2.Instance(f"web-{i}",
         ami="ami-12345",
         instance_type="t2.micro"
     )
```
---
## Ⅲ. 비교 및 연결
| 구분 | Terraform (테라폼) | Pulumi (풀루미) |
|---|---|---|
| **사용 언어** | **HCL (HashiCorp 고유 언어)** | **Python, TypeScript, Go 등 일반 언어** |
| **학습 곡선** | HCL이라는 새로운 언어를 배워야 함 | 기존 개발자는 0시간 만에 바로 짤 수 있음 |
| **테스트 및 추상화**| 조금 까다로움 | 일반 언어이므로 단위 테스트(Unit Test)가 매우 쉬움 |
| **생태계 및 레퍼런스**| **압도적인 1위 (구글 치면 다 나옴)** | 아직 성장 중이나 무섭게 쫓아옴 |
| **주 사용 타겟** | 인프라/DevOps 엔지니어 | 풀스택 / 백엔드 개발자 |
---
## Ⅳ. 실무 적용 및 기술사 판단
- **State File (상태 파일) 관리 아키텍처의 중요성**: 테라폼이나 풀루미나 가장 골치 아픈 건 현실 클라우드와 코드 사이의 간극을 기록해 두는 'State 파일'임. 특히 테라폼은 개발자 2명이 동시에 `apply`를 누르면 State 파일이 꼬여서 인프라가 박살 남. 기술사는 멀티 유저 환경에서 반드시 **AWS S3 + DynamoDB(Locking)**를 조합하거나, Terraform Cloud 같은 원격 백엔드를 구축하여 '동시 실행으로 인한 상태 오염'을 원천 차단해야 함.
- **CDK (Cloud Development Kit)와의 관계**: 풀루미처럼 진짜 언어로 인프라를 짜는 트렌드가 거세지자, HashiCorp도 'CDKTF(CDK for Terraform)'를, AWS도 'AWS CDK'를 내놓았음. 만약 회사가 **"우리는 평생 AWS만 쓴다"**면 AWS CDK가 가장 강력하지만, **"우리는 하이브리드(AWS+GCP+On-prem)를 쓴다"**면 클라우드 중립적인 Terraform이나 Pulumi를 채택하는 것이 올바른 아키텍처 의사결정임.
---
## Ⅴ. 기대효과 및 결론
- 테라폼은 독자적인 언어(HCL)를 강제하지만, 그만큼 엄격하고 실수할 확률을 줄여주어 전 세계 클라우드 인프라의 글로벌 표준(De facto)이 됨.
- 풀루미는 "인프라도 결국 소프트웨어다"라는 철학을 극한으로 밀어붙여, 인프라 팀과 개발 팀의 경계를 완전히 허무는 진정한 DevOps의 미래를 보여주고 있음.
---
### 📌 관련 개념 맵
- IaC ➡️ Declarative ➡️ HashiCorp Terraform (HCL, State file) ➡️ AWS CDK / Pulumi (General Purpose Language) ➡️ Multi-Cloud Provisioning

### 📈 관련 키워드 및 발전 흐름도
- 특정 벤더 종속 도구(AWS CloudFormation) ➡️ 멀티 클라우드를 지원하는 Terraform의 등장과 천하 통일(2014) ➡️ HCL 문법의 한계(반복문, 테스트 등) 체감 ➡️ 진짜 언어로 코딩하는 Pulumi의 등장(2018) ➡️ HashiCorp의 라이선스 변경(BUSL)으로 인한 최근 오픈소스 생태계(OpenTofu)의 분열

### 👶 어린이를 위한 3줄 비유 설명
1. **테라폼**은 '외국어(HCL)로 된 로봇 조종 설명서'예요. 외국어를 새로 배워야 해서 조금 귀찮지만, 로봇이 아주 정확하고 튼튼하게 움직여요. (전 세계 1등이에요).
2. **풀루미**는 '우리가 늘 쓰던 한국어(Python 등)'로 로봇을 조종하는 거예요. 
3. 새 언어를 안 배워도 돼서 엄청 편하고, 평소 하던 대로 조건문이나 반복문을 마구 섞어서 아주 똑똑하게 로봇을 움직일 수 있답니다!
