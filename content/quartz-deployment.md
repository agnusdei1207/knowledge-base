# 🌐 Quartz를 이용한 사내 위키 웹 사이트 배포 가이드

Quartz는 Foam 마크다운 저장소를 활용해 초고속 웹 브라우저 뷰어를 만들어주는 최적의 동반자입니다.

---

## 🛠️ GitHub Actions를 이용한 무상 배포 (정석)

GitHub Pages를 통해 별도의 웹서버를 구축하지 않고도 무료로 실시간 위키 사이트를 배포할 수 있습니다.

1. **레포지토리 설정 변경:** 
   * GitHub 레포지토리 Settings -> Pages 탭 진입
   * Build and deployment -> Source를 **GitHub Actions**로 변경
2. **GitHub Workflow 파일 생성:**
   * `.github/workflows/deploy.yml` 파일 생성 (자동 생성 스크립트 실행 시 셋팅 가능)
3. **배포 확인:**
   * 이제 마크다운 문서를 쓰고 깃허브에 `git push`하기만 하면 약 1분 뒤에 `https://<organization>.github.io/<repository>` 경로에 검색과 인터랙티브 노드 그래프가 연동된 고급 웹 위키가 즉시 배포됩니다!

---

## 🐳 Docker를 이용한 사내망 내부 배포 (Private)

만약 외부 GitHub Pages로의 노출을 원치 않고 회사 로컬 서버(내부망)에 띄우고 싶다면 Docker Compose와 Nginx를 사용해 Quartz를 호스팅합니다.

1. **Quartz 빌드 스크립트 실행:**
   * 매번 마크다운 파일이 푸시될 때마다 서버에서 Quartz 빌드를 트리거하여 정적 html을 얻습니다.
2. **Nginx 컨테이너 구동:**
   * Docker Compose를 통해 Nginx가 정적 파일을 서빙하도록 구성합니다.
   * `http://internal-wiki.company.local` 형태로 사내 인트라넷에서 안전하게 접속할 수 있습니다.
