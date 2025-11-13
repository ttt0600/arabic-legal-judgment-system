import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const JudgmentsList = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            قائمة الأحكام
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستعرض قائمة بجميع الأحكام القضائية
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default JudgmentsList;
