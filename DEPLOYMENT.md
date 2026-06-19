# Deployment Guide

This project is designed to run locally as a Model Context Protocol (MCP) server. It can also be deployed to a cloud host if you want 24/7 availability.

## Local Deployment (Recommended)

1. Open a terminal in the repository folder.
2. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Start the MCP server:

```powershell
python server.py
```

5. Keep the terminal open while the server runs.

---

## Cloud Deployment (Optional)

If you want the MCP server to remain available while your computer is off, deploy it to a cloud host.

### Common deployment options:
- Replit
- Railway
- Heroku
- AWS EC2 / Lightsail

### General steps:
1. Push your repository to GitHub.
2. Create a cloud project on your chosen host.
3. Configure the host to use Python 3.10+.
4. Install dependencies from `requirements.txt`.
5. Run `python server.py` as the service start command.
6. Update your MCP client configuration to use the host URL or local command.

> Note: This repo does not include hosted API proxy code. The MCP server is primarily intended to run locally unless you add a cloud deployment wrapper.
