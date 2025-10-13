import React, { useState, useCallback } from 'react';
import {
  Paper,
  Box,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  IconButton,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

function FileUpload({ onFileSelect, selectedFile, onFileClear }) {
  const [dragActive, setDragActive] = useState(false);
  const [fileInfo, setFileInfo] = useState(null);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    // Check if file is CSV
    if (!file.name.endsWith('.csv')) {
      alert('Please upload a CSV file');
      return;
    }

    // Check file size (1GB limit)
    const maxSize = 1024 * 1024 * 1024; // 1GB
    if (file.size > maxSize) {
      alert('File size exceeds 1GB limit');
      return;
    }

    const info = {
      name: file.name,
      size: (file.size / 1024 / 1024).toFixed(2) + ' MB',
      type: file.type,
    };

    setFileInfo(info);
    onFileSelect(file);
  };

  const handleClear = () => {
    setFileInfo(null);
    onFileClear();
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 4,
        mb: 4,
        borderRadius: 3,
      }}
    >
      <Typography variant="h5" component="h2" gutterBottom fontWeight="600">
        Upload Speaker Data CSV
      </Typography>

      {!selectedFile ? (
        <Box
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          sx={{
            mt: 3,
            p: 6,
            border: '2px dashed',
            borderColor: dragActive ? 'primary.main' : 'grey.300',
            borderRadius: 2,
            bgcolor: dragActive ? 'primary.light' : 'grey.50',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.3s',
            '&:hover': {
              borderColor: 'primary.main',
              bgcolor: 'primary.light',
            },
          }}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <CloudUploadIcon sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            Drop your CSV file here
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            or click to browse
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Maximum file size: 1GB
          </Typography>
          
          <input
            id="fileInput"
            type="file"
            accept=".csv"
            onChange={handleChange}
            style={{ display: 'none' }}
          />
        </Box>
      ) : (
        <Box sx={{ mt: 3 }}>
          <Alert 
            severity="success" 
            icon={<CheckCircleIcon fontSize="inherit" />}
            action={
              <IconButton
                aria-label="remove"
                color="inherit"
                size="small"
                onClick={handleClear}
              >
                <DeleteIcon fontSize="inherit" />
              </IconButton>
            }
          >
            <Typography variant="body2">
              <strong>File ready:</strong> {fileInfo?.name}
            </Typography>
            <Typography variant="caption">
              Size: {fileInfo?.size}
            </Typography>
          </Alert>
        </Box>
      )}

      <Box sx={{ mt: 3 }}>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          <strong>Required CSV columns:</strong>
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mt: 1 }}>
          {[
            'Name',
            'Workshops',
            "Axel's rating",
            'Notes speaker calls',
            "Jelena's comments",
            'Abstract',
            'Company',
            'Region',
            'IR Speaking engagement',
            'Activity notes'
          ].map((col) => (
            <Chip key={col} label={col} size="small" variant="outlined" />
          ))}
        </Box>
      </Box>
    </Paper>
  );
}

export default FileUpload;

