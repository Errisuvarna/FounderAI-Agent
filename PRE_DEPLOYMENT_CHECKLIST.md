# ✅ Pre-Deployment Checklist

Before deploying to Render, ensure you have completed all items below.

## 📋 Files Verification

### Required Files (created by fix)
- [ ] `backend/Dockerfile` exists
- [ ] `backend/.dockerignore` exists
- [ ] `render.yaml` exists at root level
- [ ] `.env.example` exists at root level
- [ ] `README.md` exists
- [ ] `DEPLOYMENT.md` exists

### Configuration Files (should already exist)
- [ ] `backend/requirements.txt` exists
- [ ] `backend/app/main.py` exists
- [ ] `frontend/package.json` exists
- [ ] `frontend/vite.config.js` exists

## 🔑 API Keys & Services

### MongoDB Atlas
- [ ] Account created at https://www.mongodb.com/cloud/atlas
- [ ] Free cluster created
- [ ] Database user created with username and password
- [ ] Network access configured (IP whitelist: `0.0.0.0/0`)
- [ ] Connection string obtained (format: `mongodb+srv://...`)
- [ ] Connection string tested (can connect)

### Google Gemini API
- [ ] Account created at https://ai.google.dev/
- [ ] API key generated
- [ ] API key copied and saved securely
- [ ] Gemini API enabled

### Serper API (Web Search)
- [ ] Account created at https://serper.dev/
- [ ] API key obtained from dashboard
- [ ] API key copied and saved securely

### JWT Secret Key
- [ ] Random secure string generated (32+ characters)
- [ ] String saved securely

**Command to generate JWT secret:**
```powershell
# PowerShell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

## 🌐 GitHub Setup

### Repository
- [ ] GitHub account exists
- [ ] Repository created or exists
- [ ] Local repository connected to remote
- [ ] Can push to repository

**Test with:**
```bash
git remote -v
```

## 🔧 Local Testing (Optional but Recommended)

### Backend Test
- [ ] Backend starts locally without errors
- [ ] Health endpoint responds: `http://localhost:8000/health`
- [ ] API docs accessible: `http://localhost:8000/docs`
- [ ] MongoDB connection successful

**Test with:**
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Test
- [ ] Frontend builds without errors
- [ ] Development server starts
- [ ] Can access at `http://localhost:5173`
- [ ] No console errors

**Test with:**
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Render Account Setup

### Account
- [ ] Render account created at https://render.com
- [ ] GitHub account connected to Render
- [ ] Can access Render dashboard

## 📝 Environment Variables Ready

### Backend Variables (prepare these values)
```
MONGODB_URI=_________________________________
MONGODB_DB_NAME=founderai
JWT_SECRET_KEY=________________________________
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
GEMINI_API_KEY=________________________________
GEMINI_MODEL=gemini/gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=models/text-embedding-004
SERPER_API_KEY=________________________________
FRONTEND_ORIGIN=https://founderai-frontend.onrender.com
APP_ENV=production
```

### Frontend Variables (prepare these values)
```
VITE_API_BASE_URL=https://founderai-backend.onrender.com
```

**Note**: Adjust service names if different from default.

## ✅ Verification Steps

### 1. Run Deployment Check
```bash
python check_deployment_ready.py
```

Expected output: `✅ ALL CHECKS PASSED!`

### 2. Verify Git Status
```bash
git status
```

All new files should be untracked or modified.

### 3. Review Changes
```bash
git diff
```

Review all modifications before committing.

## 🚀 Ready to Deploy?

If all items above are checked, you're ready to deploy!

### Quick Deploy Method:
```bash
# Windows
deploy_to_render.bat

# Or manual:
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

Then follow steps in `QUICK_START.md` or `DEPLOYMENT.md`.

## 📚 Documentation Reference

| Need Help With | See Document |
|----------------|--------------|
| Quick 5-minute guide | `QUICK_START.md` |
| Detailed instructions | `DEPLOYMENT.md` |
| What was fixed | `FIXES_APPLIED.md` |
| Complete summary | `RENDER_DEPLOYMENT_SUMMARY.md` |
| Full project docs | `README.md` |
| Environment variables | `.env.example` |

## 🆘 Troubleshooting

### Can't connect to MongoDB
- Verify connection string format
- Check IP whitelist (use `0.0.0.0/0` for testing)
- Verify database user credentials

### API keys not working
- Check keys are copied correctly (no spaces)
- Verify keys are active and have quota
- Check API is enabled

### Git push fails
- Verify remote is set: `git remote -v`
- Check credentials: `git config user.name` and `git config user.email`
- Try: `git push -u origin main`

### Python script fails
- Ensure Python 3.11+ is installed
- Run from project root directory
- Check file permissions

## ⏱️ Time Estimates

- [ ] Getting API keys: ~5 minutes
- [ ] Running checks: ~1 minute
- [ ] Git commit and push: ~1 minute
- [ ] Render setup: ~2 minutes
- [ ] Setting environment variables: ~3 minutes
- [ ] Waiting for deployment: ~10-15 minutes

**Total time**: ~20-25 minutes

## 🎉 Success!

When all checkboxes are completed, you're ready to deploy!

Follow the deployment steps and your FounderAI application will be live on Render.

---

**Last Updated**: July 8, 2026  
**Version**: 1.0  
**Status**: Ready for Deployment
