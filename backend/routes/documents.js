const express = require('express');
const multer = require('multer');
const path = require('path');
const Document = require('../models/Document');
const Case = require('../models/Case');
const { protect, authorize } = require('../utils/auth');

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({
  storage: storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB
  },
  fileFilter: (req, file, cb) => {
    // Allow common document types
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/jpeg',
      'image/png',
      'text/plain'
    ];
    
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('نوع الملف غير مدعوم'), false);
    }
  }
});

// @route   GET /api/documents
// @desc    Get all documents with filtering and pagination
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const {
      page = 1,
      limit = 10,
      type,
      case: caseId,
      search
    } = req.query;

    // Build filter object
    const filter = { status: 'active' };
    
    if (type) filter.type = type;
    if (caseId) filter.case = caseId;
    
    // Search filter
    if (search) {
      filter.$or = [
        { title: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } }
      ];
    }

    // Pagination
    const skip = (page - 1) * parseInt(limit);

    // Execute query
    const documents = await Document.find(filter)
      .populate('case', 'caseNumber title')
      .populate('court', 'name')
      .populate('uploadedBy', 'name')
      .select('-content.text') // Exclude large text content
      .sort({ 'dates.uploaded': -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Document.countDocuments(filter);
    const totalPages = Math.ceil(total / parseInt(limit));

    res.json({
      success: true,
      data: documents,
      pagination: {
        current: parseInt(page),
        pages: totalPages,
        total,
        hasNext: page < totalPages,
        hasPrev: page > 1
      }
    });

  } catch (error) {
    console.error('Get documents error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع الوثائق'
    });
  }
});

// @route   POST /api/documents
// @desc    Upload new document
// @access  Private
router.post('/', protect, upload.single('file'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: 'الملف مطلوب'
      });
    }

    const { title, description, type, category, case: caseId } = req.body;

    if (!title || !type || !category) {
      return res.status(400).json({
        success: false,
        message: 'العنوان ونوع الوثيقة والفئة مطلوبة'
      });
    }

    // Verify case exists if provided
    if (caseId) {
      const case_ = await Case.findById(caseId);
      if (!case_) {
        return res.status(404).json({
          success: false,
          message: 'القضية غير موجودة'
        });
      }
    }

    // Create document
    const documentData = {
      title,
      description,
      type,
      category,
      case: caseId,
      court: req.user.court?._id,
      file: {
        filename: req.file.filename,
        originalName: req.file.originalname,
        path: req.file.path,
        size: req.file.size,
        mimeType: req.file.mimetype,
        extension: path.extname(req.file.originalname).slice(1)
      },
      uploadedBy: req.user._id,
      processing: {
        status: 'uploaded'
      }
    };

    const newDocument = new Document(documentData);
    await newDocument.save();

    const populatedDocument = await Document.findById(newDocument._id)
      .populate('case', 'caseNumber title')
      .populate('court', 'name')
      .populate('uploadedBy', 'name');

    res.status(201).json({
      success: true,
      message: 'تم رفع الوثيقة بنجاح',
      data: populatedDocument
    });

  } catch (error) {
    console.error('Upload document error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في رفع الوثيقة'
    });
  }
});

module.exports = router;