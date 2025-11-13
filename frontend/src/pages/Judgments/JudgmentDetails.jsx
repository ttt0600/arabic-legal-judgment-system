import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const JudgmentDetails = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            تفاصيل الحكم
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستعرض تفاصيل الحكم القضائي
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default JudgmentDetails;
