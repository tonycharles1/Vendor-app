# 🚀 Quick Start Guide - Make Your Dashboard Live

## Step 1: Install Git (If Not Installed)

### For Windows:
1. Go to [git-scm.com/download/win](https://git-scm.com/download/win)
2. Download Git for Windows
3. Run the installer (use default settings)
4. Restart your computer after installation

**OR** use GitHub Desktop (easier):
1. Go to [desktop.github.com](https://desktop.github.com)
2. Download GitHub Desktop
3. Install and sign in with GitHub account

---

## Step 2: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Fill in:
   - **Name**: `cafeteria-dashboard` (or any name)
   - **Visibility**: **Public** ✅
   - **DO NOT** check any boxes (README, .gitignore, license)
4. Click **"Create repository"**
5. **Copy the repository URL** (looks like: `https://github.com/YOUR_USERNAME/cafeteria-dashboard.git`)

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. Click **"File"** → **"New repository"**
3. Fill in:
   - **Name**: `cafeteria-dashboard`
   - **Local path**: `C:\Users\tonyc\OneDrive\Desktop\Cafateria`
   - **GitHub**: Check "Publish this repository"
   - Make it **Public**
4. Click **"Create repository"** then **"Publish repository"**

---

## Step 3: Push Your Code

### If Using Command Line (After Git is installed):

```bash
cd "C:\Users\tonyc\OneDrive\Desktop\Cafateria"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cafeteria-dashboard.git
git push -u origin main
```

### If Using GitHub Desktop:

1. Open GitHub Desktop
2. Click **"File"** → **"Add Local Repository"**
3. Select your folder: `C:\Users\tonyc\OneDrive\Desktop\Cafateria`
4. Click **"Publish repository"** (make it Public)
5. Done! Your code is now on GitHub

---

## Step 4: Deploy to Streamlit Cloud

1. **Go to**: [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. Click **"New app"** button
4. **Select Repository**:
   - Click the dropdown under "Repository"
   - You'll see all your GitHub repositories
   - **Select**: `YOUR_USERNAME/cafeteria-dashboard` (or whatever you named it)
5. **Main file path**: Type `vendor_dashboard.py`
6. **App URL**: (Optional) You can customize or leave default
7. Click **"Deploy"**
8. Wait 2-3 minutes
9. **Done!** Your app is live at `https://YOUR_APP_NAME.streamlit.app`

---

## Visual Guide: Selecting Repository in Streamlit Cloud

When you click "New app" in Streamlit Cloud, you'll see a form like this:

```
┌─────────────────────────────────────────┐
│ Repository: [Dropdown ▼]               │
│   └─ Select: cafeteria-dashboard       │
│                                          │
│ Branch: [main ▼]                        │
│                                          │
│ Main file path: [vendor_dashboard.py]   │
│                                          │
│ App URL: [cafeteria-dashboard ▼]       │
│                                          │
│          [Deploy] Button                 │
└─────────────────────────────────────────┘
```

**In the Repository dropdown**, you'll see:
- All your GitHub repositories
- Search/filter option
- Select the one you just created

---

## ⚠️ Important Notes:

1. **Repository must be Public** for free Streamlit Cloud
2. **Make sure you pushed all files** to GitHub first
3. **Main file path** must be exactly: `vendor_dashboard.py`

---

## 🎯 Quick Checklist:

- [ ] Git installed OR GitHub Desktop installed
- [ ] GitHub account created
- [ ] Repository created on GitHub (Public)
- [ ] Code pushed to GitHub
- [ ] Signed in to Streamlit Cloud
- [ ] Selected repository in dropdown
- [ ] Set main file to `vendor_dashboard.py`
- [ ] Clicked "Deploy"
- [ ] Got live URL! 🎉

---

## Need Help?

If you're stuck at any step, tell me:
1. Which step you're on
2. What you see on your screen
3. Any error messages

I'll help you through it!

