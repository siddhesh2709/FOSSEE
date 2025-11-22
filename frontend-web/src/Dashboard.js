import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import api from './api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

function Dashboard({ user, onLogout }) {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [summary, setSummary] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchDatasets = async () => {
    try {
      const response = await api.getDatasets();
      setDatasets(response.data);
      if (response.data.length > 0 && !selectedDataset) {
        loadDataset(response.data[0].id);
      }
    } catch (err) {
      setError('Failed to fetch datasets');
    }
  };

  useEffect(() => {
    fetchDatasets();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadDataset = async (id) => {
    setLoading(true);
    try {
      const [datasetRes, summaryRes] = await Promise.all([
        api.getDataset(id),
        api.getDatasetSummary(id),
      ]);
      setSelectedDataset(datasetRes.data);
      setSummary(summaryRes.data);
      setError('');
    } catch (err) {
      setError('Failed to load dataset');
    } finally {
      setLoading(false);
    }
  };

  const closeDataset = () => {
    setSelectedDataset(null);
    setSummary(null);
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      await api.uploadDataset(file);
      setSuccess('File uploaded successfully!');
      setFile(null);
      e.target.reset();
      fetchDatasets();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPDF = async () => {
    if (!selectedDataset) return;
    
    try {
      const response = await api.downloadPDF(selectedDataset.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `equipment_report_${selectedDataset.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      setSuccess('PDF downloaded successfully!');
    } catch (err) {
      setError('Failed to download PDF');
    }
  };

  const handleLogout = () => {
    // Logout disabled
  };

  // Chart configurations
  const getEquipmentTypeChart = () => {
    if (!summary) return null;

    const labels = Object.keys(summary.equipment_types);
    const data = Object.values(summary.equipment_types);

    return {
      labels,
      datasets: [
        {
          label: 'Equipment Count',
          data,
          backgroundColor: [
            'rgba(102, 126, 234, 0.8)',
            'rgba(118, 75, 162, 0.8)',
            'rgba(237, 100, 166, 0.8)',
            'rgba(255, 154, 158, 0.8)',
            'rgba(250, 208, 196, 0.8)',
          ],
          borderColor: [
            'rgba(102, 126, 234, 1)',
            'rgba(118, 75, 162, 1)',
            'rgba(237, 100, 166, 1)',
            'rgba(255, 154, 158, 1)',
            'rgba(250, 208, 196, 1)',
          ],
          borderWidth: 2,
        },
      ],
    };
  };

  const getParameterChart = () => {
    if (!summary) return null;

    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [
        {
          label: 'Average',
          data: [
            summary.statistics.flowrate.average,
            summary.statistics.pressure.average,
            summary.statistics.temperature.average,
          ],
          backgroundColor: 'rgba(102, 126, 234, 0.8)',
          borderColor: 'rgba(102, 126, 234, 1)',
          borderWidth: 2,
        },
      ],
    };
  };

  const getParameterTrendChart = () => {
    if (!selectedDataset) return null;

    const equipmentNames = selectedDataset.data.map(item => item['Equipment Name']);
    
    return {
      labels: equipmentNames,
      datasets: [
        {
          label: 'Flowrate',
          data: selectedDataset.data.map(item => item.Flowrate),
          borderColor: 'rgba(102, 126, 234, 1)',
          backgroundColor: 'rgba(102, 126, 234, 0.2)',
          tension: 0.4,
        },
        {
          label: 'Pressure',
          data: selectedDataset.data.map(item => item.Pressure),
          borderColor: 'rgba(118, 75, 162, 1)',
          backgroundColor: 'rgba(118, 75, 162, 0.2)',
          tension: 0.4,
        },
        {
          label: 'Temperature',
          data: selectedDataset.data.map(item => item.Temperature),
          borderColor: 'rgba(237, 100, 166, 1)',
          backgroundColor: 'rgba(237, 100, 166, 0.2)',
          tension: 0.4,
        },
      ],
    };
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>⚗️ Chemical Equipment Parameter Visualizer</h1>
          <p>Convert your CSV data to visual insights with incredible accuracy</p>
        </div>

        <div className="content">
          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">{success}</div>}

          {/* Upload Section */}
          <div className="upload-section-modern">
            <div className="upload-box">
              <h2>Upload CSV File</h2>
              <form onSubmit={handleFileUpload}>
                <div className="file-input-container">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={(e) => setFile(e.target.files[0])}
                    id="fileInput"
                    className="file-input-hidden"
                  />
                  <label htmlFor="fileInput" className="file-input-label">
                    {file ? file.name : 'Select CSV file'}
                  </label>
                  <p className="file-hint">or drop CSV here</p>
                </div>
                <button type="submit" className="btn btn-upload" disabled={loading || !file}>
                  {loading ? 'Processing...' : 'Upload & Analyze'}
                </button>
              </form>
            </div>
            
            {/* Instructions */}
            <div className="upload-instructions">
              <h3>📋 How to Upload</h3>
              <ul>
                <li><strong>File Format:</strong> CSV (Comma-Separated Values)</li>
                <li><strong>Required Columns:</strong> Equipment Name, Type, Flowrate, Pressure, Temperature</li>
                <li><strong>Example:</strong> Equipment Name, Type, Flowrate, Pressure, Temperature</li>
                <li><strong>Max Size:</strong> 10 MB per file</li>
                <li><strong>Note:</strong> Only the last 5 datasets are stored</li>
              </ul>
            </div>
          </div>

          {/* Dataset List */}
          {datasets.length > 0 && (
            <div className="dataset-list">
              <h2>📊 Dataset History (Last 5)</h2>
              {datasets.map((dataset) => (
                <div
                  key={dataset.id}
                  className={`dataset-item ${selectedDataset?.id === dataset.id ? 'active' : ''}`}
                  onClick={() => loadDataset(dataset.id)}
                >
                  <div className="dataset-info">
                    <strong>{dataset.filename}</strong>
                    <br />
                    <small>
                      {new Date(dataset.uploaded_at).toLocaleString()} | {dataset.record_count} records
                    </small>
                  </div>
                  <div className="dataset-actions">
                    {selectedDataset?.id === dataset.id && (
                      <button
                        className="btn btn-success"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDownloadPDF();
                        }}
                      >
                        Download PDF
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}

          {loading && <div className="loading">Loading...</div>}

          {/* Summary Section */}
          {summary && (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>📈 Dataset Analysis</h2>
                <button 
                  className="btn btn-secondary" 
                  onClick={closeDataset}
                  style={{ 
                    backgroundColor: '#6c757d',
                    padding: '10px 20px',
                    fontSize: '16px',
                    fontWeight: 'bold'
                  }}
                >
                  ✕ Close
                </button>
              </div>
              <div className="summary-section">
                <div className="summary-card">
                  <h3>Total Equipment</h3>
                  <div className="value">{summary.total_count}</div>
                  <div className="details">Devices in dataset</div>
                </div>

                <div className="summary-card">
                  <h3>Avg Flowrate</h3>
                  <div className="value">{summary.statistics.flowrate.average.toFixed(2)}</div>
                  <div className="details">
                    Min: {summary.statistics.flowrate.min.toFixed(2)} | 
                    Max: {summary.statistics.flowrate.max.toFixed(2)}
                  </div>
                </div>

                <div className="summary-card">
                  <h3>Avg Pressure</h3>
                  <div className="value">{summary.statistics.pressure.average.toFixed(2)}</div>
                  <div className="details">
                    Min: {summary.statistics.pressure.min.toFixed(2)} | 
                    Max: {summary.statistics.pressure.max.toFixed(2)}
                  </div>
                </div>

                <div className="summary-card">
                  <h3>Avg Temperature</h3>
                  <div className="value">{summary.statistics.temperature.average.toFixed(2)}</div>
                  <div className="details">
                    Min: {summary.statistics.temperature.min.toFixed(2)} | 
                    Max: {summary.statistics.temperature.max.toFixed(2)}
                  </div>
                </div>
              </div>

              {/* Charts Section */}
              <div className="charts-section">
                <div className="chart-container">
                  <h3>Equipment Type Distribution</h3>
                  <Pie data={getEquipmentTypeChart()} />
                </div>

                <div className="chart-container">
                  <h3>Average Parameters</h3>
                  <Bar data={getParameterChart()} options={{ responsive: true }} />
                </div>
              </div>

              <div className="chart-container" style={{ marginBottom: '30px' }}>
                <h3>Parameter Trends Across Equipment</h3>
                <Line 
                  data={getParameterTrendChart()} 
                  options={{ 
                    responsive: true,
                    scales: {
                      y: {
                        beginAtZero: true
                      }
                    }
                  }} 
                />
              </div>
            </>
          )}

          {/* Data Table */}
          {selectedDataset && (
            <div className="data-section">
              <h2>📋 Equipment Data</h2>
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      <th>Equipment Name</th>
                      <th>Type</th>
                      <th>Flowrate</th>
                      <th>Pressure</th>
                      <th>Temperature</th>
                    </tr>
                  </thead>
                  <tbody>
                    {selectedDataset.data.map((row, index) => (
                      <tr key={index}>
                        <td>{row['Equipment Name']}</td>
                        <td>{row['Type']}</td>
                        <td>{row['Flowrate']}</td>
                        <td>{row['Pressure']}</td>
                        <td>{row['Temperature']}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
