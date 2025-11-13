import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const DocumentsList = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            إدارة المستندات
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستعرض قائمة بجميع المستندات مع إمكانيات الرفع والتحميل
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DocumentsList;
