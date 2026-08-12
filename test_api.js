const url = "https://api.minimax.io/anthropic/v1/messages";
const token = "sk-cp-Ep8iihBk3z3YmGNnDNYPbYEvdF7vC8FqEHOctrFnAdbpEBRPqM2Yij9BQwuYYDwhjpLEMJwW-WLZKW7OhLaxsA4QpitdaSUoE0WT9REq-sCe3j4LPujhwi8";

async function test() {
  const req = {
    model: "MiniMax-M3[1m]",
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Say hello!" }
    ]
  };

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
    console.log(JSON.stringify(data, null, 2));
  } catch (e) {
    console.error(e);
  }
}

test();
