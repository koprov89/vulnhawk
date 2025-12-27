import React, { useState, useEffect } from 'react';
import './styles/App.css';
import Dashboard from './components/Dashboard';
import ScanForm from './components/ScanForm';
import ResultsTable from './components/ResultsTable';
import { getScans } from './services/api';

function App() {
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);

  const loadScans = async () => {
    try {
      const data = await getScans();
      setScans(data);
    } catch (error) {
      console.error('Error loading scans:', error);
    }
  };

  useEffect(() => {
    loadScans();
    // Poll for updates every 5 seconds
    const interval = setInterval(loadScans, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🦅 VulnHawk</h1>
        <p>Network Vulnerability Scanner</p>
      </header>
      
      <main className="App-main">
        <Dashboard scans={scans} />
        <ScanForm onScanComplete={loadScans} />
        <ResultsTable scans={scans} onSelectScan={setSelectedScan} />
      </main>
      
      <footer className="App-footer">
        <p>&copy; 2024 VulnHawk - Network Vulnerability Scanner</p>
      </footer>
    </div>
  );
}

export default App;
