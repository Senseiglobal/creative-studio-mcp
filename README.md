# Welcome to Creative Studio MCP

<p>
  <a href="https://github.com/sponsors/Senseiglobal">
    <img src="https://img.shields.io/badge/Support%20Us-GitHub%20Sponsors-brightgreen?style=for-the-badge" alt="Support Us on GitHub Sponsors">
  </a>
</p>

## Developer Information

**Developer:** Thomas Ogun

**Organization:** Senseiglobal

**GitHub Repository:** https://github.com/Senseiglobal/creative-studio-mcp

Creative Studio MCP is developed to help creative professionals, freelancers, design studios, agencies, print shops, and small businesses reduce admin work and manage client-ready business tasks with AI.

Your support helps fund ongoing open-source improvements, documentation, testing, mobile app development, and future AI-powered business tools.

## Project Roadmap and Feedback

Visual start page: [START_HERE.html](START_HERE.html)

Windows setup check: [CHECK_INSTALL.bat](CHECK_INSTALL.bat)

Read the roadmap: [ROADMAP.md](ROADMAP.md)

Share feedback: [FEEDBACK.md](FEEDBACK.md)

Installer guide: [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md)

Join the community: https://github.com/Senseiglobal/creative-studio-mcp/discussions

## What Is This?

**Creative Studio MCP** is a smart business assistant that helps creative professionals automate everyday work.

Instead of typing the same information over and over, this tool does it for you automatically. It works with AI assistants like ChatGPT or Claude, so your AI can help you generate quotes, calculate payments, organize projects, and list your services - instantly.

### Think of it like this:

**Before:** You spend 20 minutes manually creating a quote for each client.

**After:** You type one request to ChatGPT, and a professional quote appears in 5 seconds.

---

## Who Is This For?

This tool is designed for creative professionals and small businesses:

✔ **Graphic Designers** to Generate quotes and project plans instantly

✔ **Branding Agencies** to Automate quote creation and client communications

✔ **Freelance Creatives** to Reduce time spent on admin work

✔ **Marketing Teams** to Standardize pricing and proposals

✔ **Print Shops** to Calculate costs and payment terms automatically

✔ **Design Studios** to Keep projects organized and consistent

✔ **Virtual Assistants** to Help clients with quote automation

✔ **Small Business Owners** to Save hours every week on repetitive tasks

✔ **Students** to Learn how AI automation works

---

## How This Helps Your Business

### ⏱️ Save Time

Stop spending 15+ minutes creating each quote. Let AI do it in seconds.

### 💰 Make More Money

Respond to client inquiries faster. Close more deals. Handle more projects.

### 📋 Stay Organized

Every project follows the same checklist. Nothing gets forgotten.

### 🎯 Be Consistent

Your pricing, payment terms, and process are always the same - no mistakes.

### 📱 Work Anywhere

Use this tool with ChatGPT on your phone, laptop, or tablet.

### 🤖 Work Smarter, Not Harder

Let AI handle the repetitive work so you can focus on creative work.

---

## What Can This Tool Do?

This tool helps you with 4 main tasks:

### 1. Show Your Services & Pricing

You can ask your AI: *"What services do we offer?"*

The AI instantly shows:
```
Brand Identity Design: $500 to $2,500+
Product Packaging Design: $400 to $1,500+
Corporate Profile Design: $300 to $1,200+
...and more
```

### 2. Calculate Payment Breakdowns

You ask: *"What's the payment breakdown for a $5,000 project?"*

The AI instantly shows:
```
Upfront payment (70%): $3,500
Balance payment (30%): $1,500
```

### 3. Generate Professional Quotes

You ask: *"Create a quote for John Smith for brand design at $3,000"*

The AI generates a complete, professional quote you can send directly to your client.

### 4. Create Project Checklists

You ask: *"Generate a checklist for a branding project"*

The AI creates a step-by-step checklist so nothing is forgotten.

---

## Do I Need to Know Programming?

**No.** You do not need to know how to code.

You just need to:
1. Download the files (instructions below)
2. Follow the setup steps
3. Paste the files into ChatGPT or Claude
4. Ask questions in plain English

That's it. Everything else is automatic.

---

## What Do I Need Before I Start?

Just three things:

1. **A computer** (Windows, Mac, or Linux)
2. **An internet connection** (to download and use ChatGPT/Claude)
3. **30 minutes of time** (for the first setup - then it's automatic)

**Optional but recommended:**
- ChatGPT Plus subscription ($20/month) OR Claude subscription
- A Google account (to back up your work)

---

---

## 1-Minute Setup (Automated)

The easiest way to install: **Double-click one file and everything is done automatically.**

For a fuller walkthrough, read [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md).

### Step 1: Download Python (2 minutes)

**What is Python?** Python is the software that powers this tool.

1. Go to https://www.python.org/downloads/
2. Click the big "Download Python" button
3. Install it (use all the default options)
4. **What success looks like:** Python is installed on your computer

---

### Step 2: Download This Project (1 minute)

1. Go to https://github.com/Senseiglobal/creative-studio-mcp
2. Click the green "Code" button
3. Click "Download ZIP"
4. Save it to your computer
5. Right-click the ZIP file and choose "Extract All"
6. **What success looks like:** A folder called `creative-studio-mcp` on your computer

---

### Step 3: Run the Installer (1 minute)

#### On Windows:
1. Open your `creative-studio-mcp` folder
2. Double-click `install.bat`
3. Wait for it to finish (you'll see "Installation Complete!")
4. **Done!** The installer created everything you need.

If you use PowerShell manually, make sure the terminal is inside the project folder:

```powershell
cd "C:\Users\User\creative-studio-mcp"
.\install.bat
```

#### On Mac/Linux:
1. Open Terminal in your `creative-studio-mcp` folder
2. Type this one command:
   ```
   bash install.sh
   ```
3. Wait for it to finish (you'll see "Installation Complete!")
4. **Done!** The installer created everything you need.

---

## Alternative: Manual Setup (for technical users)

If you prefer to set up manually instead of using the installer:

### Step 1: Download Python (2 minutes)

1. Go to https://www.python.org/downloads/
2. Click the big "Download Python" button
3. Install it (use all the default options)

---

### Step 2: Open Terminal

**What is Terminal?** Terminal is where you type commands for your computer.

#### On Windows:
1. Open File Explorer
2. Go to your `creative-studio-mcp` folder
3. Press `Shift + Right Click` in the empty space
4. Choose "Open PowerShell window here"

#### On Mac:
1. Open Finder
2. Go to `creative-studio-mcp` folder
3. Right-click and select "New Terminal at Folder"

#### On Linux:
1. Open your file manager
2. Right-click in the folder
3. Select "Open Terminal Here"

---

### Step 3: Run Setup Commands

Copy each command below and paste it into your terminal. Press Enter after each one.

**Command 1: Create the workspace**
```
python -m venv .venv
```
**What it does:** Creates a special folder for this project's software.

---

**Command 2: Install the software**

On Windows:
```
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On Mac/Linux:
```
.venv/bin/python -m pip install -r requirements.txt
```

**What it does:** Installs the software this project needs without using the PowerShell activation command.

---

**Command 3: Check the server file**

On Windows:
```
.\.venv\Scripts\python.exe -m py_compile server.py
```

On Mac/Linux:
```
.venv/bin/python -m py_compile server.py
```

**What it does:** Checks that the server file is valid.

---

## Test It Works

Type this command:

On Windows:
```
.\.venv\Scripts\python.exe server.py
```

On Mac/Linux:
```
.venv/bin/python server.py
```

**What success looks like:**
```
Listening on stdio
```

If you see that message, your setup worked! Press `Ctrl + C` to stop it.

---

## Optional - Set Up Your OpenAI API Key

**What is an API key?** It's a password that lets ChatGPT know you're allowed to use it.

If you want to use ChatGPT with this tool:

1. Go to https://platform.openai.com/api/keys
2. Create a new API key
3. Copy the key
4. Open the `.env` file in your `creative-studio-mcp` folder
5. Find the line `OPENAI_API_KEY=`
6. Paste your key after the `=` sign, like this:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```
7. Save the file

**Never share your API key with anyone.** It's like your password.

---

## Understanding OpenAI and API Keys

### What is OpenAI?

OpenAI is a company that makes AI tools like ChatGPT. You probably use their chatbot on https://chat.openai.com

### What is an API Key?

Think of an API key like this:
- Your house has a lock and key
- An API key is like a special key that lets software access OpenAI's services
- Only you should have your API key

### Do I Need an API Key?

**Only if you want to:**
- Use ChatGPT programmatically (have code talk to ChatGPT)
- Build a website that uses ChatGPT
- Automate ChatGPT

**You don't need an API key if you just want to:**
- Use Claude Desktop with this tool
- Copy and paste quotes into ChatGPT manually

### How Much Does It Cost?

- **ChatGPT Plus:** $20/month
- **ChatGPT API:** You pay per usage (usually $0.01 to $0.10 per request)
- **Claude Desktop:** Free with account creation
- **Claude API:** You pay per usage

For small creative businesses, the cost is usually less than $5/month.

### Is My API Key Private?

**Yes, but be careful:**
- Never share it on the internet
- Never put it in code you publish on GitHub
- Always keep it in a `.env` file (which we exclude from GitHub)
- If you accidentally share it, create a new one immediately at https://platform.openai.com/api/keys

---

## Connecting to ChatGPT or Claude

### Option 1: Use Claude Desktop (Recommended for Beginners)

Claude is a free AI chatbot made by Anthropic. This tool works best with Claude.

1. Download Claude from https://claude.ai
2. Create a free account
3. Follow the instructions in `QUICK_START.md` to connect this tool
4. Start asking Claude questions about your quotes and projects

### Option 2: Use ChatGPT

If you prefer ChatGPT, you can copy and paste quotes into ChatGPT manually, or follow the setup in `INTEGRATION_GUIDE.md` to automate it.

---

## How to Use This Tool

### Example 1: Generate a Quote

**You ask Claude:** 
```
"Create a quote for John Smith for Brand Identity Design at $3,000. Printing not included."
```

**Claude responds:**
```
Hello John,

Thank you for your interest in our creative services.

Service: Brand Identity Design
Creative Design Fee: $3,000

Payment Terms:
70% upfront ($2,100) before project commencement
30% balance ($900) before final delivery

Printing/production is not included and will be quoted separately after design approval.

Best regards,
Thomas Ogun
```

**You do:** Copy this text and send it to your client.

---

### Example 2: Calculate Payment

**You ask Claude:**
```
"Calculate the payment breakdown for a $5,000 project with 70% upfront."
```

**Claude responds:**
```
Total project fee: $5,000
Upfront payment (70%): $3,500
Balance payment (30%): $1,500
```

**You do:** Add this to your invoice or send it to your client.

---

### Example 3: Create a Project Checklist

**You ask Claude:**
```
"Generate a project checklist for product packaging design."
```

**Claude responds:**
```
1. Confirm project type: Product Packaging Design
2. Confirm client brief and packaging goals
3. Collect reference materials and content
4. Define deliverables
5. Confirm design direction with client
6. Create first draft
7. Review client feedback
8. Apply revisions
9. Prepare final print-ready files
10. Confirm printing/production separately if needed
```

**You do:** Copy this into your project management tool or send to your team.

---

## Frequently Asked Questions

### Do I really need to know programming?
**No.** You just need to follow the setup steps and ask questions in plain English. No coding required.

### Can I use this on my Mac?
**Yes.** Follow the Mac setup instructions in Step 3 above.

### Can I use this on Linux?
**Yes.** Follow the Linux setup instructions in Step 3 above.

### Can I use this without ChatGPT or Claude?
**Yes, but it's less useful.** This tool works best with AI assistants. You can use Claude Desktop for free.

### What if I don't have a ChatGPT Plus subscription?
**No problem.** You can use Claude Desktop instead (free) or use the free version of ChatGPT (slower, but works).

### How much will this cost me?
**Setup:** Free
**Monthly:** Depends on your AI choice
- Claude Desktop: Free
- ChatGPT Plus: $20/month
- Usage-based APIs: Usually $0 to $5/month for small businesses

### What if I lose my API key?
**Create a new one immediately.** Go to https://platform.openai.com/api/keys and delete the old key. Create a new one and update your `.env` file.

### How do I update the software?
**Download the latest version from GitHub.** Replace your old files with the new ones. Your pricing and settings are in `server.py`, so save a backup first.

### Can my team use this?
**Yes.** Store it on GitHub and each team member can download it. Or share the folder via Google Drive or Dropbox.

### Can I customize the pricing?
**Yes.** Open `server.py` in a text editor and change the prices. Save the file and restart the tool.

### How do I know if it's working?
**Run this command:**

On Windows:
```
.\.venv\Scripts\python.exe server.py
```

On Mac/Linux:
```
.venv/bin/python server.py
```

If you see:
```
Listening on stdio
```

It's working. Press `Ctrl + C` to stop.

---

## Troubleshooting

### Problem: "No module named 'mcp'"

**What this means:** The software wasn't installed correctly.

**Solution:**
1. Make sure you ran the commands in Step 4 above
2. Make sure you are inside the `creative-studio-mcp` folder
3. Run this command again:
   ```
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
4. Try `.\.venv\Scripts\python.exe server.py` again

---

### Problem: "Python is not recognized"

**What this means:** Python isn't installed or your computer can't find it.

**Solution:**
1. Go to https://www.python.org/downloads/
2. Download and install Python
3. **Important:** During installation, check the box that says "Add Python to PATH"
4. Restart your terminal
5. Try again

---

### Problem: Claude can't find the server

**What this means:** Claude isn't connected to this tool.

**Solution:**
1. Open the file: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`
2. Find the line with `creative-studio-mcp`
3. Make sure the path is correct (it should point to where you saved the files)
4. Restart Claude Desktop
5. Try again

---

### Problem: Commands aren't working in Terminal

**What this means:** You might be in the wrong folder or terminal type.

**Solution:**
1. Make sure you're in the `creative-studio-mcp` folder
2. Try right-clicking in the folder and choosing "Open Terminal Here" or "Open PowerShell Here"
3. On Windows, you can also click the folder address bar, type `powershell`, and press Enter
4. Try the commands again

---

### Problem: The server starts but Claude doesn't see it

**Solution:**
1. Stop the server: Press `Ctrl + C`
2. Reinstall the software:
   ```
   .\.venv\Scripts\python.exe -m pip install --upgrade mcp
   ```
3. Start it again:
   ```
   .\.venv\Scripts\python.exe server.py
   ```

---

## Next Steps

### Today (30 minutes)
- [ ] Follow the 5-Minute Setup above
- [ ] Test by running `.\.venv\Scripts\python.exe server.py` on Windows
- [ ] Create your first test quote

### This Week (1 hour)
- [ ] Connect to Claude Desktop (see `QUICK_START.md`)
- [ ] Generate 5 real quotes for your business
- [ ] Backup your files to Google Drive

### Next Week (2 hours)
- [ ] Read `INTEGRATION_GUIDE.md` to add to your website
- [ ] Create social media content using this tool
- [ ] Share with your team

---

## Getting Help

### If something isn't working:
1. Check the Troubleshooting section above
2. Read `QUICK_START.md` for beginners
3. Check `DEPLOYMENT.md` for advanced setup

### Learn more about:
- **MCP (what powers this):** https://modelcontextprotocol.io/
- **Python (the software language):** https://python.org/docs/
- **Claude (the AI assistant):** https://claude.ai
- **ChatGPT (the other AI assistant):** https://chat.openai.com

---

## Ready to Get Started?

Go to the **5-Minute Setup** section above and follow the steps. You'll be done in no time!

**Questions?** Check the FAQ section above, or read `QUICK_START.md` for more details.

---

**Last updated:** June 19, 2026

**Made for creative professionals who want to work smarter, not harder.**
