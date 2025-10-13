import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

function FilterForm({ onFilter, loading, disabled }) {
  const [eventName, setEventName] = useState('');
  const [eventTitle, setEventTitle] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (eventName.trim()) {
      onFilter(eventName.trim(), eventTitle.trim());
    }
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
        Filter Speakers by Event
      </Typography>
      
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <TextField
          fullWidth
          label="Event Name"
          placeholder='e.g., "2511 Barclays"'
          value={eventName}
          onChange={(e) => setEventName(e.target.value)}
          required
          disabled={loading}
          sx={{ mb: 3 }}
          helperText="Enter the event name tag as it appears in Airtable"
        />

        <TextField
          fullWidth
          label="Event Title (Optional)"
          placeholder='e.g., "Digital Transformation in Finance"'
          value={eventTitle}
          onChange={(e) => setEventTitle(e.target.value)}
          disabled={loading}
          sx={{ mb: 3 }}
          helperText="Optional: Helps improve content fit analysis"
        />

        <Button
          type="submit"
          variant="contained"
          size="large"
          fullWidth
          disabled={loading || !eventName.trim() || disabled}
          startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
          sx={{
            py: 1.5,
            fontSize: '1.1rem',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5568d3 0%, #63397d 100%)',
            },
          }}
        >
          {loading ? 'Filtering...' : disabled ? 'Upload CSV First' : 'Filter Speakers'}
        </Button>
      </Box>
    </Paper>
  );
}

export default FilterForm;



