const mongoose = require('mongoose');

const judgmentSchema = new mongoose.Schema({
  judgmentNumber: {
    type: String,
    required: [true, 'رقم الحكم مطلوب'],
    unique: true,
    trim: true
  },
  case: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Case',
    required: [true, 'القضية مطلوبة']
  },
  court: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Court',
    required: [true, 'المحكمة مطلوبة']
  },
  judge: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'القاضي مطلوب']
  },
  panel: [{
    judge: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    role: {
      type: String,
      enum: ['presiding', 'member'],
      default: 'member'
    }
  }],
  type: {
    type: String,
    required: [true, 'نوع الحكم مطلوب'],
    enum: [
      'final',           // نهائي
      'preliminary',     // تمهيدي
      'interlocutory',   // تحضيري
      'default',         // غيابي
      'summary',         // مستعجل
      'appeal',          // استئناف
      'cassation'        // نقض
    ]
  },
  decision: {
    type: String,
    required: [true, 'نوع القرار مطلوب'],
    enum: [
      'accept',          // قبول
      'reject',          // رفض
      'partial_accept',  // قبول جزئي
      'dismiss',         // رد الدعوى
      'no_jurisdiction', // عدم اختصاص
      'settlement',      // صلح
      'withdrawal',      // تنازل
      'postpone',        // تأجيل
      'refer'           // إحالة
    ]
  },
  summary: {
    type: String,
    required: [true, 'ملخص الحكم مطلوب'],
    maxLength: [500, 'ملخص الحكم لا يمكن أن يتجاوز 500 حرف']
  },
  content: {
    introduction: {
      type: String,
      required: [true, 'مقدمة الحكم مطلوبة']
    },
    facts: {
      type: String,
      required: [true, 'وقائع القضية مطلوبة']
    },
    legalAnalysis: {
      type: String,
      required: [true, 'التحليل القانوني مطلوب']
    },
    reasoning: {
      type: String,
      required: [true, 'أسباب الحكم مطلوبة']
    },
    verdict: {
      type: String,
      required: [true, 'منطوق الحكم مطلوب']
    },
    orders: [String], // الأمر بالتنفيذ والتوجيهات
    costs: {
      courtFees: Number,
      lawyerFees: Number,
      otherCosts: Number,
      responsibleParty: String
    }
  },
  legalBasis: {
    laws: [{
      name: String,
      articles: [String]
    }],
    precedents: [{
      caseNumber: String,
      court: String,
      date: Date,
      principle: String
    }],
    doctrines: [{
      author: String,
      reference: String,
      page: String
    }]
  },
  dates: {
    sessionDate: Date,
    issuedDate: {
      type: Date,
      required: [true, 'تاريخ إصدار الحكم مطلوب']
    },
    notificationDate: Date,
    effectiveDate: Date,
    appealDeadline: Date
  },
  parties: {
    inFavor: [{
      name: String,
      type: String, // plaintiff, defendant, third_party
      awards: [{
        type: String, // monetary, property, action
        description: String,
        amount: Number,
        currency: String
      }]
    }],
    against: [{
      name: String,
      type: String,
      obligations: [{
        type: String,
        description: String,
        amount: Number,
        currency: String,
        deadline: Date
      }]
    }]
  },
  appeals: [{
    appealNumber: String,
    appellant: String,
    court: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Court'
    },
    filedDate: Date,
    status: {
      type: String,
      enum: ['pending', 'accepted', 'rejected', 'withdrawn']
    },
    decision: String,
    decisionDate: Date
  }],
  execution: {
    status: {
      type: String,
      enum: ['pending', 'in_progress', 'completed', 'suspended'],
      default: 'pending'
    },
    executionCourt: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Court'
    },
    startDate: Date,
    completionDate: Date,
    obstacles: [String],
    notes: String
  },
  publication: {
    isPublished: { type: Boolean, default: false },
    publishedDate: Date,
    publicationMedium: [String], // website, official_gazette, legal_journal
    anonymized: { type: Boolean, default: true }
  },
  classification: {
    subject: [String],
    keywords: [String],
    legalPrinciples: [String],
    importance: {
      type: String,
      enum: ['low', 'medium', 'high', 'landmark'],
      default: 'medium'
    }
  },
  attachments: [{
    type: String,
    filename: String,
    path: String,
    size: Number,
    uploadDate: Date
  }],
  signatures: [{
    judge: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    signedDate: Date,
    digitalSignature: String,
    role: String
  }],
  status: {
    type: String,
    enum: [
      'draft',           // مسودة
      'under_review',    // قيد المراجعة
      'signed',          // موقع
      'issued',          // صادر
      'notified',        // مبلغ
      'effective',       // نافذ
      'appealed',        // مستأنف
      'executed',        // منفذ
      'archived'         // مؤرشف
    ],
    default: 'draft'
  },
  language: {
    type: String,
    enum: ['ar', 'en'],
    default: 'ar'
  },
  metadata: {
    version: { type: Number, default: 1 },
    createdBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    lastModifiedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    reviewHistory: [{
      reviewer: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      reviewDate: Date,
      comments: String,
      approved: Boolean
    }],
    statistics: {
      wordCount: Number,
      pageCount: Number,
      readingTime: Number // in minutes
    }
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
judgmentSchema.index({ judgmentNumber: 1 }, { unique: true });
judgmentSchema.index({ case: 1 });
judgmentSchema.index({ court: 1, 'dates.issuedDate': -1 });
judgmentSchema.index({ judge: 1 });
judgmentSchema.index({ type: 1, decision: 1 });
judgmentSchema.index({ 'dates.issuedDate': -1 });
judgmentSchema.index({ status: 1 });
judgmentSchema.index({ 'classification.keywords': 1 });
judgmentSchema.index({ 'publication.isPublished': 1 });

// Full text search index
judgmentSchema.index({
  summary: 'text',
  'content.facts': 'text',
  'content.reasoning': 'text',
  'classification.keywords': 'text'
});

// Virtuals
judgmentSchema.virtual('isAppealable').get(function() {
  if (!this.dates.appealDeadline) return false;
  return new Date() <= this.dates.appealDeadline;
});

judgmentSchema.virtual('isExecutable').get(function() {
  return this.status === 'effective' && !this.isAppealable;
});

judgmentSchema.virtual('daysSinceIssued').get(function() {
  if (!this.dates.issuedDate) return null;
  return Math.ceil((new Date() - this.dates.issuedDate) / (1000 * 60 * 60 * 24));
});

// Static methods
judgmentSchema.statics.getByType = function(type) {
  return this.find({ type }).populate('case court judge');
};

judgmentSchema.statics.getByDecision = function(decision) {
  return this.find({ decision }).populate('case court');
};

judgmentSchema.statics.getByDateRange = function(startDate, endDate) {
  return this.find({
    'dates.issuedDate': {
      $gte: startDate,
      $lte: endDate
    }
  });
};

judgmentSchema.statics.getByJudge = function(judgeId) {
  return this.find({ judge: judgeId }).populate('case court');
};

judgmentSchema.statics.getPublished = function() {
  return this.find({ 'publication.isPublished': true });
};

judgmentSchema.statics.searchJudgments = function(searchTerm, options = {}) {
  const query = {
    $and: [
      {
        $text: { $search: searchTerm }
      }
    ]
  };
  
  if (options.court) query.$and.push({ court: options.court });
  if (options.type) query.$and.push({ type: options.type });
  if (options.decision) query.$and.push({ decision: options.decision });
  if (options.dateFrom || options.dateTo) {
    const dateFilter = {};
    if (options.dateFrom) dateFilter.$gte = options.dateFrom;
    if (options.dateTo) dateFilter.$lte = options.dateTo;
    query.$and.push({ 'dates.issuedDate': dateFilter });
  }
  
  return this.find(query, { score: { $meta: 'textScore' } })
    .sort({ score: { $meta: 'textScore' } });
};

// Instance methods
judgmentSchema.methods.calculateStatistics = function() {
  const content = [
    this.content.introduction,
    this.content.facts,
    this.content.legalAnalysis,
    this.content.reasoning,
    this.content.verdict
  ].join(' ');
  
  this.metadata.statistics.wordCount = content.split(/\s+/).length;
  this.metadata.statistics.readingTime = Math.ceil(this.metadata.statistics.wordCount / 200);
  
  return this;
};

judgmentSchema.methods.addAppeal = function(appealData) {
  this.appeals.push(appealData);
  this.status = 'appealed';
  return this.save();
};

judgmentSchema.methods.addReview = function(reviewerId, comments, approved) {
  this.metadata.reviewHistory.push({
    reviewer: reviewerId,
    reviewDate: new Date(),
    comments,
    approved
  });
  return this.save();
};

judgmentSchema.methods.publish = function(medium = ['website']) {
  this.publication.isPublished = true;
  this.publication.publishedDate = new Date();
  this.publication.publicationMedium = medium;
  this.status = 'issued';
  return this.save();
};

judgmentSchema.methods.canBeEditedBy = function(user) {
  if (user.role === 'admin') return true;
  if (this.status === 'draft' || this.status === 'under_review') {
    if (user.role === 'judge' && this.judge && this.judge.toString() === user._id.toString()) return true;
    if (this.panel.some(p => p.judge.toString() === user._id.toString())) return true;
  }
  return false;
};

// Pre-save middleware
judgmentSchema.pre('save', function(next) {
  // Calculate statistics before saving
  this.calculateStatistics();
  
  // Set appeal deadline (30 days from issue date for most types)
  if (this.dates.issuedDate && !this.dates.appealDeadline) {
    const appealPeriod = this.type === 'summary' ? 15 : 30; // days
    this.dates.appealDeadline = new Date(this.dates.issuedDate.getTime() + appealPeriod * 24 * 60 * 60 * 1000);
  }
  
  next();
});

module.exports = mongoose.model('Judgment', judgmentSchema);