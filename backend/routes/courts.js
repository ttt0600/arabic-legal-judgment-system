const express = require('express');
const Court = require('../models/Court');
const { protect, authorize, requireRole } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/courts
// @desc    Get all courts with filtering and pagination
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const {
      page = 1,
      limit = 20,
      type,
      jurisdiction,
      city,
      status = 'active',
      search
    } = req.query;

    // Build filter object
    const filter = {};
    
    if (type) filter.type = type;
    if (jurisdiction) filter.jurisdiction = jurisdiction;
    if (city) filter['location.city'] = city;
    if (status) filter.status = status;
    
    // Search filter
    if (search) {
      filter.$or = [
        { name: { $regex: search, $options: 'i' } },
        { nameEn: { $regex: search, $options: 'i' } },
        { 'location.city': { $regex: search, $options: 'i' } },
        { 'location.region': { $regex: search, $options: 'i' } }
      ];
    }

    // Pagination
    const skip = (page - 1) * parseInt(limit);

    // Execute query
    const courts = await Court.find(filter)
      .populate('parentCourt', 'name type')
      .sort({ name: 1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Court.countDocuments(filter);
    const totalPages = Math.ceil(total / parseInt(limit));

    res.json({
      success: true,
      data: courts,
      pagination: {
        current: parseInt(page),
        pages: totalPages,
        total,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get courts error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع المحاكم'
    });
  }
});

// @route   GET /api/courts/:id
// @desc    Get single court by ID
// @access  Private
router.get('/:id', protect, async (req, res) => {
  try {
    const court = await Court.findById(req.params.id)
      .populate('parentCourt', 'name type location');

    if (!court) {
      return res.status(404).json({
        success: false,
        message: 'المحكمة غير موجودة'
      });
    }

    res.json({
      success: true,
      data: court
    });

  } catch (error) {
    console.error('Get court error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع المحكمة'
    });
  }
});

// @route   POST /api/courts
// @desc    Create new court
// @access  Private (Admin only)
router.post('/', protect, requireRole('admin'), async (req, res) => {
  try {
    const {
      name,
      nameEn,
      type,
      level,
      jurisdiction,
      location,
      contact,
      parentCourt
    } = req.body;

    // Validate required fields
    if (!name || !type || !level || !jurisdiction || !location?.city || !location?.region) {
      return res.status(400).json({
        success: false,
        message: 'البيانات الأساسية للمحكمة مطلوبة'
      });
    }

    // Check if parent court exists
    if (parentCourt) {
      const parent = await Court.findById(parentCourt);
      if (!parent) {
        return res.status(404).json({
          success: false,
          message: 'المحكمة الأم غير موجودة'
        });
      }
    }

    // Create court
    const courtData = {
      name,
      nameEn,
      type,
      level,
      jurisdiction,
      location,
      contact,
      parentCourt,
      settings: {
        caseNumberFormat: 'YYYY/MM/####',
        judgmentNumberFormat: 'YYYY/####',
        defaultLanguage: 'ar',
        timezone: 'Asia/Riyadh'
      }
    };

    const court = new Court(courtData);
    await court.save();

    const populatedCourt = await Court.findById(court._id)
      .populate('parentCourt', 'name type');

    res.status(201).json({
      success: true,
      message: 'تم إنشاء المحكمة بنجاح',
      data: populatedCourt
    });

  } catch (error) {
    console.error('Create court error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في إنشاء المحكمة'
    });
  }
});

module.exports = router;