import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Box,
  Typography,
  Chip,
  IconButton,
  Collapse,
  Divider,
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import BusinessIcon from '@mui/icons-material/Business';
import StarIcon from '@mui/icons-material/Star';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import LocationOnIcon from '@mui/icons-material/LocationOn';

function SpeakerCard({ speaker, category, index }) {
  const [expanded, setExpanded] = useState(false);

  const isDetailed = category === 'intended' || category === 'endorsed';

  return (
    <Card
      elevation={1}
      sx={{
        '&:hover': {
          boxShadow: 3,
        },
        transition: 'all 0.3s',
      }}
    >
      <CardContent>
        {/* Header */}
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
          <Box sx={{ flex: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Typography variant="h6" component="h3" fontWeight="600">
                {index}. {speaker.speaker_name || 'Unknown'}
              </Typography>
              {speaker.rating_flag && (
                <Chip
                  label={speaker.rating_flag}
                  size="small"
                  color={speaker.rating_flag === 'Good option' ? 'success' : 'warning'}
                  icon={<StarIcon />}
                />
              )}
            </Box>

            {speaker.company && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                <BusinessIcon fontSize="small" color="action" />
                <Typography variant="body2" color="text.secondary">
                  {speaker.company}
                </Typography>
              </Box>
            )}

            {speaker.region && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                <LocationOnIcon fontSize="small" color="action" />
                <Typography variant="body2" color="text.secondary">
                  {speaker.region}
                </Typography>
              </Box>
            )}
          </Box>

          {isDetailed && (
            <IconButton onClick={() => setExpanded(!expanded)} size="small">
              {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
            </IconButton>
          )}
        </Box>

        {/* Ratings Summary (always visible for detailed) */}
        {isDetailed && (
          <Box sx={{ display: 'flex', gap: 1, mt: 2, flexWrap: 'wrap' }}>
            {speaker.axel_rating && (
              <Chip
                label={`Axel: ${speaker.axel_rating}`}
                size="small"
                variant="outlined"
              />
            )}
            {speaker.ir_rating && (
              <Chip
                label={`IR: ${speaker.ir_rating}`}
                size="small"
                variant="outlined"
                color="primary"
              />
            )}
            {speaker.jelena_rating && (
              <Chip
                label={`Jelena: ${speaker.jelena_rating}`}
                size="small"
                variant="outlined"
                color="secondary"
              />
            )}
          </Box>
        )}

        {/* Confirmed speakers show tag */}
        {category === 'confirmed' && speaker.tag && (
          <Box sx={{ mt: 2 }}>
            <Chip label={speaker.tag} size="small" color="success" />
          </Box>
        )}

        {/* Expanded Details */}
        {isDetailed && (
          <Collapse in={expanded}>
            <Box sx={{ mt: 3 }}>
              <Divider sx={{ mb: 2 }} />

              {/* Call Notes */}
              {(speaker.in_sum || speaker.call_date) && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                    Call Notes
                  </Typography>
                  {speaker.call_date && (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mb: 1 }}>
                      <CalendarTodayIcon fontSize="small" color="action" />
                      <Typography variant="body2" color="text.secondary">
                        {speaker.call_date}
                      </Typography>
                    </Box>
                  )}
                  {speaker.in_sum && (
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      <strong>In Sum:</strong> {speaker.in_sum}
                    </Typography>
                  )}
                </Box>
              )}

              {/* Jelena's Comments */}
              {speaker.jelena_comments && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                    Jelena's Comments
                  </Typography>
                  <Typography variant="body2">{speaker.jelena_comments}</Typography>
                </Box>
              )}

              {/* Abstract Title */}
              {speaker.abstract_title && (
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                    Abstract
                  </Typography>
                  <Typography variant="body2">{speaker.abstract_title}</Typography>
                </Box>
              )}

              {/* Content Fit Analysis */}
              {speaker.content_fit_analysis && (
                <Box sx={{ mb: 3, p: 2, bgcolor: 'primary.light', borderRadius: 2 }}>
                  <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                    Content Fit Analysis
                  </Typography>
                  <Typography variant="body2">{speaker.content_fit_analysis}</Typography>
                </Box>
              )}

              {/* IR Speaking Engagement */}
              {speaker.ir_engagement && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" fontWeight="600" gutterBottom>
                    IR Speaking Engagement
                  </Typography>
                  <Typography variant="body2">{speaker.ir_engagement}</Typography>
                </Box>
              )}
            </Box>
          </Collapse>
        )}
      </CardContent>
    </Card>
  );
}

export default SpeakerCard;



