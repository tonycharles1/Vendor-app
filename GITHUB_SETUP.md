# Step-by-Step: GitHub Repository Setup

## Part 1: Create GitHub Repository

### Step 1: Go to GitHub
1. Open your web browser
2. Go to [github.com](https://github.com)
3. Sign in (or create an account if you don't have one - it's free)

### Step 2: Create New Repository
1. Click the **"+"** icon in the top right corner
2. Select **"New repository"**

### Step 3: Fill Repository Details
- **Repository name**: `cafeteria-vendor-dashboard` (or any name you like)
- **Description**: (Optional) "XPRESS SGS Vendor Dashboard"
- **Visibility**: Select **"Public"** (required for free Streamlit Cloud)
- **DO NOT** check "Initialize with README" (we already have files)
- **DO NOT** add .gitignore or license (we already have them)

### Step 4: Create Repository
- Click the green **"Create repository"** button

### Step 5: Copy the Repository URL
- You'll see a page with setup instructions
- Copy the repository URL (it looks like: `https://github.com/YOUR_USERNAME/cafeteria-vendor-dashboard.git`)
- Save this URL - you'll need it in the next step!

---

## Part 2: Push Your Code to GitHub

### Open Terminal/PowerShell in Your Project Folder

**On Windows:**
1. Open PowerShell or Command Prompt
2. Navigate to your project folder:
   ```powershell
   cd "C:\Users\tonyc\OneDrive\Desktop\Cafateria"
   ```

### Run These Commands One by One:

```bash
# 1. Initialize git (if not already done)
git init

# 2. Add all files
git add .

# 3. Create first commit
git commit -m "Initial commit - Vendor Dashboard"

# 4. Rename branch to main
git branch -M main

# 5. Add your GitHub repository (REPLACE WITH YOUR ACTUAL URL)
git remote add origin https://github.com/YOUR_USERNAME/cafeteria-vendor-dashboard.git

# 6. Push to GitHub
git push -u origin main
```

**Note**: When you run `git push`, GitHub will ask for your username and password. 
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your GitHub password)
  - How to create one: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
  - Give it "repo" permissions
  - Copy the token and use it as password

---

## Part 3: Deploy to Streamlit Cloud

### Step 1: Go to Streamlit Cloud
1. Open [share.streamlit.io](https://share.streamlit.io) in your browser
2. Click **"Sign in"**
3. Sign in with your **GitHub account**

### Step 2: Create New App
1. Click the **"New app"** button (usually top right or in dashboard)

### Step 3: Select Repository
You'll see a form with these fields:

1. **Repository**: 
   - Click the dropdown
   - You'll see a list of your GitHub repositories
   - **Select**: `YOUR_USERNAME/cafeteria-vendor-dashboard` (or whatever you named it)
   - If you don't see it, make sure you pushed your code successfully

2. **Branch**: 
   - Leave as `main` (default)

3. **Main file path**: 
   - Type: `vendor_dashboard.py`
   - This is your main dashboard file

4. **App URL** (optional):
   - You can customize this or leave it as default
   - Example: `https://cafeteria-dashboard.streamlit.app`

### Step 4: Deploy
1. Click the **"Deploy"** button
2. Wait 2-3 minutes for deployment
3. You'll see a success message when done!

### Step 5: Access Your Live App
- Your app will be available at: `https://YOUR_APP_NAME.streamlit.app`
- Share this link with anyone!

---

## Troubleshooting

### "Repository not showing in dropdown"
- Make sure you pushed your code to GitHub
- Check that the repository is **Public** (not Private)
- Try refreshing the Streamlit Cloud page

### "Git push failed"
- Make sure you're using a Personal Access Token (not password)
- Check that you copied the correct repository URL
- Verify your internet connection

### "App deployment failed"
- Check that `vendor_dashboard.py` exists in your repository
- Verify all dependencies are in `requirements.txt`
- Check the deployment logs in Streamlit Cloud dashboard

---

## Need Help?

If you get stuck at any step, let me know which step and what error message you see!


