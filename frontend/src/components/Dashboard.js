import React from 'react';

function Dashboard({ scans }) {
  const completedScans = scans.filter(s => s.status === 'completed').length;
  const runningScans = scans.filter(s => s.status === 'running').length;
  const failedScans = scans.filter(s => s.status === 'failed').length;

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats">
        <div className="stat-card">
          <h3>{scans.length}</h3>
          <p>Total Scans</p>
        </div>
        <div className="stat-card success">
          <h3>{completedScans}</h3>
          <p>Completed</p>
        </div>
        <div className="stat-card warning">
          <h3>{runningScans}</h3>
          <p>Running</p>
        </div>
        <div className="stat-card danger">
          <h3>{failedScans}</h3>
          <p>Failed</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
