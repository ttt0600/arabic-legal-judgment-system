const express = require('express');
const User = require('../models/User');
const { protect, authorize, requireRole } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/users
// @desc    Get all users with filtering and pagination
// @access  Private (Admin only)
router.get('/', protect, requireRole('admin'), async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      role,
      search
    } = req.query;

    // Build filter object
    const filter = {};
    
    if (role) filter.role = role;
    
    // Search filter
    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: 'i' } },
        { email: { $regex: search, $options: 'i' } }
      ];
    }

    // Pagination
    const skip = (page - 1) * parseInt(limit);

    // Execute query
    const users = await User.find(filter)
      .populate('court', 'name type location.city')
      .select('-password')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await User.countDocuments(filter);
    const totalPages = Math.ceil(total / parseInt(limit));

    res.json({
      success: true,
      data: users,
      pagination: {
        current: parseInt(page),
        pages: totalPages,
        total,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع المستخدمين'
    });
  }
});

// @route   GET /api/users/:id
// @desc    Get single user by ID
// @access  Private
router.get('/:id', protect, async (req, res) => {
  try {
    // Users can only view their own profile unless they're admin
    if (req.user.role !== 'admin' && req.params.id !== req.user._id.toString()) {
      return res.status(403).json({
        success: false,
        message: 'غير مصرح لك بعرض هذا المستخدم'
      });
    }

    const user = await User.findById(req.params.id)
      .populate('court')
      .select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'المستخدم غير موجود'
      });
    }

    res.json({
      success: true,
      data: user
    });

  } catch (error) {
    console.error('Get user error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع المستخدم'
    });
  }
});

module.exports = router;