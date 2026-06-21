# Security Policy

Creative Studio MCP is designed to run locally on your computer.

## What This App Does

- Opens a local browser app on your own computer.
- Saves your projects locally in `projects.json`.
- Saves your business settings locally in `brand_profile.json`.
- Does not require Claude, OpenAI, or internet access to use the local app.

## What This App Should Not Do

This project should not:

- Ask for your Windows admin password.
- Ask you to disable antivirus.
- Ask you to turn off Windows security.
- Upload your private files.
- Send your business database to a remote server.
- Require you to share your `.env`, `projects.json`, or `brand_profile.json`.

## Safe Download Steps

1. Download only from the official repository:

   https://github.com/Senseiglobal/creative-studio-mcp

2. Extract the ZIP file before running anything.
3. Open the folder and run:

   ```text
   SECURITY_CHECK.bat
   ```

4. If the check looks normal, run:

   ```text
   START_APP.bat
   ```

## Windows Safety Notes

Windows may warn you because this is an open-source script, not a paid signed installer.

That warning does not automatically mean it is malware.

Still, do not run the app if:

- You downloaded it from a random website.
- The file names look different from the GitHub repo.
- Someone sent you a modified ZIP privately.
- Your antivirus says a file is dangerous.

## Private Files

Do not upload or share these files:

```text
.env
brand_profile.json
projects.json
deleted_projects.json
exports
```

## Reporting Security Issues

If you find a security problem, open a GitHub issue or discussion without posting private keys, client data, or passwords.

Repository:

https://github.com/Senseiglobal/creative-studio-mcp
