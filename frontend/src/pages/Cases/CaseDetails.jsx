import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const CaseDetails = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            تفاصيل القضية
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستعرض تفاصيل القضية المحددة
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CaseDetails;
