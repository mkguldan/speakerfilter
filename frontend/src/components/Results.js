import React, { useState } from 'react';
import {
  Paper,
  Box,
  Typography,
  Tabs,
  Tab,
  Button,
  ButtonGroup,
  Chip,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import PeopleIcon from '@mui/icons-material/People';
import SpeakerList from './SpeakerList';

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

function Results({ results, onExport }) {
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  if (!results) return null;

  const { summary, confirmed_speakers, intended_speakers, endorsed_speakers } = results;

  return (
    <Paper elevation={2} sx={{ p: 4, borderRadius: 3 }}>
      {/* Header with Summary */}
      <Box sx={{ mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
          <Box>
            <Typography variant="h5" component="h2" gutterBottom fontWeight="600">
              Results for: {results.event_name}
            </Typography>
            {results.event_title && (
              <Typography variant="body1" color="text.secondary">
                {results.event_title}
              </Typography>
            )}
          </Box>

          {/* Export Buttons */}
          <ButtonGroup variant="outlined" size="small">
            <Button
              startIcon={<DownloadIcon />}
              onClick={() => onExport('csv')}
            >
              CSV
            </Button>
            <Button
              startIcon={<DownloadIcon />}
              onClick={() => onExport('json')}
            >
              JSON
            </Button>
            <Button
              startIcon={<DownloadIcon />}
              onClick={() => onExport('text')}
            >
              TXT
            </Button>
          </ButtonGroup>
        </Box>

        {/* Summary Stats */}
        <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
          <Chip
            icon={<PeopleIcon />}
            label={`Total: ${summary.total_count}`}
            color="primary"
            variant="outlined"
          />
          <Chip
            label={`Confirmed: ${summary.confirmed_count}`}
            color="success"
            variant="outlined"
          />
          <Chip
            label={`Intended: ${summary.intended_count}`}
            color="info"
            variant="outlined"
          />
          <Chip
            label={`Endorsed: ${summary.endorsed_count}`}
            color="warning"
            variant="outlined"
          />
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab 
            label={`Confirmed (${summary.confirmed_count})`}
            sx={{ textTransform: 'none', fontWeight: 600 }}
          />
          <Tab 
            label={`Intended (${summary.intended_count})`}
            sx={{ textTransform: 'none', fontWeight: 600 }}
          />
          <Tab 
            label={`Endorsed (${summary.endorsed_count})`}
            sx={{ textTransform: 'none', fontWeight: 600 }}
          />
        </Tabs>
      </Box>

      {/* Tab Panels */}
      <TabPanel value={currentTab} index={0}>
        <SpeakerList speakers={confirmed_speakers} category="confirmed" />
      </TabPanel>
      
      <TabPanel value={currentTab} index={1}>
        <SpeakerList speakers={intended_speakers} category="intended" />
      </TabPanel>
      
      <TabPanel value={currentTab} index={2}>
        <SpeakerList speakers={endorsed_speakers} category="endorsed" />
      </TabPanel>
    </Paper>
  );
}

export default Results;



