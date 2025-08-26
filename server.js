// Minimal backend proxy to call AI provider safely
const path = require('path');
const envPath = path.join(__dirname, '.env');
require('dotenv').config({ path: envPath });

const express = require('express');
const cors = require('cors');

// Node 18+ has global fetch
const app = express();

app.use(cors());
app.use(express.json({ limit: '1mb' }));
app.use(express.static(__dirname));

const PORT = process.env.PORT || 3000;
const AI_API_KEY = process.env.AI_API_KEY;
const AI_BASE_URL = (process.env.AI_BASE_URL || 'https://api.openai.com/v1').replace(/\/$/, '');
const AI_MODEL = process.env.AI_MODEL || 'gpt-4o-mini';

if (!AI_API_KEY) {
  console.warn(`[WARN] Missing AI_API_KEY. Ensure ${envPath} exists and contains AI_API_KEY=...`);
}

app.get('/healthz', (req, res) => {
  res.json({ ok: true });
});

app.post('/api/ai-recommend', async (req, res) => {
  try {
    if (!AI_API_KEY) {
      return res.status(500).json({ error: 'Server is not configured: missing AI_API_KEY' });
    }

    const { dishes = [], preferences = '', history = [] } = req.body || {};

    const userPrompt = [
      '你是一个美食推荐助手。',
      '请从“可选菜品列表”中挑选 1 道最合适的，并简要说明理由。',
      '若用户有偏好/忌口/预算等，请综合考虑。',
      '输出严格遵循 JSON 格式：{"name":"菜名","reason":"简短理由"}，不要包含多余文本。',
      '',
      `可选菜品列表: ${dishes.join('、') || '(空)'}`,
      preferences ? `用户偏好: ${preferences}` : '用户偏好: (无)',
      history && history.length ? `近期抽中: ${history.join('、')}` : '近期抽中: (无)'
    ].join('\n');

    const payload = {
      model: AI_MODEL,
      messages: [
        { role: 'system', content: '你是一个专业的中文美食推荐助手。' },
        { role: 'user', content: userPrompt }
      ],
      temperature: 0.7
    };

    const resp = await fetch(`${AI_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI_API_KEY}`
      },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const text = await resp.text();
      return res.status(resp.status).json({ error: text || 'upstream_error' });
    }

    const data = await resp.json();
    const content = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content || '';

    let name, reason, recommendation;
    try {
      const parsed = JSON.parse(content);
      name = parsed.name;
      reason = parsed.reason;
    } catch (_) {
      recommendation = content;
    }

    return res.json({ name, reason, recommendation });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'server_error', detail: String(err && err.message || err) });
  }
});

app.post('/api/ai-chat', async (req, res) => {
  try {
    if (!AI_API_KEY) {
      return res.status(500).json({ error: 'Server is not configured: missing AI_API_KEY' });
    }

    const { messages = [] } = req.body || {};
    const safeMessages = Array.isArray(messages) ? messages.slice(-20) : [];

    const payload = {
      model: AI_MODEL,
      messages: [
        { role: 'system', content: '你是一个中文美食助手。简洁、友好地回答用户关于吃什么的问题。' },
        ...safeMessages
      ],
      temperature: 0.7
    };

    const resp = await fetch(`${AI_BASE_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI_API_KEY}`
      },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const text = await resp.text();
      return res.status(resp.status).json({ error: text || 'upstream_error' });
    }

    const data = await resp.json();
    const reply = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content || '';
    return res.json({ reply });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'server_error', detail: String(err && err.message || err) });
  }
});

app.listen(PORT, () => {
  console.log(`Server listening on http://localhost:${PORT}`);
  console.log('Open:  http://localhost:' + PORT + '/js/%E4%BB%8A%E5%A4%A9%E5%90%83%E4%BB%80%E4%B9%88index.html');
});


