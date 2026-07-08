# Render Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Files Created/Updated
- [x] `backend/Dockerfile` - Docker configuration for backend
- [x] `backend/.dockerignore` - Ignore unnecessary files in Docker build
- [x] `render.yaml` - Render deployment configuration (at root level)
- [x] `.env.example` - Environment variables template
- [x] `README.md` - Complete documentation

### 2. Required API Keys & Services

Get these before deployment:

1. **MongoDB Atlas** (Free Tier Available)
   - Sign up at: https://www.mongodb.com/cloud/atlas
   - Create a cluster
   - Create a database user
   - Get connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/`)
   - **Important**: Whitelist Render IPs or use 0.0.0.0/0 (all IPs)

2. **Google Gemini API Key** (Free Tier Available)
   - Get key at: https://ai.google.dev/
   - Enable Gemini API
   - Copy API key

3. **Serper API Key** (Free Tier Available)
   - Sign up at: https://serper.dev/
   - Get API key from dashboard

4. **JWT Secret Key**
   - Generate a secure random string:
     ```bash
     # On Linux/Mac:
     openssl rand -hex 32
     
     # On Windows PowerShell:
     -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
     ```

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

### Step 2: Create Render Account
- Go to https://render.com
- Sign up with GitHub
- Connect your GitHub account

### Step 3: Deploy with Blueprint

1. Click "New +" → "Blueprint"
2. Select your repository: `FounderAI-Agent`
3. Render will detect `render.yaml`
4. Click "Apply"

### Step 4: Configure Environment Variables

**For Backend Service (`founderai-backend`):**

Go to the backend service → Environment → Add the following:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `MONGODB_URI` | Your MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `MONGODB_DB_NAME` | Database name | `founderai` |
| `JWT_SECRET_KEY` | Random secure string | `abc123...` (use openssl command) |
| `GEMINI_API_KEY` | Your Gemini API key | `AIzaSy...` |
| `SERPER_API_KEY` | Your Serper API key | `e8f9a...` |
| `FRONTEND_ORIGIN` | Frontend URL | `https://founderai-frontend.onrender.com` |

**For Frontend Service (`founderai-frontend`):**

Go to the frontend service → Environment → Add:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `VITE_API_BASE_URL` | Backend URL | `https://founderai-backend.onrender.com` |

### Step 5: Monitor Deployment

1. Watch the build logs in Render dashboard
2. Both services should show "Live" status when ready
3. Backend health check: `https://your-backend.onrender.com/health`
4. Frontend: `https://your-frontend.onrender.com`

## 🔍 Verifying Deployment

### Backend Health Check
```bash
curl https://your-backend.onrender.com/health
# Should return: {"status":"ok","service":"founderai-backend"}
```

### API Documentation
Visit: `https://your-backend.onrender.com/docs`

### Frontend
Visit: `https://your-frontend.onrender.com`

## 🐛 Troubleshooting

### Build Fails with "No Dockerfile found"
- ✅ **Fixed**: Created `backend/Dockerfile` and updated `render.yaml` with correct paths
- The `render.yaml` must be at the repository root
- Check that `dockerfilePath: ./backend/Dockerfile` is correct

### Backend Service Won't Start

1. **Check Environment Variables**:
   - All required variables set?
   - MongoDB URI format correct?
   - API keys valid?

2. **Check Logs**:
   - Go to service → Logs tab
   - Look for specific error messages

3. **MongoDB Connection Issues**:
   - IP whitelist includes Render IPs (or 0.0.0.0/0)
   - Database user has correct permissions
   - Connection string includes database name

### Frontend Shows Blank Page

1. **Check Console Errors** (Browser DevTools)
2. **Verify Environment Variables**:
   - `VITE_API_BASE_URL` points to correct backend URL
   - No trailing slash in URL

3. **CORS Issues**:
   - Backend's `FRONTEND_ORIGIN` matches frontend URL exactly
   - Include protocol (https://)

### Services Start But Can't Communicate

1. **Update CORS Settings**:
   - In Render, update backend's `FRONTEND_ORIGIN` to actual frontend URL
   - Redeploy backend service

2. **Update API Base URL**:
   - Update frontend's `VITE_API_BASE_URL` to actual backend URL
   - Redeploy frontend service

## 📊 Post-Deployment

### Monitor Your Services

1. **Free Tier Limitations**:
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - Consider upgrading for production use

2. **Set Up Monitoring**:
   - Use Render's built-in metrics
   - Set up UptimeRobot or similar for health checks

3. **Check Logs Regularly**:
   - Review error logs
   - Monitor API usage
   - Track performance

### Cost Optimization

- Free tier includes 750 hours/month per service
- Database and external services may have separate costs
- Monitor API usage (Gemini, Serper) to stay within free tiers

## 🔄 Updating Deployment

```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push origin main

# Render will automatically redeploy
```

## 📞 Support

If issues persist:
1. Check Render status: https://status.render.com/
2. Review Render documentation: https://render.com/docs
3. Check project README: `README.md`

---

**Deployment Date**: _____________________  
**Backend URL**: _____________________  
**Frontend URL**: _____________________  
**MongoDB Cluster**: _____________________
