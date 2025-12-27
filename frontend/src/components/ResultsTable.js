import React, { useState, useEffect } from 'react';
import { getVulnerabilities } from '../services/api';
import VulnerabilityCard from './VulnerabilityCard';

function ResultsTable({ scans }) {
  const [selectedScan, setSelectedScan] = useState(null);
  const [vulnerabilities, setVulnerabilities] = useState([]);

  const loadVulnerabilities = async (scanId) => {
    try {
      const data = await getVulnerabilities(scanId);
      setVulnerabilities(data.vulnerabilities || []);
    } catch (error) {
      console.error('Error loading vulnerabilities:', error);
      setVulnerabilities([]);
    }
  };

  const handleScanClick = (scan) => {
    setSelectedScan(scan);
    if (scan.status === 'completed') {
      loadVulnerabilities(scan.id);
    }
  };

  return (
    <div className="results-section">
      <h2>Scan Results</h2>
      {scans.length === 0 ? (
        <p className="no-data">No scans yet. Create a new scan to get started!</p>
      ) : (
        <table className="results-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Target</th>
              <th>Type</th>
              <th>Status</th>
              <th>Created</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {scans.map(scan => (
              <tr key={scan.id}>
                <td>{scan.id}</td>
                <td>{scan.target}</td>
                <td>{scan.scan_type}</td>
                <td>
                  <span className={`status status-${scan.status}`}>
                    {scan.status}
                  </span>
                </td>
                <td>{new Date(scan.created_at).toLocaleString()}</td>
                <td>
                  <button onClick={() => handleScanClick(scan)}>
                    View Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selectedScan && (
        <div className="scan-details">
          <h3>Scan Details: {selectedScan.target}</h3>
          <p>Status: {selectedScan.status}</p>
          <p>Scan Type: {selectedScan.scan_type}</p>
          
          {selectedScan.status === 'completed' && vulnerabilities.length > 0 && (
            <div className="vulnerabilities-section">
              <h4>Vulnerabilities Found: {vulnerabilities.length}</h4>
              <div className="vulnerability-grid">
                {vulnerabilities.map(vuln => (
                  <VulnerabilityCard key={vuln.id} vulnerability={vuln} />
                ))}
              </div>
            </div>
          )}
          
          {selectedScan.status === 'completed' && vulnerabilities.length === 0 && (
            <p className="no-data">No vulnerabilities found! The target appears secure.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default ResultsTable;
