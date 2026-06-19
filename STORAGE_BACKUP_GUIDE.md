# Backup & Storage Guide

**Protect your work so you never lose it.**

---

## Why Backup?

Your tool is on your computer right now. If your computer:
- Crashes
- Gets stolen
- Gets damaged
- Has a hard drive failure

...you lose everything.

**But if you back it up to the cloud, you're safe.** This guide shows you how.

---

## Quick Backup (5 Minutes)

### Option 1: Google Drive (Easiest)

Google Drive automatically backs up your files to Google's servers.

**Setup:**
1. Go to https://www.google.com/drive/download/
2. Download Google Drive for Desktop
3. Install it
4. Log in with your Google account
5. Drag your `creative-studio-mcp` folder into Google Drive
6. Done! Files automatically back up every time you save

**Cost:** Free (15 GB), then $2-$20/month for more storage
**Best for:** Beginners, ease of use

---

### Option 2: OneDrive (If You Have Windows)

OneDrive comes with Windows and automatically backs up files.

**Setup:**
1. Open File Explorer
2. Look for "OneDrive" in the sidebar
3. Drag your `creative-studio-mcp` folder into OneDrive
4. Done! Files automatically back up

**Cost:** Free (5 GB), then $1.99+/month for more storage
**Best for:** Windows users

---

### Option 3: Dropbox

Dropbox is similar to Google Drive but with less free storage.

**Setup:**
1. Go to https://www.dropbox.com/download
2. Download Dropbox
3. Install it
4. Log in
5. Drag your `creative-studio-mcp` folder into Dropbox
6. Done!

**Cost:** Free (2 GB), then $9.99+/month for more storage
**Best for:** Teams who want shared backups

---

## Better Backup (GitHub + Cloud)

### What is GitHub?

GitHub is a place to store code and files on the internet. It's free.

**Benefits:**
- Free backup
- Share with your team
- Keep version history (go back to old versions)
- Deploy to the cloud later

---

### How to Set Up GitHub (15 Minutes)

#### Step 1: Create a GitHub Account (Free)
1. Go to https://github.com
2. Click "Sign up"
3. Create an account (use your email)
4. Verify your email

#### Step 2: Create a Repository (Storage Space)
1. Log into GitHub
2. Click the "+" icon → "New repository"
3. Name it: `creative-studio-mcp`
4. Description: "MCP server for creative business automation"
5. Choose "Private" (only you can see) or "Public" (anyone can see)
6. Click "Create repository"

#### Step 3: Install Git

**What is Git?** It's a tool that uploads your files to GitHub.

**On Windows:**
1. Go to https://git-scm.com/download/win
2. Download and install (use all defaults)
3. Restart your terminal

**On Mac:**
1. Go to https://git-scm.com/download/mac
2. Download and install
3. Restart your terminal

**On Linux:**
```
sudo apt install git
```

#### Step 4: Upload Your Files to GitHub

Open Terminal and run these commands:

```
cd creative-studio-mcp
```
(Go into your project folder)

```
git init
```
(Initialize Git)

```
git add .
```
(Add all files)

```
git commit -m "Initial commit: Creative Studio MCP"
```
(Create a backup snapshot)

```
git branch -M main
```
(Use the main branch)

GitHub will show you a command like:
```
git remote add origin https://github.com/YOUR-USERNAME/creative-studio-mcp.git
```

Paste that command.

Then:
```
git push -u origin main
```
(Upload to GitHub)

**Success:** Go to https://github.com/YOUR-USERNAME/creative-studio-mcp and you see your files!

---

## Best Backup Strategy (For Peace of Mind)

Combine multiple backups:

1. **Cloud backup (automatic):** Google Drive or OneDrive
   - Runs every time you save
   - Requires internet

2. **GitHub (version control):** Push once per week
   - Keep history of changes
   - Share with team
   - Free

3. **External drive (offline):** USB drive, external hard drive
   - Manual backup once per month
   - Works offline
   - Good for disaster recovery

**Example routine:**
- Every day: Work on files (Google Drive auto-backs up)
- Every Friday: Push to GitHub (`git add . && git commit -m "Weekly" && git push`)
- Every month: Copy to USB drive

---

## Moving Your Files

If you want to move this tool to a different location:

### Moving to a Different Folder

1. Cut the `creative-studio-mcp` folder (right-click → Cut)
2. Paste it in the new location
3. Update the path in Claude's config:
   - Find: `C:\Users\YourName\AppData\Roaming\Claude\claude_desktop_config.json`
   - Update the "args" path to your new location
4. Restart Claude

### Moving Between Computers

**Easy method:**
1. Back up to GitHub (see above)
2. On new computer: `git clone https://github.com/YOUR-USERNAME/creative-studio-mcp.git`
3. Run the setup again: `python -m venv .venv`, then `pip install -r requirements.txt`
4. Done!

---

## Backup Checklist

**Weekly:**
- [ ] Google Drive has new files (check it's running)
- [ ] Test your tool works

**Monthly:**
- [ ] Push to GitHub (`git push`)
- [ ] Copy to external drive
- [ ] Review your backup folder

**Yearly:**
- [ ] Test restoring from backup
- [ ] Clean up old backups

---

## If You Lose Your Files

### From Google Drive
1. Go to https://drive.google.com
2. Find your `creative-studio-mcp` folder
3. Download it
4. Extract and use it

### From GitHub
```
git clone https://github.com/YOUR-USERNAME/creative-studio-mcp.git
```

### From External Drive
1. Plug in external drive
2. Copy the folder back to your computer

---

## Sharing With Your Team

If you want your team to use this tool:

### Option 1: GitHub (Best for Teams)
1. Put it on GitHub (see setup above)
2. Each team member clones it: `git clone [repo-url]`
3. Everyone runs the setup steps
4. Everyone has the same tool

### Option 2: Google Drive / Dropbox
1. Move your tool to Google Drive or Dropbox
2. Share the folder with your team
3. They access it directly from there

### Option 3: Email
1. Zip your folder
2. Email to your team
3. They extract and set up locally

**Best method:** GitHub (easier to manage updates)

---

## Cost Comparison

| Backup Type | Cost | Setup Time | Automatic | Best For |
|-------------|------|-----------|-----------|----------|
| Google Drive | Free–$20/mo | 5 min | Yes | Beginners |
| OneDrive | Free–$2/mo | 5 min | Yes | Windows users |
| Dropbox | Free–$10/mo | 5 min | Yes | Teams |
| GitHub | Free | 15 min | No (manual) | Code + teams |
| External Drive | $30–$100 (one-time) | 5 min | No (manual) | Offline backup |

---

## My Recommendation

**For Most People:**
- Google Drive (automatic, easy)
- + GitHub (free backup, version history)

**For Teams:**
- GitHub (everyone can access)
- + Google Drive (extra backup)

**For Maximum Safety:**
- Google Drive (automatic)
- + GitHub (version control)
- + External drive (offline backup)

---

## Questions?

### I'm worried I'll lose my API key
**Don't worry.** Your API key is in the `.env` file, which is never uploaded to GitHub (it's in `.gitignore`). Only the `.env.example` file is public.

### Can I use multiple cloud services?
**Yes.** You can have your files in Google Drive AND GitHub. They don't conflict.

### How much space does this take up?
About 100 MB (mostly from the `.venv` folder). The important code is only about 10 KB.

### What if I delete my GitHub repository?
Go to Settings → Danger Zone → Delete Repository. You can restore from Google Drive or your external drive.

### Can my team edit the code?
**On GitHub:** Yes, if they have permission. Use GitHub's collaboration features.
**On Google Drive:** Yes, but not recommended (can get messy).

---

## Next Steps

1. **Today:** Set up Google Drive backup (5 minutes)
2. **This Week:** Set up GitHub backup (15 minutes)
3. **This Month:** Set up external drive backup (optional)
4. **Ongoing:** Check your backups monthly

---

**Your work is now protected. You can focus on creating instead of worrying about losing your tool.**

**Last updated:** June 19, 2026
