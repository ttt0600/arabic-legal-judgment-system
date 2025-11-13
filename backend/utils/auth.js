const jwt = require('jsonwebtoken');
const User = require('../models/User');

// Middleware to protect routes
const protect = async (req, res, next) => {
  try {
    let token;

    // Get token from header
    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }

    // Make sure token exists
    if (!token) {
      return res.status(401).json({
        success: false,
        message: 'غير مصرح، لا يوجد رمز دخول'
      });
    }

    try {
      // Verify token
      const decoded = jwt.verify(token, process.env.JWT_SECRET);

      // Get user from token
      const user = await User.findById(decoded.userId).populate('court');
      
      if (!user) {
        return res.status(401).json({
          success: false,
          message: 'غير مصرح، المستخدم غير موجود'
        });
      }

      if (!user.isActive) {
        return res.status(401).json({
          success: false,
          message: 'غير مصرح، الحساب غير مفعل'
        });
      }

      req.user = user;
      next();
    } catch (error) {
      return res.status(401).json({
        success: false,
        message: 'غير مصرح، رمز دخول غير صحيح'
      });
    }
  } catch (error) {
    console.error('Auth middleware error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في الخادم الداخلي'
    });
  }
};

// Middleware to check specific permissions
const authorize = (...permissions) => {
  return (req, res, next) => {
    // Simple permission check - in a full implementation, you'd check user permissions
    // For now, we'll just allow admins and judges to do most things
    if (req.user.role === 'admin' || req.user.role === 'judge') {
      return next();
    }
    
    // Check if user has specific permissions
    const userPermissions = req.user.getEffectivePermissions ? req.user.getEffectivePermissions() : [];
    const hasPermission = permissions.some(permission => userPermissions.includes(permission));

    if (!hasPermission) {
      return res.status(403).json({
        success: false,
        message: 'غير مصرح، ليس لديك الصلاحيات المطلوبة'
      });
    }

    next();
  };
};

// Middleware to check roles
const requireRole = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({
        success: false,
        message: 'غير مصرح'
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        success: false,
        message: 'غير مصرح، الدور غير مناسب'
      });
    }

    next();
  };
};

// Optional authentication middleware (doesn't fail if no token)
const optionalAuth = async (req, res, next) => {
  try {
    let token;

    if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }

    if (token) {
      try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        const user = await User.findById(decoded.userId).populate('court');
        
        if (user && user.isActive) {
          req.user = user;
        }
      } catch (error) {
        // Token invalid, but that's okay for optional auth
        console.log('Optional auth failed:', error.message);
      }
    }

    next();
  } catch (error) {
    console.error('Optional auth middleware error:', error);
    next();
  }
};

module.exports = {
  protect,
  authorize,
  requireRole,
  optionalAuth
};