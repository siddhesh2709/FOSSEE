import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QComboBox, QTextEdit, QTabWidget,
    QGroupBox, QFormLayout, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd


API_BASE_URL = 'http://localhost:8000/api'


class LoginWindow(QWidget):
    """Login window for authentication"""
    
    def __init__(self, on_login_success):
        super().__init__()
        self.on_login_success = on_login_success
        self.session = requests.Session()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer - Login')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Desktop Application')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Login form
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter username')
        form_layout.addRow('Username:', self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.returnPressed.connect(self.login)
        form_layout.addRow('Password:', self.password_input)
        
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        # Buttons
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.register)
        layout.addWidget(self.register_btn)
        
        # Status
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
            return
        
        try:
            response = self.session.post(
                f'{API_BASE_URL}/auth/login/',
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self.on_login_success(self.session, user_data['user'])
                self.close()
            else:
                self.status_label.setText('Invalid credentials')
        except Exception as e:
            self.status_label.setText(f'Error: {str(e)}')
    
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText('Please enter username and password')
            return
        
        try:
            response = self.session.post(
                f'{API_BASE_URL}/auth/register/',
                json={'username': username, 'password': password, 'email': ''}
            )
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'Registration successful! Please login.')
                self.password_input.clear()
            else:
                error = response.json().get('error', 'Registration failed')
                self.status_label.setText(error)
        except Exception as e:
            self.status_label.setText(f'Error: {str(e)}')


class MatplotlibCanvas(FigureCanvas):
    """Canvas for embedding matplotlib charts"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, session, user):
        super().__init__()
        self.session = session
        self.user = user
        self.datasets = []
        self.selected_dataset = None
        self.summary = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        self.setWindowTitle(f'Chemical Equipment Visualizer - {self.user["username"]}')
        self.setGeometry(100, 100, 1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        
        # Header
        header = QLabel('⚗️ Chemical Equipment Parameter Visualizer')
        header.setFont(QFont('Arial', 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('background-color: #667eea; color: white; padding: 15px;')
        main_layout.addWidget(header)
        
        # User info and logout
        user_layout = QHBoxLayout()
        user_label = QLabel(f'Welcome, {self.user["username"]}!')
        user_layout.addWidget(user_label)
        user_layout.addStretch()
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        user_layout.addWidget(logout_btn)
        
        main_layout.addLayout(user_layout)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV File')
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        upload_layout.addWidget(self.file_label)
        
        browse_btn = QPushButton('Browse')
        browse_btn.clicked.connect(self.browse_file)
        upload_layout.addWidget(browse_btn)
        
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        upload_layout.addWidget(self.upload_btn)
        
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)
        
        # Dataset selector
        dataset_layout = QHBoxLayout()
        dataset_layout.addWidget(QLabel('Select Dataset:'))
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_changed)
        dataset_layout.addWidget(self.dataset_combo)
        
        self.pdf_btn = QPushButton('Download PDF Report')
        self.pdf_btn.clicked.connect(self.download_pdf)
        dataset_layout.addWidget(self.pdf_btn)
        
        dataset_layout.addStretch()
        main_layout.addLayout(dataset_layout)
        
        # Tabs for different views
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_tab = QWidget()
        self.setup_summary_tab()
        self.tabs.addTab(self.summary_tab, 'Summary')
        
        # Data tab
        self.data_tab = QWidget()
        self.setup_data_tab()
        self.tabs.addTab(self.data_tab, 'Data Table')
        
        # Charts tab
        self.charts_tab = QWidget()
        self.setup_charts_tab()
        self.tabs.addTab(self.charts_tab, 'Charts')
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage('Ready')
        
        main_widget.setLayout(main_layout)
        
        self.selected_file = None
    
    def setup_summary_tab(self):
        layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setFont(QFont('Courier', 10))
        layout.addWidget(self.summary_text)
        
        self.summary_tab.setLayout(layout)
    
    def setup_data_tab(self):
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            'Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'
        ])
        layout.addWidget(self.data_table)
        
        self.data_tab.setLayout(layout)
    
    def setup_charts_tab(self):
        layout = QVBoxLayout()
        
        # Equipment type chart
        self.type_canvas = MatplotlibCanvas(self, width=5, height=3)
        layout.addWidget(self.type_canvas)
        
        # Parameters chart
        self.params_canvas = MatplotlibCanvas(self, width=5, height=3)
        layout.addWidget(self.params_canvas)
        
        self.charts_tab.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select CSV File', '', 'CSV Files (*.csv)'
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(file_path.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                response = self.session.post(f'{API_BASE_URL}/datasets/', files=files)
            
            if response.status_code == 201:
                QMessageBox.information(self, 'Success', 'File uploaded successfully!')
                self.selected_file = None
                self.file_label.setText('No file selected')
                self.upload_btn.setEnabled(False)
                self.load_datasets()
            else:
                error = response.json().get('error', 'Upload failed')
                QMessageBox.warning(self, 'Error', error)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def load_datasets(self):
        try:
            response = self.session.get(f'{API_BASE_URL}/datasets/')
            if response.status_code == 200:
                self.datasets = response.json()
                self.dataset_combo.clear()
                
                for dataset in self.datasets:
                    label = f"{dataset['filename']} ({dataset['record_count']} records)"
                    self.dataset_combo.addItem(label, dataset['id'])
                
                if self.datasets:
                    self.load_dataset(self.datasets[0]['id'])
        except Exception as e:
            self.statusBar().showMessage(f'Error loading datasets: {str(e)}')
    
    def on_dataset_changed(self, index):
        if index >= 0:
            dataset_id = self.dataset_combo.itemData(index)
            if dataset_id:
                self.load_dataset(dataset_id)
    
    def load_dataset(self, dataset_id):
        try:
            # Load dataset details
            response = self.session.get(f'{API_BASE_URL}/datasets/{dataset_id}/')
            if response.status_code == 200:
                self.selected_dataset = response.json()
            
            # Load summary
            response = self.session.get(f'{API_BASE_URL}/datasets/{dataset_id}/summary/')
            if response.status_code == 200:
                self.summary = response.json()
                self.update_views()
        except Exception as e:
            self.statusBar().showMessage(f'Error loading dataset: {str(e)}')
    
    def update_views(self):
        if not self.selected_dataset or not self.summary:
            return
        
        # Update summary
        self.update_summary()
        
        # Update data table
        self.update_data_table()
        
        # Update charts
        self.update_charts()
        
        self.statusBar().showMessage('Dataset loaded successfully')
    
    def update_summary(self):
        text = f"""
========================================
CHEMICAL EQUIPMENT ANALYSIS SUMMARY
========================================

Dataset: {self.selected_dataset['filename']}
Uploaded: {self.selected_dataset['uploaded_at']}
Total Equipment: {self.summary['total_count']}

----------------------------------------
EQUIPMENT TYPE DISTRIBUTION
----------------------------------------
"""
        for eq_type, count in self.summary['equipment_types'].items():
            text += f"{eq_type}: {count}\n"
        
        text += """
----------------------------------------
PARAMETER STATISTICS
----------------------------------------
"""
        for param in ['flowrate', 'pressure', 'temperature']:
            stats = self.summary['statistics'][param]
            text += f"""
{param.upper()}:
  Average: {stats['average']:.2f}
  Min: {stats['min']:.2f}
  Max: {stats['max']:.2f}
  Std Dev: {stats['std']:.2f}
"""
        
        self.summary_text.setText(text)
    
    def update_data_table(self):
        data = self.selected_dataset['data']
        self.data_table.setRowCount(len(data))
        
        for row_idx, row in enumerate(data):
            self.data_table.setItem(row_idx, 0, QTableWidgetItem(row['Equipment Name']))
            self.data_table.setItem(row_idx, 1, QTableWidgetItem(row['Type']))
            self.data_table.setItem(row_idx, 2, QTableWidgetItem(str(row['Flowrate'])))
            self.data_table.setItem(row_idx, 3, QTableWidgetItem(str(row['Pressure'])))
            self.data_table.setItem(row_idx, 4, QTableWidgetItem(str(row['Temperature'])))
        
        self.data_table.resizeColumnsToContents()
    
    def update_charts(self):
        # Equipment type distribution chart
        self.type_canvas.axes.clear()
        types = list(self.summary['equipment_types'].keys())
        counts = list(self.summary['equipment_types'].values())
        
        colors = ['#667eea', '#764ba2', '#ed64a6', '#ff9a9e', '#fad0c4']
        self.type_canvas.axes.pie(counts, labels=types, autopct='%1.1f%%', colors=colors)
        self.type_canvas.axes.set_title('Equipment Type Distribution')
        self.type_canvas.draw()
        
        # Parameters chart
        self.params_canvas.axes.clear()
        params = ['Flowrate', 'Pressure', 'Temperature']
        averages = [
            self.summary['statistics']['flowrate']['average'],
            self.summary['statistics']['pressure']['average'],
            self.summary['statistics']['temperature']['average']
        ]
        
        bars = self.params_canvas.axes.bar(params, averages, color=['#667eea', '#764ba2', '#ed64a6'])
        self.params_canvas.axes.set_title('Average Parameters')
        self.params_canvas.axes.set_ylabel('Value')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            self.params_canvas.axes.text(
                bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom'
            )
        
        self.params_canvas.draw()
    
    def download_pdf(self):
        if not self.selected_dataset:
            return
        
        try:
            response = self.session.get(
                f'{API_BASE_URL}/datasets/{self.selected_dataset["id"]}/pdf/',
                stream=True
            )
            
            if response.status_code == 200:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, 'Save PDF Report', f'equipment_report_{self.selected_dataset["id"]}.pdf',
                    'PDF Files (*.pdf)'
                )
                
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, 'Success', 'PDF downloaded successfully!')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to download PDF')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
    
    def logout(self):
        try:
            self.session.post(f'{API_BASE_URL}/auth/logout/')
        except:
            pass
        
        self.close()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    def on_login_success(session, user):
        main_window = MainWindow(session, user)
        main_window.show()
    
    login_window = LoginWindow(on_login_success)
    login_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
