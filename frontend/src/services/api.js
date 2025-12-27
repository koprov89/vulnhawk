import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getScans = async () => {
  const response = await api.get('/scans');
  return response.data;
};

export const createScan = async (scanData) => {
  const response = await api.post('/scans', scanData);
  return response.data;
};

export const getScan = async (scanId) => {
  const response = await api.get(`/scans/${scanId}`);
  return response.data;
};

export const getVulnerabilities = async (scanId) => {
  const response = await api.get(`/scans/${scanId}/vulnerabilities`);
  return response.data;
};

export const deleteScan = async (scanId) => {
  const response = await api.delete(`/scans/${scanId}`);
  return response.data;
};

export const getScanRisk = async (scanId) => {
  const response = await api.get(`/scans/${scanId}/risk`);
  return response.data;
};
