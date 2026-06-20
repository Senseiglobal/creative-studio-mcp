# Quick Start Guide for Beginners

**Get this tool working in 10 minutes - no coding experience required.**

---

## Before You Start

Make sure you have:
- ✅ A computer (Windows, Mac, or Linux)
- ✅ Internet connection
- ✅ 30 minutes for the first setup

---

## Step 1: Download Python (2 minutes)

**What is Python?** It's the software that powers this tool. Don't worry - you don't need to understand it.

1. Go to https://www.python.org/downloads/
2. Click the large "Download Python" button (pick the latest version)
3. Run the installer
4. **Important:** Check the box that says "Add Python to PATH"
5. Click "Install"
6. Wait for it to finish

**How to check it worked:**
- Open Terminal (Windows: Command Prompt, Mac: Terminal, Linux: Terminal)
- Type: `python --version`
- You should see: `Python 3.x.x` (3.10 or higher)

---

## Step 2: Download This Tool (2 minutes)

Option A: **From GitHub (if you know Git)**
```
git clone https://github.com/yourusername/creative-studio-mcp.git
cd creative-studio-mcp
```

Option B: **Without Git**
1. Go to https://github.com/yourusername/creative-studio-mcp
2. Click the green "Code" button
3. Click "Download ZIP"
4. Right-click the ZIP and choose "Extract All"
5. A folder called `creative-studio-mcp` appears

**Success looks like:** You have a folder with these files:
- server.py
- README.md
- QUICK_START.md
- requirements.txt
- .env.example
- (and a few others)

---

## Step 3: Open Terminal in Your Project Folder

**What is Terminal?** It's where you type commands to your computer.

### On Windows:
1. Open File Explorer
2. Go to your `creative-studio-mcp` folder
3. Hold `Shift` and right-click in the empty space
4. Choose "Open PowerShell window here"

### On Mac:
1. Open Finder
2. Go to your `creative-studio-mcp` folder
3. Right-click it
4. Select "New Terminal at Folder"

### On Linux:
1. Open your file manager
2. Right-click in the folder
3. Select "Open Terminal Here"

**Success looks like:** A terminal window opens showing your folder path.

On Windows, the path should include `creative-studio-mcp`, like this:

```powershell
PS C:\Users\YourName\creative-studio-mcp>
```

If it only shows something like this:

```powershell
PS C:\Users\YourName>
```

you are in the wrong folder. Open the `creative-studio-mcp` folder in File Explorer, click the address bar, type `powershell`, and press Enter.

---

## Step 4: Run the Setup Commands

Copy each command below and paste it into your terminal. Press Enter after each one.

### Command 1: Create the Python workspace
```
python -m venv .venv
```

**What it does:** Creates a special folder for this project's software.

**Expected output:** No messages, just returns to the prompt.

---

### Command 2: Install the required software

**On Windows:**
```
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**On Mac/Linux:**
```
.venv/bin/python -m pip install -r requirements.txt
```

**What it does:** Installs the software this project needs.

Important for Windows users:

Do not run `.venv\Scripts\Activate.ps1`. Some Windows computers block that file because of PowerShell security settings. The commands in this guide avoid that problem.

---

### Command 3: Check the server file

**On Windows:**
```
.venv\Scripts\python.exe -m py_compile server.py
```

**On Mac/Linux:**
```
.venv/bin/python -m py_compile server.py
```

**What it does:** Checks that the server file is valid.

**Expected output:** No messages, just returns to the prompt.

---

## Step 5: Test Your Installation (2 minutes)

Type this command:

**On Windows:**
```
.venv\Scripts\python.exe server.py
```

**On Mac/Linux:**
```
.venv/bin/python server.py
```

**Expected output:**
```
Listening on stdio
```

This means your setup worked! The server is running.

**To stop the server:** Press `Ctrl + C`

---

## Step 6: Connect to ChatGPT or Claude (3 minutes)

### Option A: Use Claude Desktop (Recommended - it's free)

Claude is a free AI chatbot. This tool works perfectly with it.

1. Go to https://www.anthropic.com/claude
2. Create a free account
3. Download Claude Desktop
4. Open Claude Desktop

Now you can ask Claude questions like:
```
"Generate a quote for John Smith for Brand Identity Design at $3,000"
```

And Claude will use this tool to create a professional quote instantly.

---

### Option B: Use ChatGPT

If you prefer ChatGPT:

1. Go to https://chat.openai.com
2. Sign in or create an account
3. You can copy and paste quotes into ChatGPT manually

For full automation, follow the setup in `INTEGRATION_GUIDE.md`.

---

## Step 7: Create Your First Quote (2 minutes)

Once Claude or ChatGPT is connected, try this:

**Ask Claude:**
```
"Create a quote for ABC Company for Product Packaging Design at $2,000. Don't include printing."
```

**You'll see a professional quote like:**
```
Hello ABC Company,

Thank you for your interest in our creative services.

Service: Product Packaging Design
Creative Design Fee: $2,000

Payment Terms:
70% upfront before project commencement ($1,400)
30% balance before final delivery ($600)

Printing/production is not included and will be quoted separately after design approval.

Best regards,
[Your Name]
```

**You do:** Copy this quote and send it to your client. Done!

---

## That's It! You're Done!

You now have:
- ✅ The tool installed and working
- ✅ Connected to Claude or ChatGPT
- ✅ Created your first professional quote in seconds

---

## Next: Customize Your Information

Your quotes currently use default pricing. To customize them:

1. Open `server.py` in a text editor (Notepad, VS Code, etc.)
2. Find this section:
   ```python
   "Brand Identity Design": "$500 to $2,500+",
   ```
3. Change the prices to yours
4. Save the file
5. Claude will use your new prices next time

---

## Backup Your Work (Important!)

Your tool is on your computer. If your computer crashes, you lose it. Back it up:

### Option 1: Google Drive (Easiest)
1. Install Google Drive from https://www.google.com/drive/download/
2. Drag your `creative-studio-mcp` folder into Google Drive
3. Done! It auto-backs up

### Option 2: OneDrive (Built into Windows)
1. Open File Explorer
2. Drag your `creative-studio-mcp` folder into OneDrive
3. Done!

### Option 3: GitHub (For sharing with team)
1. Create account at https://github.com
2. Create a new repository
3. Follow GitHub's upload instructions
4. Your code is safe in the cloud

---

## Common Issues & Fixes

### "Python is not recognized"
- You didn't check "Add Python to PATH" during installation
- **Solution:** Reinstall Python and check that box

### "No module named 'mcp'"
- Step 3 or 4 didn't work
- **Solution on Windows:** Run `.venv\Scripts\python.exe -m pip install -r requirements.txt` again
- **Solution on Mac/Linux:** Run `.venv/bin/python -m pip install -r requirements.txt` again

### "Server starts but Claude doesn't see it"
- Claude isn't configured correctly
- **Solution:** Read `README.md` → Setup & Configuration section

### Terminal commands aren't working
- You're in the wrong folder
- **Solution:** Right-click your `creative-studio-mcp` folder and choose "Open Terminal Here"
- On Windows, you can also open the folder, click the address bar, type `powershell`, and press Enter

---

## Need More Help?

| Question | Where to Find Help |
|----------|-------------------|
| How do I change my prices? | See "Customize Your Information" above |
| How do I back up my work? | See "Backup Your Work" above |
| How do I use this on my website? | Read `INTEGRATION_GUIDE.md` |
| I'm getting errors | Read `README.md` → Troubleshooting |
| How do I deploy to the cloud? | Read `DEPLOYMENT.md` |

---

## Ready to Use It?

### Today:
- [x] Installed Python
- [x] Downloaded the project
- [x] Ran the setup commands
- [x] Created your first quote

### This Week:
- [ ] Customize your pricing
- [ ] Generate quotes for 5 real clients
- [ ] Back up your work
- [ ] Share with your team (if applicable)

### Next Week:
- [ ] Add it to your website (see `INTEGRATION_GUIDE.md`)
- [ ] Create social media content with it
- [ ] Deploy to cloud for 24/7 access (optional)

---

## One More Thing

**You've just saved yourself hours of work.**

This tool will:
- Generate 100s of quotes with zero errors
- Save you 15+ minutes per quote
- Work 24/7 with AI assistants
- Free up your time for creative work

Enjoy your automation!

---

**Questions?** Email us or check the FAQ in `README.md`.

**Last updated:** June 19, 2026
