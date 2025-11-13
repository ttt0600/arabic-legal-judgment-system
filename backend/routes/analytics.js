const express = require('express');
const Case = require('../models/Case');
const Judgment = require('../models/Judgment');
const Document = require('../models/Document');
const { protect, authorize } = require('../utils/auth');

const router = express.Router();

// @route   GET /api/analytics/dashboard
// @desc    Get comprehensive dashboard analytics
// @access  Private
router.get('/dashboard', protect, authorize('view_analytics'), async (req, res) => {
  try {
    const { court, dateRange = '30' } = req.query;
    
    // Build base filter based on user role
    let baseFilter = {};
    
    if (req.user.role !== 'admin') {
      if (req.user.role === 'judge') {
        baseFilter = { judge: req.user._id };
      } else if (req.user.court) {
        baseFilter = { court: req.user.court._id };
      }
    }
    
    if (court && req.user.role === 'admin') {
      baseFilter.court = court;
    }

    // Date filter for recent data
    const dateFrom = new Date();
    dateFrom.setDate(dateFrom.getDate() - parseInt(dateRange));
    
    const recentFilter = {
      ...baseFilter,
      createdAt: { $gte: dateFrom }
    };

    // Parallel execution of analytics queries
    const [
      totalCases,
      recentCases,
      casesByStatus,
      casesByType,
      totalJudgments,
      recentJudgments,
      judgmentsByDecision,
      totalDocuments,
      recentDocuments
    ] = await Promise.all([
      Case.countDocuments(baseFilter),
      Case.countDocuments(recentFilter),
      Case.aggregate([
        { $match: baseFilter },
        { $group: { _id: '$status', count: { $sum: 1 } } }
      ]),
      Case.aggregate([
        { $match: baseFilter },
        { $group: { _id: '$type', count: { $sum: 1 } } }
      ]),
      Judgment.countDocuments(baseFilter),
      Judgment.countDocuments({
        ...baseFilter,
        'dates.issuedDate': { $gte: dateFrom }
      }),
      Judgment.aggregate([
        { $match: baseFilter },
        { $group: { _id: '$decision', count: { $sum: 1 } } }
      ]),
      Document.countDocuments({ ...baseFilter, status: 'active' }),
      Document.countDocuments({
        ...baseFilter,
        status: 'active',
        'dates.uploaded': { $gte: dateFrom }
      })
    ]);

    // Format response data
    const analytics = {
      summary: {
        totalCases,
        totalJudgments,
        totalDocuments,
        recentCases,
        recentJudgments,
        recentDocuments
      },
      cases: {
        byStatus: casesByStatus.reduce((acc, item) => {
          acc[item._id] = item.count;
          return acc;
        }, {}),
        byType: casesByType.reduce((acc, item) => {
          acc[item._id] = item.count;
          return acc;
        }, {})
      },
      judgments: {
        byDecision: judgmentsByDecision.reduce((acc, item) => {
          acc[item._id] = item.count;
          return acc;
        }, {})
      }
    };

    res.json({
      success: true,
      data: analytics
    });

  } catch (error) {
    console.error('Get analytics error:', error);
    res.status(500).json({
      success: false,
      message: 'خطأ في استرجاع التحليلات'
    });
  }
});

module.exports = router;