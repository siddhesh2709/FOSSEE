# Chemical Equipment Parameter Visualizer

A hybrid application that runs both as a Web Application (React) and Desktop Application (PyQt5) for chemical equipment data visualization and analytics.

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Web Frontend**: React.js + Chart.js
- **Desktop Frontend**: PyQt5 + Matplotlib
- **Data Processing**: Pandas
- **Database**: SQLite
- **PDF Generation**: ReportLab

## Features

- ✅ CSV file upload (Web & Desktop)
- ✅ Data summary and statistics API
- ✅ Interactive charts and visualizations
- ✅ History management (last 5 datasets)
- ✅ PDF report generation
- ✅ Basic authentication
- ✅ Equipment type distribution analysis

## Project Structure

```
chemical-equipment-visualizer/
├── backend/                 # Django REST API
│   ├── equipment_api/       # Main Django app
│   ├── manage.py
│   └── requirements.txt
├── frontend-web/            # React Web App
│   ├── src/
│   ├── public/
│   └── package.json
├── frontend-desktop/        # PyQt5 Desktop App
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv
└── README.md
```

## Setup Instructions

### 1. Backend (Django)

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The backend will run at `http://localhost:8000`

### 2. Web Frontend (React)

```powershell
cd frontend-web
npm install
npm start
```

The web app will run at `http://localhost:3000`

### 3. Desktop Frontend (PyQt5)

```powershell
cd frontend-desktop
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## API Endpoints

- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - List all datasets
- `GET /api/datasets/{id}/` - Get specific dataset details
- `GET /api/datasets/{id}/summary/` - Get dataset summary statistics
- `GET /api/datasets/{id}/pdf/` - Download PDF report
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

## Usage

1. **Upload CSV**: Use either web or desktop interface to upload `sample_equipment_data.csv`
2. **View Data**: Data table displays all equipment records
3. **Analyze**: View summary statistics and charts
4. **Download Report**: Generate and download PDF report
5. **History**: Access previously uploaded datasets (last 5)

## Sample CSV Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
...
```

## Authentication

- Default credentials can be created using `python manage.py createsuperuser`
- Login required for all API operations
- Session-based authentication for web and token-based for desktop

## Development

- Backend API: Django REST Framework with CORS enabled
- Web: React with Axios for API calls
- Desktop: PyQt5 with requests library
- Data stored in SQLite with automatic cleanup (keeps last 5 datasets)

## License

MIT License

## Author

FOSSEE Project - Chemical Equipment Visualizer
