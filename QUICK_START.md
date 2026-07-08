# ⚡ Quick Start - Deploy to Render in 5 Minutes

## 🎯 What You Need (5 minutes to get)

1. **MongoDB Atlas** (2 min):
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up → Create free cluster → Create database user
   - Network Access → Add IP: `0.0.0.0/0` (Allow all)
   - Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/`

2. **Google Gemini API** (1 min):
   - Go to https://ai.google.dev/
   - Sign in → Get API Key
   - Copy the key

3. **Serper API** (1 min):
   - Go to https://serper.dev/
   - Sign up → Get API key from dashboard

4. **JWT Secret** (30 seconds):
   - Generate random string:
   ```bash
   # PowerShell:
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
   ```

## 🚀 Deploy Now (3 steps)

### Step 1: Push to GitHub (1 minute)
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### Step 2: Create Render Services (2 minutes)
1. Go to https://dashboard.render.com/
2. Click **"New +" → "Blueprint"**
3. Connect your GitHub repository
4. Click **"Apply"**

### Step 3: Add Environment Variables (2 minutes)

**Backend Service** (`founderai-backend`):

Click on the backend service → "Environment" → Add these:

| Variable | Your Value |
|----------|------------|
| `MONGODB_URI` | Paste your MongoDB connection string |
| `JWT_SECRET_KEY` | Paste the random string you generated |
| `GEMINI_API_KEY` | Paste your Gemini API key |
| `SERPER_API_KEY` | Paste your Serper API key |
| `FRONTEND_ORIGIN` | `https://founderai-frontend.onrender.com` |

**Frontend Service** (`founderai-frontend`):

Click on the frontend service → "Environment" → Add this:

| Variable | Your Value |
|----------|------------|
| `VITE_API_BASE_URL` | `https://founderai-backend.onrender.com` |

> **Note**: Replace `founderai-backend` and `founderai-frontend` with your actual service names if different.

### Step 4: Wait for Build (5-10 minutes)
- Render will automatically build and deploy
- Watch the logs for progress
- Services will show "Live" when ready

## ✅ Verify Deployment

1. **Backend**: Visit `https://your-backend.onrender.com/health`
   - Should return: `{"status":"ok","service":"founderai-backend"}`

2. **API Docs**: Visit `https://your-backend.onrender.com/docs`

3. **Frontend**: Visit `https://your-frontend.onrender.com`

## 🎉 You're Live!

Your FounderAI app is now running on Render!

## ⚠️ Important Notes

### Free Tier Limitations
- Services sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for continuous operation)

### After Deployment
- Save your service URLs
- Test the application thoroughly
- Monitor the logs for any errors

## 🐛 Something Not Working?

### Backend Won't Start
1. Check logs in Render dashboard
2. Verify all environment variables are set
3. Ensure MongoDB connection string is correct
4. Check MongoDB IP whitelist includes `0.0.0.0/0`

### Frontend Can't Connect to Backend
1. Update `FRONTEND_ORIGIN` in backend to exact frontend URL (with https://)
2. Update `VITE_API_BASE_URL` in frontend to exact backend URL (with https://)
3. Redeploy both services

### More Help
- See `DEPLOYMENT.md` for detailed troubleshooting
- Check Render logs for specific errors
- Review `README.md` for full documentation

## 📋 Quick Reference

### Your Service URLs (fill in after deployment):
- **Backend**: https://__________________.onrender.com
- **Frontend**: https://__________________.onrender.com
- **API Docs**: https://__________________.onrender.com/docs

### Your API Keys (keep secure):
- **MongoDB URI**: mongodb+srv://...
- **Gemini Key**: AIzaSy...
- **Serper Key**: ...
- **JWT Secret**: ...

---

**Need detailed instructions?** See `DEPLOYMENT.md`  
**Need full documentation?** See `README.md`
