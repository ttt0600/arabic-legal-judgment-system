const express = require('express');
const Judgment = require('../models/Judgment');
const Case = require('../models/Case');
const Court = require('../models/Court');
const { protect, authorize, requireRole } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/judgments
// @desc    Get all judgments with filtering and pagination
// @access  Private
router.get('/', protect, authorize('view_judgment'), async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      type,
      decision,
      court,
      judge,
      status,
      search
    } = req.query;

    // Build filter object
    const filter = {};
    
    // Role-based filtering
    if (req.user.role !== 'admin') {
      if (req.user.role === 'judge') {
        filter.judge = req.user._id;
      } else if (req.user.court) {
        filter.court = req.user.court._id;
      }
    }

    if (type) filter.type = type;
    if (decision) filter.decision = decision;
    if (court) filter.court = court;
    if (judge) filter.judge = judge;
    if (status) filter.status = status;

    // Search filter
    if (search) {
      filter.$or = [
        { judgmentNumber: { $regex: search, $options: 'i' } },
        { summary: { $regex: search, $options: 'i' } }
      ];
    }

    // Pagination
    const skip = (page - 1) * parseInt(limit);

    // Execute query
    const judgments = await Judgment.find(filter)
      .populate('case', 'caseNumber title type')
      .populate('court', 'name type location.city')
      .populate('judge', 'name')
      .select('-content.introduction -content.facts -content.legalAnalysis -content.reasoning')
      .sort({ 'dates.issuedDate': -1 })
      .skip(skip)
      .limit(parseInt(limit));

    // Get total count for pagination
    const total = await Judgment.countDocuments(filter);
    const totalPages = Math.ceil(total / parseInt(limit));

    res.json({
      success: true,
      data: judgments,
      pagination: {
        current: parseInt(page),
        pages: totalPages,
        total,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get judgments error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع الأحكام'
    });
  }
});

// @route   GET /api/judgments/:id
// @desc    Get single judgment by ID
// @access  Private
router.get('/:id', protect, authorize('view_judgment'), async (req, res) => {
  try {
    const judgment = await Judgment.findById(req.params.id)
      .populate('case')
      .populate('court')
      .populate('judge', 'name email profile');

    if (!judgment) {
      return res.status(404).json({
        success: false,
        message: 'الحكم غير موجود'
      });
    }

    res.json({
      success: true,
      data: judgment
    });

  } catch (error) {
    console.error('Get judgment error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع الحكم'
    });
  }
});

// @route   POST /api/judgments
// @desc    Create new judgment
// @access  Private
router.post('/', protect, authorize('create_judgment'), async (req, res) => {
  try {
    // Verify case and court exist
    const [case_, court] = await Promise.all([
      Case.findById(req.body.case),
      Court.findById(req.body.court)
    ]);

    if (!case_) {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }

    if (!court) {
      return res.status(404).json({
        success: false,
        message: 'المحكمة غير موجودة'
      });
    }

    // Generate judgment number (simplified)
    const judgmentCount = await Judgment.countDocuments({ court: req.body.court });
    const currentYear = new Date().getFullYear();
    const judgmentNumber = `${currentYear}/${String(judgmentCount + 1).padStart(4, '0')}`;

    // Create judgment
    const judgmentData = {
      ...req.body,
      judgmentNumber,
      judge: req.user._id,
      metadata: {
        createdBy: req.user._id,
        lastModifiedBy: req.user._id
      }
    };

    const newJudgment = new Judgment(judgmentData);
    await newJudgment.save();

    res.status(201).json({
      success: true,
      message: 'تم إنشاء الحكم بنجاح',
      data: newJudgment
    });

  } catch (error) {
    console.error('Create judgment error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في إنشاء الحكم'
    });
  }
});

module.exports = router;