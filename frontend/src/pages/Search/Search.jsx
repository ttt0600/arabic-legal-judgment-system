import React from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';

const Search = () => {
  return (
    <Box>
      <Card>
        <CardContent>
          <Typography variant="h4" gutterBottom>
            البحث المتقدم
          </Typography>
          <Typography variant="body1">
            هذه الصفحة قيد التطوير - ستحتوي على أدوات البحث المتقدم في القضايا والأحكام
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Search;
