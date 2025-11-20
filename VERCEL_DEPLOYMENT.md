# Deployment Guide for Vercel

## Prerequisites
- Vercel account (sign up at https://vercel.com)
- Git repository (GitHub, GitLab, or Bitbucket)

## Option 1: Deploy via Vercel CLI (Recommended)

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy from project root
```bash
cd d:\Projects\FOSSEE\chemical-equipment-visualizer
vercel
```

Follow the prompts:
- Set up and deploy? **Y**
- Which scope? **Select your account**
- Link to existing project? **N**
- Project name? **chemical-equipment-visualizer**
- In which directory is your code located? **./**

### 4. Set Environment Variables
After deployment, go to your Vercel dashboard and add:
- `DJANGO_SETTINGS_MODULE` = `equipment_visualizer.settings`
- `DEBUG` = `False`

### 5. Redeploy
```bash
vercel --prod
```

## Option 2: Deploy via Git Integration

### 1. Initialize Git Repository
```bash
cd d:\Projects\FOSSEE\chemical-equipment-visualizer
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repository
- Go to https://github.com/new
- Create a new repository
- Follow instructions to push your code

### 3. Connect to Vercel
- Go to https://vercel.com/new
- Import your GitHub repository
- Configure:
  - Framework Preset: **Other**
  - Build Command: `cd backend && pip install -r requirements.txt`
  - Output Directory: **Leave empty**

### 4. Add Environment Variables
In Vercel project settings:
- `DJANGO_SETTINGS_MODULE` = `equipment_visualizer.settings`
- `DEBUG` = `False`

### 5. Deploy
Click **Deploy** button

## Important Notes

### For Production:
1. **Update CORS settings** in `backend/equipment_visualizer/settings.py`:
   ```python
   CORS_ALLOWED_ORIGINS = [
       'https://your-vercel-app.vercel.app',
   ]
   ```

2. **Update API URL** in `frontend-web/src/api.js`:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 'https://your-backend-url.vercel.app/api';
   ```

3. **Database**: Vercel uses serverless functions, so SQLite won't persist. Consider:
   - PostgreSQL (Vercel Postgres)
   - MongoDB (MongoDB Atlas)
   - Supabase

### Alternative: Deploy Frontend and Backend Separately

#### Deploy Backend (Django):
1. Use **Vercel** for serverless Django
2. Or use **Railway**, **Render**, or **PythonAnywhere**

#### Deploy Frontend (React):
1. Build React app: `cd frontend-web && npm run build`
2. Deploy to Vercel/Netlify/Cloudflare Pages

## Quick Deploy Commands

```bash
# From project root
cd d:\Projects\FOSSEE\chemical-equipment-visualizer

# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

## Troubleshooting

### If deployment fails:
1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `requirements.txt`
3. Verify Python version compatibility
4. Check environment variables

### Database Issues:
- For production, switch from SQLite to PostgreSQL
- Update `DATABASES` in settings.py for production

## Post-Deployment

1. Test all endpoints
2. Upload a CSV file
3. Verify charts display correctly
4. Test PDF download
5. Check authentication flow

## Recommended Production Setup

For a production-ready deployment, consider:

1. **Backend**: Railway or Render (with PostgreSQL)
2. **Frontend**: Vercel or Netlify
3. **Database**: Railway Postgres or Supabase
4. **Static Files**: AWS S3 or Cloudinary
