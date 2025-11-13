import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const CasesList = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            قائمة القضايا
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستعرض قائمة بجميع القضايا مع إمكانيات البحث والتصفية
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CasesList;
