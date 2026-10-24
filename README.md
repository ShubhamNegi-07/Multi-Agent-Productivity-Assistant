- "I'm at 72% with 60% done. What do I need on the final to hit 80%?"

</td><td>

**💰 Finance**
- "Calculate EMI for 5 lakhs at 9% for 5 years."
- "Split my ₹60,000 salary using the 50/30/20 rule."

</td></tr>
</table>

## 🏗 Architecture

```
User input
    │
    ▼
Streamlit UI (app.py)  ── AGENTS registry drives routing
    │
    ▼
Selected agent (agents/)  ── system prompt + scoped tool list
    │
    ▼
utils/agent_runtime.run_agent  ── guarded invoke, readable error translation
    │
    ▼
LangChain tool calling (create_agent)
    │
    ▼
Tool execution (tools/) ── external APIs / calculation logic
    │
    ▼
Gemini formats the response
    │
    ▼
Response displayed in UI
```

Failures raise rather than return a fake answer: `agent_runtime` turns provider errors into plain sentences, and `app.py` renders them as an error bubble in the thread.

## 🧰 Technologies

| | Technology | Purpose |
|:---:|---|---|
| 🐍 | Python 3.10+ | Application runtime |
| 🦜 | LangChain 1.x | Agent creation and tool calling |
| 🕸 | LangGraph 1.x | Agent execution graph behind `create_agent` |
| ✨ | Gemini 2.5 Flash | LLM reasoning and generation |
| 🌦 | OpenWeatherMap | Real-time weather data |
| 🎈 | Streamlit 1.56+ | Web frontend |
| 🔐 | python-dotenv | Environment variable management |

## 🤝 Contributing

<!-- PLACEHOLDER: no process existed in the original README. -->

## 📜 Changelog

<!-- TODO: verify release history. -->

## 📄 License