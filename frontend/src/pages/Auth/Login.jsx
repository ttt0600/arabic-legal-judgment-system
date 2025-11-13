import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
  Divider,
  Paper,
} from '@mui/material';
import {
  Visibility,
  VisibilityOff,
  AccountBalance as AccountBalanceIcon,
  Person as PersonIcon,
  Lock as LockIcon,
} from '@mui/icons-material';
import { toast } from 'react-toastify';

import { useAuth } from '../../contexts/AuthContext';

const Login = () => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const { login, isAuthenticated, error, clearError } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Get redirect location
  const from = location.state?.from?.pathname || '/dashboard';

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  // Clear errors when component unmounts
  useEffect(() => {
    return () => {
      clearError();
    };
  }, [clearError]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials(prev => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear errors when user starts typing
    if (error) {
      clearError();
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!credentials.username.trim() || !credentials.password.trim()) {
      toast.error('يرجى ملء جميع الحقول');
      return;
    }

    setIsLoading(true);
    
    try {
      const result = await login(credentials);
      
      if (result.success) {
        toast.success('تم تسجيل الدخول بنجاح');
        navigate(from, { replace: true });
      } else {
        toast.error(result.error || 'فشل في تسجيل الدخول');
      }
    } catch (err) {
      toast.error('حدث خطأ غير متوقع');
    } finally {
      setIsLoading(false);
    }
  };

  // Toggle password visibility
  const handleTogglePassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 2,
      }}
    >
      <Paper
        elevation={24}
        sx={{
          maxWidth: 450,
          width: '100%',
          borderRadius: 3,
          overflow: 'hidden',
        }}
      >
        {/* Header */}
        <Box
          sx={{
            backgroundColor: 'primary.main',
            color: 'white',
            padding: 4,
            textAlign: 'center',
          }}
        >
          <AccountBalanceIcon sx={{ fontSize: 60, mb: 2 }} />
          <Typography variant="h4" component="h1" sx={{ fontWeight: 600, mb: 1 }}>
            نظام الأحكام القانونية
          </Typography>
          <Typography variant="body1" sx={{ opacity: 0.9 }}>
            تسجيل الدخول إلى النظام
          </Typography>
        </Box>

        {/* Login Form */}
        <CardContent sx={{ padding: 4 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            {/* Username Field */}
            <TextField
              fullWidth
              name="username"
              label="اسم المستخدم"
              value={credentials.username}
              onChange={handleChange}
              margin="normal"
              required
              autoFocus
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <PersonIcon color="action" />
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 2 }}
            />

            {/* Password Field */}
            <TextField
              fullWidth
              name="password"
              type={showPassword ? 'text' : 'password'}
              label="كلمة المرور"
              value={credentials.password}
              onChange={handleChange}
              margin="normal"
              required
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LockIcon color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={handleTogglePassword}
                      edge="end"
                      size="small"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
              sx={{ mb: 3 }}
            />

            {/* Login Button */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              disabled={isLoading}
              sx={{
                height: 50,
                fontSize: '1.1rem',
                fontWeight: 600,
                mb: 3,
              }}
            >
              {isLoading ? 'جاري تسجيل الدخول...' : 'تسجيل الدخول'}
            </Button>

            <Divider sx={{ mb: 3 }}>
              <Typography variant="body2" color="textSecondary">
                أو
              </Typography>
            </Divider>

            {/* Demo Credentials */}
            <Box
              sx={{
                backgroundColor: 'grey.50',
                padding: 2,
                borderRadius: 1,
                border: '1px solid',
                borderColor: 'grey.200',
              }}
            >
              <Typography variant="body2" color="textSecondary" sx={{ mb: 1 }}>
                بيانات تجريبية:
              </Typography>
              <Typography variant="body2">
                <strong>اسم المستخدم:</strong> admin
              </Typography>
              <Typography variant="body2">
                <strong>كلمة المرور:</strong> admin123
              </Typography>
            </Box>
          </form>
        </CardContent>

        {/* Footer */}
        <Box
          sx={{
            backgroundColor: 'grey.50',
            padding: 2,
            textAlign: 'center',
          }}
        >
          <Typography variant="body2" color="textSecondary">
            © 2024 نظام إدارة الأحكام القانونية العربية
          </Typography>
        </Box>
      </Paper>
    </Box>
  );
};

export default Login;
