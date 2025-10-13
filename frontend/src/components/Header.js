import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import FilterListIcon from '@mui/icons-material/FilterList';

function Header() {
  return (
    <Paper
      elevation={3}
      sx={{
        p: 4,
        mb: 4,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        borderRadius: 3,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <FilterListIcon sx={{ fontSize: 48, mr: 2 }} />
        <Typography variant="h3" component="h1" fontWeight="bold">
          Speaker Prospect Filtering Tool
        </Typography>
      </Box>
      <Typography variant="h6" sx={{ opacity: 0.9 }}>
        Filter and organize speaker prospects from Airtable into Confirmed, Intended, and Endorsed categories
      </Typography>
    </Paper>
  );
}

export default Header;



