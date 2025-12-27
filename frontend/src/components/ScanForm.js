import React, { useState } from 'react';
import { createScan } from '../services/api';

function ScanForm({ onScanComplete }) {
  const [target, setTarget] = useState('');
  const [scanType, setScanType] = useState('quick');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      await createScan({ target, scan_type: scanType });
      setMessage('Scan started successfully!');
      setTarget('');
      onScanComplete();
    } catch (error) {
      setMessage('Error starting scan: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scan-form">
      <h2>New Scan</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Target (IP or Hostname):</label>
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="192.168.1.1 or example.com"
            required
          />
        </div>
        
        <div className="form-group">
          <label>Scan Type:</label>
          <select value={scanType} onChange={(e) => setScanType(e.target.value)}>
            <option value="quick">Quick Scan (Top 100 ports)</option>
            <option value="full">Full Scan (All ports)</option>
          </select>
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Scanning...' : 'Start Scan'}
        </button>
        
        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}

export default ScanForm;
