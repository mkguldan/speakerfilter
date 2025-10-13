import React, { useState } from 'react';
import {
  Container,
  Box,
  ThemeProvider,
  createTheme,
  CssBaseline,
  Snackbar,
  Alert
} from '@mui/material';
import Header from './components/Header';
import FilterForm from './components/FilterForm';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import api from './services/api';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
    background: {
      default: '#f5f7fa',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 4px 20px rgba(0,0,0,0.08)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
  },
});

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'info'
  });

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResults(null); // Clear previous results
    setSnackbar({
      open: true,
      message: `File "${file.name}" ready to process!`,
      severity: 'info'
    });
  };

  const handleFileClear = () => {
    setSelectedFile(null);
    setResults(null);
  };

  const handleFilter = async (eventName, eventTitle) => {
    if (!selectedFile) {
      setSnackbar({
        open: true,
        message: 'Please upload a CSV file first!',
        severity: 'warning'
      });
      return;
    }

    setLoading(true);
    try {
      const response = await api.filterSpeakersCSV(eventName, eventTitle, selectedFile);
      setResults(response.data);
      setSnackbar({
        open: true,
        message: 'Speakers filtered successfully!',
        severity: 'success'
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: error.response?.data?.detail || 'Error filtering speakers',
        severity: 'error'
      });
      console.error('Error filtering speakers:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (format) => {
    if (!results || !selectedFile) return;
    
    try {
      await api.exportSpeakersCSV(
        format,
        results.event_name,
        results.event_title,
        selectedFile
      );
      setSnackbar({
        open: true,
        message: `Export started! Your ${format.toUpperCase()} file will download shortly.`,
        severity: 'success'
      });
    } catch (error) {
      setSnackbar({
        open: true,
        message: 'Error exporting data',
        severity: 'error'
      });
      console.error('Error exporting:', error);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar({ ...snackbar, open: false });
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        py: 4
      }}>
        <Container maxWidth="xl">
          <Header />
          
          <FileUpload 
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile}
            onFileClear={handleFileClear}
          />

          <FilterForm 
            onFilter={handleFilter} 
            loading={loading}
            disabled={!selectedFile}
          />

          {results && (
            <Results 
              results={results} 
              onExport={handleExport}
            />
          )}
        </Container>

        <Snackbar
          open={snackbar.open}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert 
            onClose={handleCloseSnackbar} 
            severity={snackbar.severity}
            variant="filled"
            sx={{ width: '100%' }}
          >
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}

export default App;



