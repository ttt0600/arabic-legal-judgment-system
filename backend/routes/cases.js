const express = require('express');
const Case = require('../models/Case');
const Court = require('../models/Court');
const { protect, authorize, requireRole } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/cases
// @desc    Get all cases with filtering and pagination
// @access  Private
router.get('/', protect, authorize('view_case'), async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      status,
      type,
      court,
      judge,
      priority,
      search,
      sortBy = 'dates.filed',
      sortOrder = 'desc',
      dateFrom,
      dateTo
    } = req.query;

    // Build filter object
    const filter = {};
    
    // Role-based filtering
    if (req.user.role !== 'admin') {
      if (req.user.role === 'judge') {
        filter.judge = req.user._id;
      } else if (req.user.role === 'clerk') {
        filter.clerk = req.user._id;
      } else if (req.user.court) {
        filter.court = req.user.court._id;
      }
    }

    if (status) filter.status = status;
    if (type) filter.type = type;
    if (court) filter.court = court;
    if (judge) filter.judge = judge;
    if (priority) filter.priority = priority;
    
    // Date range filter
    if (dateFrom || dateTo) {
      filter['dates.filed'] = {};
      if (dateFrom) filter['dates.filed'].$gte = new Date(dateFrom);
      if (dateTo) filter['dates.filed'].$lte = new Date(dateTo);
    }

    // Search filter
    if (search) {
      filter.$or = [
        { title: { $regex: search, $options: 'i' } },
        { caseNumber: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } },
        { 'parties.plaintiffs.name': { $regex: search, $options: 'i' } },
        { 'parties.defendants.name': { $regex: search, $options: 'i' } }
      ];
    }

    // Pagination
    const skip = (page - 1) * parseInt(limit);
    const sortOptions = {};
    sortOptions[sortBy] = sortOrder === 'desc' ? -1 : 1;

    // Execute query
    const cases = await Case.find(filter)
      .populate('court', 'name type location.city')
      .populate('judge', 'name')
      .populate('clerk', 'name')
      .populate('parties.plaintiffs.lawyer', 'name')
      .populate('parties.defendants.lawyer', 'name')
      .sort(sortOptions)
      .skip(skip)
      .limit(parseInt(limit));

    // Get total count for pagination
    const total = await Case.countDocuments(filter);
    const totalPages = Math.ceil(total / parseInt(limit));

    res.json({
      success: true,
      data: cases,
      pagination: {
        current: parseInt(page),
        pages: totalPages,
        total,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get cases error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع القضايا'
    });
  }
});

// @route   POST /api/cases
// @desc    Create new case
// @access  Private
router.post('/', protect, authorize('create_case'), async (req, res) => {
  try {
    // Basic validation
    const { title, description, type, category, court } = req.body;
    
    if (!title || !description || !type || !category || !court) {
      return res.status(400).json({
        success: false,
        message: 'البيانات الأساسية مطلوبة'
      });
    }

    // Verify court exists and user has access
    const courtDoc = await Court.findById(court);
    if (!courtDoc) {
      return res.status(404).json({
        success: false,
        message: 'المحكمة غير موجودة'
      });
    }

    // Check court access
    if (req.user.role !== 'admin' && req.user.court && req.user.court._id.toString() !== court) {
      return res.status(403).json({
        success: false,
        message: 'غير مصرح لك بإنشاء قضايا في هذه المحكمة'
      });
    }

    // Generate case number (simplified)
    const caseCount = await Case.countDocuments({ court: court });
    const currentYear = new Date().getFullYear();
    const caseNumber = `${currentYear}/${String(caseCount + 1).padStart(4, '0')}`;

    // Create case
    const caseData = {
      ...req.body,
      caseNumber,
      dates: {
        filed: new Date(),
        ...req.body.dates
      },
      clerk: req.user.role === 'clerk' ? req.user._id : req.body.clerk,
      metadata: {
        lastModifiedBy: req.user._id
      }
    };

    const newCase = new Case(caseData);

    // Add initial timeline event
    newCase.timeline.push({
      event: 'case_created',
      description: 'تم إنشاء القضية',
      user: req.user._id
    });

    await newCase.save();

    // Populate response
    const populatedCase = await Case.findById(newCase._id)
      .populate('court', 'name type')
      .populate('judge', 'name')
      .populate('clerk', 'name');

    res.status(201).json({
      success: true,
      message: 'تم إنشاء القضية بنجاح',
      data: populatedCase
    });

  } catch (error) {
    console.error('Create case error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في إنشاء القضية'
    });
  }
});

// @route   GET /api/cases/:id
// @desc    Get single case by ID
// @access  Private
router.get('/:id', protect, authorize('view_case'), async (req, res) => {
  try {
    const case_ = await Case.findById(req.params.id)
      .populate('court')
      .populate('judge', 'name email profile')
      .populate('clerk', 'name email')
      .populate('parties.plaintiffs.lawyer', 'name email profile')
      .populate('parties.defendants.lawyer', 'name email profile')
      .populate('timeline.user', 'name')
      .populate('relatedCases.case', 'caseNumber title');

    if (!case_) {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }

    // Check access permissions
    if (req.user.role !== 'admin') {
      let hasAccess = false;
      
      if (req.user.role === 'judge' && case_.judge && case_.judge._id.toString() === req.user._id.toString()) {
        hasAccess = true;
      } else if (req.user.role === 'clerk' && case_.clerk && case_.clerk._id.toString() === req.user._id.toString()) {
        hasAccess = true;
      } else if (req.user.court && case_.court._id.toString() === req.user.court._id.toString()) {
        hasAccess = true;
      } else if (case_.confidentialityLevel === 'public') {
        hasAccess = true;
      }
      
      if (!hasAccess) {
        return res.status(403).json({
          success: false,
          message: 'غير مصرح لك بعرض هذه القضية'
        });
      }
    }

    res.json({
      success: true,
      data: case_
    });

  } catch (error) {
    console.error('Get case error:', error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع القضية'
    });
  }
});

// @route   PUT /api/cases/:id
// @desc    Update case
// @access  Private
router.put('/:id', protect, authorize('edit_case'), async (req, res) => {
  try {
    const case_ = await Case.findById(req.params.id);
    
    if (!case_) {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }

    // Check edit permissions
    let canEdit = false;
    if (req.user.role === 'admin') canEdit = true;
    else if (req.user.role === 'judge' && case_.judge && case_.judge.toString() === req.user._id.toString()) canEdit = true;
    else if (req.user.role === 'clerk' && case_.clerk && case_.clerk.toString() === req.user._id.toString()) canEdit = true;

    if (!canEdit) {
      return res.status(403).json({
        success: false,
        message: 'غير مصرح لك بتعديل هذه القضية'
      });
    }

    // Update case
    const updatedFields = { ...req.body };
    updatedFields.metadata = {
      ...case_.metadata,
      lastModifiedBy: req.user._id,
      version: (case_.metadata.version || 1) + 1
    };

    const updatedCase = await Case.findByIdAndUpdate(
      req.params.id,
      updatedFields,
      { new: true, runValidators: true }
    ).populate('court judge clerk');

    // Add timeline event
    updatedCase.timeline.push({
      event: 'case_updated',
      description: 'تم تحديث بيانات القضية',
      user: req.user._id,
      date: new Date()
    });

    await updatedCase.save();

    res.json({
      success: true,
      message: 'تم تحديث القضية بنجاح',
      data: updatedCase
    });

  } catch (error) {
    console.error('Update case error:', error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }
    res.status(500).json({
      success: false,
      message: 'خطأ في تحديث القضية'
    });
  }
});

// @route   DELETE /api/cases/:id
// @desc    Delete case (Admin only)
// @access  Private
router.delete('/:id', protect, requireRole('admin'), async (req, res) => {
  try {
    const case_ = await Case.findById(req.params.id);
    
    if (!case_) {
      return res.status(404).json({
        success: false,
        message: 'القضية غير موجودة'
      });
    }

    // Check if case can be deleted
    if (['final', 'archived'].includes(case_.status)) {
      return res.status(400).json({
        success: false,
        message: 'لا يمكن حذف قضية نهائية أو مؤرشفة'
      });
    }

    await Case.findByIdAndDelete(req.params.id);

    res.json({
      success: true,
      message: 'تم حذف القضية بنجاح'
    });

  } catch (error) {
    console.error('Delete case error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في حذف القضية'
    });
  }
});

module.exports = router;