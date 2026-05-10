 AI智能伴侣 (AI-Chatbot-Practice)

基于 DeepSeek 大模型和 Streamlit 构建的个性化 AI 聊天机器人。

 功能特点
- 角色定制：支持自定义 AI 的昵称与性格。
- 流式输出：像微信一样流畅的打字机对话体验。
- 持久化记忆：支持保存历史会话，随时继续聊天。

  技术栈
- 语言: Python 3.x
- 大模型: DeepSeek-V3 API
- Web 框架: Streamlit
- 工具库: OpenAI Python SDK, python-dotenv

 快速开始
1. 克隆项目：`git clone https://github.com/ruoyeli/ai-agent-learn.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 配置环境：在 `.env` 中填入你的 `DEEPSEEK_API_KEY`
4. 运行应用：`streamlit run main.py`
