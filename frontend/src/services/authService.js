import API from './api';

class AuthService {
  // Set authorization token
  setAuthToken = (token) => {
    if (token) {
      API.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete API.defaults.headers.common['Authorization'];
    }
  };

  // Remove authorization token
  removeAuthToken = () => {
    delete API.defaults.headers.common['Authorization'];
  };

  // Login user
  login = async (credentials) => {
    try {
      const response = await API.post('/auth/login', credentials);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تسجيل الدخول',
      };
    }
  };

  // Register user
  register = async (userData) => {
    try {
      const response = await API.post('/auth/register', userData);
      return {
        success: true,
        data: response.data,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في إنشاء الحساب',
      };
    }
  };

  // Logout user
  logout = async () => {
    try {
      await API.post('/auth/logout');
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تسجيل الخروج',
      };
    }
  };

  // Verify token
  verifyToken = async () => {
    try {
      const response = await API.get('/auth/verify');
      return {
        success: true,
        user: response.data.user,
      };
    } catch (error) {
      return {
        success: false,
        error: 'الرمز المميز غير صالح',
      };
    }
  };

  // Update user profile
  updateProfile = async (userData) => {
    try {
      const response = await API.put('/auth/profile', userData);
      return {
        success: true,
        data: response.data.user,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تحديث الملف الشخصي',
      };
    }
  };

  // Change password
  changePassword = async (passwordData) => {
    try {
      const response = await API.put('/auth/change-password', passwordData);
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في تغيير كلمة المرور',
      };
    }
  };

  // Forgot password
  forgotPassword = async (email) => {
    try {
      const response = await API.post('/auth/forgot-password', { email });
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في إرسال رابط إعادة تعيين كلمة المرور',
      };
    }
  };

  // Reset password
  resetPassword = async (token, newPassword) => {
    try {
      const response = await API.post('/auth/reset-password', {
        token,
        password: newPassword,
      });
      return {
        success: true,
        message: response.data.message,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'حدث خطأ في إعادة تعيين كلمة المرور',
      };
    }
  };
}

export const authService = new AuthService();
