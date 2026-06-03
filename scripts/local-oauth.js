#!/usr/bin/env node
const http = require('http');
const https = require('https');
const url = require('url');

// 포트 및 환경변수 설정
const PORT = process.env.PORT || 9091;
const CLIENT_ID = process.env.OAUTH_CLIENT_ID;
const CLIENT_SECRET = process.env.OAUTH_CLIENT_SECRET;

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error("❌ 에러: 환경변수 OAUTH_CLIENT_ID와 OAUTH_CLIENT_SECRET을 설정해야 합니다.");
  console.error("실행 예시: OAUTH_CLIENT_ID=xxx OAUTH_CLIENT_SECRET=yyy node scripts/local-oauth.js");
  process.exit(1);
}

const server = http.createServer((req, res) => {
  const reqUrl = url.parse(req.url, true);
  
  // CORS 허용 설정
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // 1. 로그인 창 열기 (/auth)
  if (reqUrl.pathname === '/auth') {
    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=repo,user`;
    res.writeHead(302, { Location: githubAuthUrl });
    res.end();
    return;
  }

  // 2. 로그인 성공 콜백 (/callback)
  if (reqUrl.pathname === '/callback') {
    const code = reqUrl.query.code;
    if (!code) {
      res.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('인증 코드(code)가 없습니다.');
      return;
    }

    const postData = JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      code: code
    });

    const options = {
      hostname: 'github.com',
      port: 443,
      path: '/login/oauth/access_token',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    // GitHub API로 인증 토큰 교환 요청
    const gitReq = https.request(options, (gitRes) => {
      let body = '';
      gitRes.on('data', (chunk) => body += chunk);
      gitRes.on('end', () => {
        try {
          const data = JSON.parse(body);
          if (data.error) {
            res.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
            res.end(`GitHub 인증 실패: ${data.error_description || data.error}`);
            return;
          }

          // Decap CMS에 토큰 전달하는 HTML
          const html = `
            <!DOCTYPE html>
            <html>
            <head><meta charset="utf-8"/></head>
            <body>
              <script>
                const sender = window.opener || window.parent;
                sender.postMessage("authorization:github:success:${JSON.stringify({
                  token: data.access_token,
                  provider: 'github'
                })}", "*");
              </script>
              <p style="text-align:center; margin-top: 50px; font-family: sans-serif;">
                🎉 인증에 성공했습니다! 이 창을 닫으셔도 좋습니다.
              </p>
            </body>
            </html>
          `;
          res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
          res.end(html);
        } catch (e) {
          res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
          res.end('GitHub 응답 해석 실패');
        }
      });
    });

    gitReq.on('error', (e) => {
      res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end(`네트워크 에러: ${e.message}`);
    });

    gitReq.write(postData);
    gitReq.end();
    return;
  }

  res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
  res.end('페이지를 찾을 수 없습니다.');
});

server.listen(PORT, () => {
  console.log(`✅ 로컬 OAuth 프록시 서버 작동 중: http://localhost:${PORT}`);
  console.log(`   - Authorization URL: http://localhost:${PORT}/auth`);
  console.log(`   - Callback URL: http://localhost:${PORT}/callback`);
});
