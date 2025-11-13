import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const UserProfile = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            الملف الشخصي
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستحتوي على معلومات المستخدم وإعدادات الحساب
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default UserProfile;
