const express = require('express');
const Case = require('../models/Case');
const Judgment = require('../models/Judgment');
const Document = require('../models/Document');
const { protect, optionalAuth } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/search
// @desc    Universal search across all entities
// @access  Private
router.get('/', protect, async (req, res) => {
  try {
    const {
      q: query,
      type = 'all',
      page = 1,
      limit = 10,
      court,
      dateFrom,
      dateTo
    } = req.query;

    if (!query || query.trim().length < 2) {
      return res.status(400).json({
        success: false,
        message: 'يجب أن يكون النص المراد البحث عنه حرفين على الأقل'
      });
    }

    // Build base filter based on user role
    let baseFilter = {};
    
    if (req.user.role !== 'admin') {
      if (req.user.role === 'judge') {
        baseFilter.judge = req.user._id;
      } else if (req.user.court) {
        baseFilter.court = req.user.court._id;
      }
    }
    
    if (court) {
      baseFilter.court = court;
    }

    // Date range filter
    const dateFilter = {};
    if (dateFrom) dateFilter.$gte = new Date(dateFrom);
    if (dateTo) dateFilter.$lte = new Date(dateTo);

    // Pagination
    const skip = (page - 1) * parseInt(limit);
    const limitNum = parseInt(limit);

    let results = {
      cases: [],
      judgments: [],
      documents: [],
      total: 0
    };

    // Search cases
    if (type === 'all' || type === 'cases') {
      const caseFilter = { ...baseFilter };
      if (Object.keys(dateFilter).length > 0) {
        caseFilter['dates.filed'] = dateFilter;
      }

      const caseResults = await Case.find({
        ...caseFilter,
        $or: [
          { title: { $regex: query, $options: 'i' } },
          { caseNumber: { $regex: query, $options: 'i' } },
          { description: { $regex: query, $options: 'i' } }
        ]
      })
      .populate('court', 'name')
      .populate('judge', 'name')
      .select('caseNumber title description type status dates court judge')
      .skip(type === 'cases' ? skip : 0)
      .limit(type === 'cases' ? limitNum : 5);

      results.cases = caseResults;
    }

    // Search judgments  
    if (type === 'all' || type === 'judgments') {
      const judgmentFilter = { ...baseFilter };
      if (Object.keys(dateFilter).length > 0) {
        judgmentFilter['dates.issuedDate'] = dateFilter;
      }

      const judgmentResults = await Judgment.find({
        ...judgmentFilter,
        $or: [
          { judgmentNumber: { $regex: query, $options: 'i' } },
          { summary: { $regex: query, $options: 'i' } }
        ]
      })
      .populate('case', 'caseNumber title')
      .populate('court', 'name')
      .populate('judge', 'name')
      .select('judgmentNumber type decision summary dates case court judge')
      .skip(type === 'judgments' ? skip : 0)
      .limit(type === 'judgments' ? limitNum : 5);

      results.judgments = judgmentResults;
    }

    // Search documents
    if (type === 'all' || type === 'documents') {
      const documentFilter = {
        ...baseFilter,
        status: 'active'
      };
      if (Object.keys(dateFilter).length > 0) {
        documentFilter['dates.uploaded'] = dateFilter;
      }

      const documentResults = await Document.find({
        ...documentFilter,
        $or: [
          { title: { $regex: query, $options: 'i' } },
          { description: { $regex: query, $options: 'i' } }
        ]
      })
      .populate('case', 'caseNumber title')
      .populate('court', 'name')
      .populate('uploadedBy', 'name')
      .select('title description type category file.size dates case court uploadedBy')
      .skip(type === 'documents' ? skip : 0)
      .limit(type === 'documents' ? limitNum : 5);

      results.documents = documentResults;
    }

    // Calculate total results
    results.total = results.cases.length + results.judgments.length + results.documents.length;

    res.json({
      success: true,
      data: results,
      pagination: {
        current: parseInt(page),
        total: results.total
      },
      query: {
        searchTerm: query,
        type
      }
    });

  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في البحث'
    });
  }
});

// @route   GET /api/search/public
// @desc    Public search for published judgments only
// @access  Public
router.get('/public', async (req, res) => {
  try {
    const {
      q: query,
      page = 1,
      limit = 10,
      type,
      decision,
      court
    } = req.query;

    if (!query || query.trim().length < 2) {
      return res.status(400).json({
        success: false,
        message: 'يجب أن يكون النص المراد البحث عنه حرفين على الأقل'
      });
    }

    // Build filter for published judgments only
    const filter = {
      'publication.isPublished': true,
      status: { $in: ['issued', 'effective', 'executed'] }
    };

    if (type) filter.type = type;
    if (decision) filter.decision = decision;
    if (court) filter.court = court;

    // Add text search
    filter.$or = [
      { summary: { $regex: query, $options: 'i' } },
      { judgmentNumber: { $regex: query, $options: 'i' } }
    ];

    // Pagination
    const skip = (page - 1) * parseInt(limit);

    // Execute search with anonymized results
    const judgments = await Judgment.find(filter)
      .populate('court', 'name type location.city')
      .select('-parties -case') // Remove identifying information
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Judgment.countDocuments(filter);

    res.json({
      success: true,
      data: judgments,
      pagination: {
        current: parseInt(page),
        total
      }
    });

  } catch (error) {
    console.error('Public search error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في البحث العام'
    });
  }
});

module.exports = router;