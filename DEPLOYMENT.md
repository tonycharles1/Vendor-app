# Quick Deployment Guide

## Option 1: Streamlit Cloud (Easiest - Recommended) ⭐

### Prerequisites:
- GitHub account
- All your code in a GitHub repository

### Steps:

1. **Create GitHub Repository** (if not already done):
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it (e.g., "cafeteria-dashboard")
   - Make it Public (required for free Streamlit Cloud)
   - Don't initialize with README (you already have one)

2. **Push Your Code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

3. **Deploy to Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `vendor_dashboard.py`
   - Click "Deploy"
   - Wait 2-3 minutes for deployment

4. **Your App is Live!**
   - URL format: `https://YOUR_APP_NAME.streamlit.app`
   - Share this link with anyone!

---

## Option 2: Railway.app (Alternative)

1. Sign up at [railway.app](https://railway.app) (free tier available)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects and deploys
6. Get your live URL

---

## Option 3: Render.com (Alternative)

1. Sign up at [render.com](https://render.com)
2. Create "New Web Service"
3. Connect GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run vendor_dashboard.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy and get URL

---

## Important Notes:

- ✅ Streamlit Cloud is FREE and easiest
- ✅ Your app will update automatically when you push to GitHub
- ✅ No credit card required for Streamlit Cloud
- ⚠️ Make sure your GitHub repo is PUBLIC for free Streamlit Cloud
- ⚠️ For private repos, you need Streamlit Cloud Teams (paid)

---

## Troubleshooting:

**Issue: "Module not found"**
- Make sure all dependencies are in `requirements.txt`

**Issue: "App won't start"**
- Check that `vendor_dashboard.py` is the correct filename
- Verify all imports are correct

**Issue: "Connection timeout"**
- Check your DATA_URL is accessible from the internet
- Some APIs may block requests from cloud servers

---

## Need Help?

Check the main README.md for more details!



