# Employee Lifecycle AI (Lifecycle AI)

A premium Employee Lifecycle Automation system featuring an AI Assistant for natural language processing and an MCP-based Automation Engine for executing lifecycle tasks (onboarding, offboarding, transfers).

## 🚀 Key Features
- **AI-Powered Orchestration**: Natural language understanding for complex HR workflows.
- **MCP Automation Node**: Model Context Protocol based server for reliable tool execution.
- **Premium UI**: Modern, glassmorphic dashboard with a full-screen assistant experience.
- **Mock Integrations**: Pre-configured mock adapters for Active Directory, GitLab, Workday, and Slack.

## 🛠 Tech Stack
- **Backend**: Python, Flask
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Deployment**: Docker, AWS App Runner

## 📦 Local Setup
1. **Clone & Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Application**:
   ```bash
   python src/app/server.py
   ```
3. **Access**: Open `http://localhost:5000` in your browser.

## ☁️ Cloud Deployment
The project is containerized and ready for **AWS App Runner**.
- Build command: `pip install -r requirements.txt`
- Start command: `python src/app/server.py`
- Port: `5000`

See `aws_deployment_guide.md` for detailed instructions.
