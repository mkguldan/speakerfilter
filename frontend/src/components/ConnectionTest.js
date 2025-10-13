import React, { useState, useEffect } from 'react';
import {
  Paper,
  Box,
  Typography,
  Chip,
  IconButton,
  Collapse,
  Alert,
  CircularProgress,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import RefreshIcon from '@mui/icons-material/Refresh';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import api from '../services/api';

function ConnectionTest() {
  const [status, setStatus] = useState('loading');
  const [data, setData] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState(false);

  const testConnection = async () => {
    setLoading(true);
    setStatus('loading');
    try {
      const response = await api.testConnection();
      setData(response.data);
      setStatus('success');
    } catch (error) {
      setStatus('error');
      setData({
        message: error.response?.data?.detail || 'Failed to connect to backend',
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testConnection();
  }, []);

  const getStatusChip = () => {
    if (status === 'loading' || loading) {
      return (
        <Chip
          icon={<CircularProgress size={16} />}
          label="Testing..."
          size="small"
          color="default"
        />
      );
    }
    if (status === 'success') {
      return (
        <Chip
          icon={<CheckCircleIcon />}
          label="Connected"
          size="small"
          color="success"
        />
      );
    }
    return (
      <Chip
        icon={<ErrorIcon />}
        label="Connection Error"
        size="small"
        color="error"
      />
    );
  };

  return (
    <Paper elevation={1} sx={{ p: 2, borderRadius: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography variant="body1" fontWeight="600">
            Airtable Connection
          </Typography>
          {getStatusChip()}
          {status === 'success' && data && (
            <Typography variant="body2" color="text.secondary">
              {data.record_count} records found
            </Typography>
          )}
        </Box>
        
        <Box>
          <IconButton onClick={testConnection} disabled={loading} size="small">
            <RefreshIcon />
          </IconButton>
          <IconButton onClick={() => setExpanded(!expanded)} size="small">
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Box>
      </Box>

      <Collapse in={expanded}>
        <Box sx={{ mt: 2 }}>
          {status === 'success' && data ? (
            <Alert severity="success" sx={{ mb: 1 }}>
              <Typography variant="body2">
                <strong>Status:</strong> {data.message}
              </Typography>
              {data.sample_columns && data.sample_columns.length > 0 && (
                <Box sx={{ mt: 1 }}>
                  <Typography variant="body2" fontWeight="600">
                    Sample Columns:
                  </Typography>
                  <Typography variant="body2" component="div">
                    {data.sample_columns.join(', ')}
                  </Typography>
                </Box>
              )}
            </Alert>
          ) : status === 'error' ? (
            <Alert severity="error">
              <Typography variant="body2">
                {data?.message || 'Connection failed'}
              </Typography>
              <Typography variant="body2" sx={{ mt: 1 }}>
                Please check your backend configuration and ensure Airtable credentials are set correctly.
              </Typography>
            </Alert>
          ) : (
            <Alert severity="info">Testing connection...</Alert>
          )}
        </Box>
      </Collapse>
    </Paper>
  );
}

export default ConnectionTest;



