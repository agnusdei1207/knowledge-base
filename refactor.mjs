import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const url = "https://api.minimax.io/anthropic/v1/messages";
const token = "sk-cp-Ep8iihBk3z3YmGNnDNYPbYEvdF7vC8FqEHOctrFnAdbpEBRPqM2Yij9BQwuYYDwhjpLEMJwW-WLZKW7OhLaxsA4QpitdaSUoE0WT9REq-sCe3j4LPujhwi8";

const systemPrompt = `당신은 CSPE(정보관리기술사/컴퓨터시스템응용기술사) 시험 노트 리팩토링 전문 에이전트입니다.
주어진 마크다운 본문을 다음 규칙에 따라 리팩토링하세요. 프론트매터(Frontmatter)는 제공되지 않으므로 마크다운 본문만 출력하세요.

<규칙>
1. **영어 병기**: <details><summary>핵심 용어</summary> 블록 내의 모든 용어에 대해 '한국어(English)' 또는 'English (한국어)' 형식으로 영어/약어 병기를 추가하세요. 이미 있다면 설명을 더 구체적이고 실질적으로 보완하세요.
2. **정의 품질**: 본문 내에서 "~이다.", "~말함." 같이 끝나는 단순 정의를 실질적 의미, 작동 방식, 사용 맥락이 담긴 문장으로 보완하세요.
3. **본문 내용**: Ⅰ~Ⅶ 섹션 본문에서 단순 열거된 항목들을 구체적 원리와 차별점이 드러나는 문장으로 보완하세요.
4. **Ⅶ 결론의 한줄요약**: "#### 한줄 요약" 밑에 오는 결론 문장은 반드시 완결된 명사구('~체계 적용', '~원칙 준수', '~구현 필수' 등)로 종결하세요. 절대 "~한다", "~이다" 등의 동사구로 끝내지 마세요.
5. **구조 유지**: 기존의 7섹션(Ⅰ~Ⅶ) 구조, 한줄요약, 표(table), 코드블록, 인용구(>) 형식은 절대 훼손하지 말고 그대로 유지하세요.

응답 시 마크다운 본문만 바로 출력하고, 다른 인삿말이나 부연설명은 절대 하지 마세요.`;

async function processContent(content) {
  const req = {
    model: "MiniMax-M3[1m]",
    max_tokens: 8192,
    system: systemPrompt,
    messages: [
      { role: "user", content: "다음 마크다운 본문을 리팩토링해주세요:\n\n" + content }
    ]
  };

  for (let i = 0; i < 3; i++) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "x-api-key": token,
          "anthropic-version": "2023-06-01",
          "content-type": "application/json"
        },
        body: JSON.stringify(req)
      });
      const data = await res.json();
      if (data.content && data.content[0] && data.content[0].text) {
        let result = data.content[0].text.trim();
        // Remove markdown codeblock wrappers if present
        if (result.startsWith("```markdown")) {
          result = result.replace(/^```markdown\n/, '').replace(/\n```$/, '');
        } else if (result.startsWith("```")) {
          result = result.replace(/^```\n/, '').replace(/\n```$/, '');
        }
        return result;
      }
      console.log("Unexpected response format:", JSON.stringify(data).substring(0, 500));
      // wait on error
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      console.error(`Attempt ${i+1} failed:`, e.message);
      await new Promise(r => setTimeout(r, 2000));
    }
  }
  throw new Error("Failed after 3 attempts");
}

async function main() {
  const dir = path.join('C:', 'workspace', 'study', 'src', 'content', 'docs', 'notes', '08-latest-tech');
  const files = fs.readdirSync(dir).filter(f => f.match(/^0[0-7][0-9]_.*\.md$/) && f >= '001_' && f <= '075_');
  
  console.log(`Found ${files.length} files to process.`);
  
  const concurrency = 5;
  for (let i = 0; i < files.length; i += concurrency) {
    const chunk = files.slice(i, i + concurrency);
    console.log(`Processing chunk ${Math.floor(i/concurrency) + 1}/${Math.ceil(files.length/concurrency)}...`);
    
    await Promise.all(chunk.map(async (file) => {
      const filepath = path.join(dir, file);
      const fullText = fs.readFileSync(filepath, 'utf8');
      
      const match = fullText.match(/^(---\r?\n[\s\S]*?\r?\n---\r?\n)([\s\S]*)$/);
      if (!match) {
        console.log(`Skipping ${file} due to missing frontmatter format.`);
        return;
      }
      
      const frontmatter = match[1];
      const body = match[2];
      
      try {
        const newBody = await processContent(body);
        fs.writeFileSync(filepath, frontmatter + newBody + '\n', 'utf8');
        console.log(`Successfully refactored ${file}`);
      } catch (e) {
        console.error(`Error processing ${file}:`, e);
      }
    }));
  }
  
  console.log("All files processed. Running git commands...");
  try {
    execSync('git add -A', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git commit -m "08-latest-tech 001~075: 용어 영어 병기, 종결 다양화, 명사구 종결 교정"', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    execSync('git push', { cwd: 'C:\\workspace\\study', stdio: 'inherit' });
    console.log("Git commands completed successfully.");
  } catch (e) {
    console.error("Git command failed:", e.message);
  }
}

main().catch(console.error);
