# Deploy Chemical Equipment Visualizer to Vercel

## Quick Deployment Steps

### Step 1: Deploy Frontend to Vercel
```powershell
cd d:\Projects\FOSSEE\chemical-equipment-visualizer
vercel --prod
```

### Step 2: Deploy Backend to Railway (Recommended for Django)

Since Vercel has limitations with Django/SQLite, use Railway for backend:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository (or create one first)
5. Railway will auto-detect Django and deploy

### Alternative: Use Vercel for Frontend + Railway for Backend

## Option A: Deploy Full Stack

```powershell
# From project root
cd d:\Projects\FOSSEE\chemical-equipment-visualizer

# Deploy to Vercel
vercel
```

## Option B: Separate Deployments (Recommended)

### Frontend (Vercel):
```powershell
cd d:\Projects\FOSSEE\chemical-equipment-visualizer\frontend-web
vercel --prod
```

### Backend (Railway):
1. Create account at https://railway.app
2. New Project → Deploy from GitHub
3. Point to backend folder
4. Add environment variables:
   - `DEBUG=False`
   - `ALLOWED_HOSTS=*.railway.app`

### After Backend Deployment:
Update `frontend-web/src/api.js` with your Railway backend URL:
```javascript
const API_URL = 'https://your-app.railway.app/api';
```

## Current Setup

✅ Vercel CLI installed (v48.6.7)
✅ Configuration files created
✅ Build scripts configured

## Next Steps:

Run this command to deploy:
```powershell
cd d:\Projects\FOSSEE\chemical-equipment-visualizer
vercel
```

Answer the prompts:
- Link to existing project? **N**
- Project name: **chemical-equipment-visualizer**
- Directory: **./** (or just press Enter)
- Override settings? **N**

The app will be deployed to: `https://chemical-equipment-visualizer.vercel.app`

## Post-Deployment Tasks:

1. **Update API URL** in `frontend-web/src/api.js`
2. **Configure CORS** in backend for your Vercel domain
3. **Test the deployed app**

---

Need help? Run: `vercel --help`
