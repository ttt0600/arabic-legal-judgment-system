import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { authService } from '../services/authService';

// Initial state
const initialState = {
  user: null,
  token: localStorage.getItem('token'),
  loading: true,
  error: null,
  isAuthenticated: false,
};

// Action types
const AUTH_ACTIONS = {
  AUTH_START: 'AUTH_START',
  AUTH_SUCCESS: 'AUTH_SUCCESS',
  AUTH_FAILURE: 'AUTH_FAILURE',
  LOGOUT: 'LOGOUT',
  CLEAR_ERROR: 'CLEAR_ERROR',
  UPDATE_USER: 'UPDATE_USER',
};

// Reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.AUTH_START:
      return {
        ...state,
        loading: true,
        error: null,
      };

    case AUTH_ACTIONS.AUTH_SUCCESS:
      return {
        ...state,
        loading: false,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        error: null,
      };

    case AUTH_ACTIONS.AUTH_FAILURE:
      return {
        ...state,
        loading: false,
        user: null,
        token: null,
        isAuthenticated: false,
        error: action.payload,
      };

    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
        error: null,
      };

    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null,
      };

    case AUTH_ACTIONS.UPDATE_USER:
      return {
        ...state,
        user: { ...state.user, ...action.payload },
      };

    default:
      return state;
  }
};

// Create context
const AuthContext = createContext();

// Auth provider component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check if user is authenticated on app start
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          // Set token in axios headers
          authService.setAuthToken(token);
          
          // Verify token with backend
          const response = await authService.verifyToken();
          if (response.success) {
            dispatch({
              type: AUTH_ACTIONS.AUTH_SUCCESS,
              payload: {
                user: response.user,
                token: token,
              },
            });
          } else {
            // Token is invalid
            localStorage.removeItem('token');
            dispatch({ type: AUTH_ACTIONS.LOGOUT });
          }
        } catch (error) {
          localStorage.removeItem('token');
          dispatch({
            type: AUTH_ACTIONS.AUTH_FAILURE,
            payload: 'جلسة العمل منتهية الصلاحية',
          });
        }
      } else {
        dispatch({ type: AUTH_ACTIONS.LOGOUT });
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (credentials) => {
    dispatch({ type: AUTH_ACTIONS.AUTH_START });
    
    try {
      const response = await authService.login(credentials);
      
      if (response.success) {
        const { user, access_token } = response.data;
        
        // Store token
        localStorage.setItem('token', access_token);
        authService.setAuthToken(access_token);
        
        dispatch({
          type: AUTH_ACTIONS.AUTH_SUCCESS,
          payload: {
            user,
            token: access_token,
          },
        });
        
        return { success: true };
      } else {
        dispatch({
          type: AUTH_ACTIONS.AUTH_FAILURE,
          payload: response.error || 'فشل في تسجيل الدخول',
        });
        return { success: false, error: response.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'حدث خطأ في الاتصال';
      dispatch({
        type: AUTH_ACTIONS.AUTH_FAILURE,
        payload: errorMessage,
      });
      return { success: false, error: errorMessage };
    }
  };

  // Register function
  const register = async (userData) => {
    dispatch({ type: AUTH_ACTIONS.AUTH_START });
    
    try {
      const response = await authService.register(userData);
      
      if (response.success) {
        // Auto login after successful registration
        return await login({
          username: userData.username,
          password: userData.password,
        });
      } else {
        dispatch({
          type: AUTH_ACTIONS.AUTH_FAILURE,
          payload: response.error || 'فشل في إنشاء الحساب',
        });
        return { success: false, error: response.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'حدث خطأ في الاتصال';
      dispatch({
        type: AUTH_ACTIONS.AUTH_FAILURE,
        payload: errorMessage,
      });
      return { success: false, error: errorMessage };
    }
  };

  // Logout function
  const logout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('token');
      authService.removeAuthToken();
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  };

  // Update user profile
  const updateUser = async (userData) => {
    try {
      const response = await authService.updateProfile(userData);
      
      if (response.success) {
        dispatch({
          type: AUTH_ACTIONS.UPDATE_USER,
          payload: response.data,
        });
        return { success: true };
      } else {
        return { success: false, error: response.error };
      }
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'حدث خطأ في التحديث';
      return { success: false, error: errorMessage };
    }
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  };

  // Change password
  const changePassword = async (passwordData) => {
    try {
      const response = await authService.changePassword(passwordData);
      return response;
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'حدث خطأ في تغيير كلمة المرور';
      return { success: false, error: errorMessage };
    }
  };

  // Check if user has specific permission
  const hasPermission = (permission) => {
    if (!state.user) return false;
    
    // Admin has all permissions
    if (state.user.role === 'admin') return true;
    
    // Define role-based permissions
    const rolePermissions = {
      judge: ['view_cases', 'create_judgment', 'view_judgments', 'view_documents'],
      lawyer: ['view_cases', 'create_case', 'view_judgments', 'upload_documents'],
      user: ['view_cases', 'view_judgments'],
    };
    
    const userPermissions = rolePermissions[state.user.role] || [];
    return userPermissions.includes(permission);
  };

  // Check if user has specific role
  const hasRole = (role) => {
    return state.user?.role === role;
  };

  const value = {
    ...state,
    login,
    register,
    logout,
    updateUser,
    clearError,
    changePassword,
    hasPermission,
    hasRole,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export { AUTH_ACTIONS };
