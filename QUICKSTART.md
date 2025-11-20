# 🚀 Quick Start Guide

## Fastest Way to Get Started

### Prerequisites Check
```powershell
python --version  # Should be 3.8+
node --version    # Should be 14+
npm --version
```

---

## 🎯 Option 1: Use Batch Scripts (Windows - Easiest!)

### Step 1: Setup (One-time only)

1. **Setup Backend**
   ```powershell
   .\setup_backend.bat
   ```
   - When prompted, create a superuser (remember the username/password!)

2. **Setup Web Frontend**
   ```powershell
   .\setup_frontend_web.bat
   ```

3. **Setup Desktop App**
   ```powershell
   .\setup_frontend_desktop.bat
   ```

### Step 2: Run the Applications

**Always start backend first!**

1. **Start Backend** (Terminal 1)
   ```powershell
   .\start_backend.bat
   ```
   Wait for: "Starting development server at http://127.0.0.1:8000/"

2. **Start Web App** (Terminal 2)
   ```powershell
   .\start_web.bat
   ```
   Browser will open at http://localhost:3000

3. **Start Desktop App** (Terminal 3)
   ```powershell
   .\start_desktop.bat
   ```
   Desktop window will appear

---

## 🎯 Option 2: Manual Commands

### Backend
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Web Frontend
```powershell
cd frontend-web
npm install
npm start
```

### Desktop App
```powershell
cd frontend-desktop
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

---

## 📝 First Time Usage

1. **Register/Login**
   - Web: Go to http://localhost:3000
   - Desktop: Launch the app
   - Create account or use superuser credentials

2. **Upload Sample Data**
   - Click "Browse" → Select `sample_equipment_data.csv`
   - Click "Upload"

3. **Explore Features**
   - View summary statistics
   - Check data tables
   - Explore charts
   - Download PDF report

---

## ✅ Checklist

- [ ] Backend running on port 8000
- [ ] Web app accessible at localhost:3000
- [ ] Desktop app launched successfully
- [ ] Registered user account
- [ ] Uploaded sample CSV file
- [ ] Downloaded PDF report

---

## 🐛 Common Issues

**Can't start backend?**
→ Make sure virtual environment is activated

**Web app not loading?**
→ Check if backend is running first

**Desktop app connection error?**
→ Backend must be running on port 8000

**Import errors?**
→ Run `pip install -r requirements.txt` again

---

## 📚 Next Steps

- Read `SETUP_GUIDE.md` for detailed information
- Check `README.md` for project overview
- Explore API endpoints
- Customize the application

---

## 🎉 You're All Set!

Enjoy using the Chemical Equipment Parameter Visualizer!
