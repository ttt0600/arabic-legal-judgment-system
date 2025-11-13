import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const CreateCase = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            إنشاء قضية جديدة
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستحتوي على نموذج لإنشاء قضية جديدة
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default CreateCase;
