# Chemical Equipment Parameter Visualizer - Setup Guide

This guide will help you set up and run the hybrid Chemical Equipment Parameter Visualizer application.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git (for version control)

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                    # Django REST API
├── frontend-web/               # React Web Application
├── frontend-desktop/           # PyQt5 Desktop Application
├── sample_equipment_data.csv   # Sample data for testing
└── README.md
```

## Setup Instructions

### 1. Backend Setup (Django)

**Step 1: Navigate to backend directory**
```powershell
cd backend
```

**Step 2: Create virtual environment**
```powershell
python -m venv venv
```

**Step 3: Activate virtual environment**
```powershell
.\venv\Scripts\Activate.ps1
```

**Step 4: Install dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Run migrations**
```powershell
python manage.py migrate
```

**Step 6: Create superuser (for admin access)**
```powershell
python manage.py createsuperuser
```
- Enter username (e.g., admin)
- Enter email (optional)
- Enter password (e.g., admin123)

**Step 7: Start the backend server**
```powershell
python manage.py runserver
```

The backend will run at: `http://localhost:8000`

**Admin Panel**: `http://localhost:8000/admin`

---

### 2. Web Frontend Setup (React)

**Step 1: Open a new terminal and navigate to frontend-web**
```powershell
cd frontend-web
```

**Step 2: Install dependencies**
```powershell
npm install
```

**Step 3: Start the development server**
```powershell
npm start
```

The web app will run at: `http://localhost:3000`

---

### 3. Desktop Frontend Setup (PyQt5)

**Step 1: Open a new terminal and navigate to frontend-desktop**
```powershell
cd frontend-desktop
```

**Step 2: Create virtual environment**
```powershell
python -m venv venv
```

**Step 3: Activate virtual environment**
```powershell
.\venv\Scripts\Activate.ps1
```

**Step 4: Install dependencies**
```powershell
pip install -r requirements.txt
```

**Step 5: Run the desktop application**
```powershell
python main.py
```

---

## Usage Guide

### First Time Setup

1. **Start the Backend** (Django server must be running first)
2. **Register a User**:
   - Web: Go to http://localhost:3000 and click "Register"
   - Desktop: Launch the app and click "Register"
3. **Login** with your credentials

### Uploading Data

1. Use the provided `sample_equipment_data.csv` file
2. Click "Browse" or select file
3. Click "Upload"
4. Data will be parsed and displayed

### Viewing Data

- **Summary Tab/Section**: View statistics and counts
- **Data Table**: See all equipment records
- **Charts**: Visualize data with interactive charts
  - Equipment type distribution (Pie chart)
  - Average parameters (Bar chart)
  - Parameter trends (Line chart - Web only)

### Downloading Reports

1. Select a dataset
2. Click "Download PDF Report"
3. PDF includes:
   - Dataset information
   - Equipment type distribution
   - Parameter statistics
   - Full data table

### History Management

- System automatically keeps the last 5 uploaded datasets
- Older datasets are automatically deleted

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/user/` - Get current user

### Datasets
- `GET /api/datasets/` - List all datasets
- `POST /api/datasets/` - Upload CSV file
- `GET /api/datasets/{id}/` - Get dataset details
- `GET /api/datasets/{id}/summary/` - Get statistics
- `GET /api/datasets/{id}/pdf/` - Download PDF report
- `DELETE /api/datasets/{id}/` - Delete dataset

---

## CSV File Format

Your CSV file should have the following columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
...
```

**Required Columns**:
- Equipment Name (string)
- Type (string)
- Flowrate (number)
- Pressure (number)
- Temperature (number)

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'django'`
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Issue**: `CSRF token missing`
- **Solution**: Make sure CORS is properly configured in settings.py

### Web Frontend Issues

**Issue**: `npm ERR! code ENOENT`
- **Solution**: Run `npm install` in the frontend-web directory

**Issue**: API connection errors
- **Solution**: Ensure backend is running on port 8000

### Desktop Application Issues

**Issue**: `ImportError: No module named 'PyQt5'`
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Issue**: Connection refused
- **Solution**: Start the Django backend server first

---

## Development Tips

1. **Backend Changes**: Restart Django server after model changes
2. **Web Frontend**: Changes auto-reload with React hot reloading
3. **Desktop App**: Restart application to see changes
4. **Database Reset**: Delete `db.sqlite3` and run migrations again

---

## Features Overview

### Web Application (React)
- ✅ Responsive design
- ✅ Interactive charts with Chart.js
- ✅ Real-time data updates
- ✅ Session-based authentication
- ✅ File upload with drag-drop support

### Desktop Application (PyQt5)
- ✅ Native desktop experience
- ✅ Matplotlib charts
- ✅ Multi-tab interface
- ✅ File browser integration
- ✅ PDF download functionality

### Backend (Django)
- ✅ RESTful API
- ✅ Pandas data processing
- ✅ SQLite database
- ✅ PDF report generation with ReportLab
- ✅ User authentication
- ✅ Automatic data cleanup

---

## Next Steps

1. **Test with Sample Data**: Upload `sample_equipment_data.csv`
2. **Explore Features**: Try all tabs and visualizations
3. **Generate Reports**: Download PDF reports
4. **Add More Data**: Create your own CSV files
5. **Customize**: Modify charts, colors, and layouts

---

## Support

For issues or questions:
1. Check this guide first
2. Review API documentation
3. Check Django admin panel for data
4. Review browser console for web app errors

---

## Version Control

Initialize Git repository:
```powershell
git init
git add .
git commit -m "Initial commit: Chemical Equipment Visualizer"
```

Create GitHub repository:
```powershell
git remote add origin https://github.com/yourusername/chemical-equipment-visualizer.git
git push -u origin main
```

---

## License

MIT License - Feel free to modify and distribute

## Author

FOSSEE Project - Chemical Equipment Parameter Visualizer
