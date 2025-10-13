import React from 'react';
import { Box, Typography } from '@mui/material';
import SpeakerCard from './SpeakerCard';

function SpeakerList({ speakers, category }) {
  if (!speakers || speakers.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 6 }}>
        <Typography variant="h6" color="text.secondary">
          No {category} speakers found
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      {speakers.map((speaker, index) => (
        <SpeakerCard
          key={index}
          speaker={speaker}
          category={category}
          index={index + 1}
        />
      ))}
    </Box>
  );
}

export default SpeakerList;



