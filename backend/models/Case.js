const mongoose = require('mongoose');

const caseSchema = new mongoose.Schema({
  caseNumber: {
    type: String,
    required: [true, 'رقم القضية مطلوب'],
    unique: true,
    trim: true
  },
  title: {
    type: String,
    required: [true, 'عنوان القضية مطلوب'],
    trim: true,
    maxLength: [200, 'عنوان القضية لا يمكن أن يتجاوز 200 حرف']
  },
  description: {
    type: String,
    required: [true, 'وصف القضية مطلوب'],
    maxLength: [2000, 'وصف القضية لا يمكن أن يتجاوز 2000 حرف']
  },
  type: {
    type: String,
    required: [true, 'نوع القضية مطلوب'],
    enum: [
      'civil',           // مدنية
      'criminal',        // جنائية
      'commercial',      // تجارية
      'labor',          // عمالية
      'administrative',  // إدارية
      'family',         // أحوال شخصية
      'real_estate',    // عقارية
      'intellectual_property', // ملكية فكرية
      'bankruptcy',     // إفلاس
      'tax',           // ضريبية
      'constitutional', // دستورية
      'other'          // أخرى
    ]
  },
  category: {
    type: String,
    required: [true, 'فئة القضية مطلوبة']
  },
  subcategory: String,
  priority: {
    type: String,
    enum: ['low', 'normal', 'high', 'urgent'],
    default: 'normal'
  },
  status: {
    type: String,
    enum: [
      'registered',      // مسجلة
      'under_review',    // قيد المراجعة
      'scheduled',       // محددة موعد
      'in_session',      // في جلسة
      'postponed',       // مؤجلة
      'under_deliberation', // قيد المداولة
      'decided',         // صدر حكم
      'appealed',        // مستأنفة
      'final',           // نهائية
      'archived',        // مؤرشفة
      'cancelled'        // ملغية
    ],
    default: 'registered'
  },
  court: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Court',
    required: [true, 'المحكمة مطلوبة']
  },
  judge: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  clerk: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  parties: {
    plaintiffs: [{
      type: {
        type: String,
        enum: ['individual', 'organization', 'government'],
        required: true
      },
      name: {
        type: String,
        required: [true, 'اسم المدعي مطلوب']
      },
      nationalId: String,
      commercialRegistry: String,
      contact: {
        phone: String,
        email: String,
        address: String
      },
      lawyer: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      role: String, // دور الطرف في القضية
      notes: String
    }],
    defendants: [{
      type: {
        type: String,
        enum: ['individual', 'organization', 'government'],
        required: true
      },
      name: {
        type: String,
        required: [true, 'اسم المدعى عليه مطلوب']
      },
      nationalId: String,
      commercialRegistry: String,
      contact: {
        phone: String,
        email: String,
        address: String
      },
      lawyer: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      role: String,
      notes: String
    }],
    witnesses: [{
      name: {
        type: String,
        required: [true, 'اسم الشاهد مطلوب']
      },
      nationalId: String,
      contact: {
        phone: String,
        email: String,
        address: String
      },
      type: {
        type: String,
        enum: ['witness', 'expert', 'translator'],
        default: 'witness'
      },
      notes: String
    }],
    experts: [{
      name: String,
      specialization: String,
      licenseNumber: String,
      contact: {
        phone: String,
        email: String
      }
    }]
  },
  sessions: [{
    sessionNumber: Number,
    date: Date,
    time: String,
    type: {
      type: String,
      enum: ['hearing', 'deliberation', 'verdict', 'preliminary']
    },
    attendees: [String],
    summary: String,
    decisions: [String],
    nextSessionDate: Date,
    status: {
      type: String,
      enum: ['scheduled', 'completed', 'postponed', 'cancelled']
    }
  }],
  timeline: [{
    date: { type: Date, default: Date.now },
    event: String,
    description: String,
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    }
  }],
  amounts: {
    claimed: {
      amount: Number,
      currency: { type: String, default: 'SAR' }
    },
    awarded: {
      amount: Number,
      currency: { type: String, default: 'SAR' }
    },
    fees: {
      court: Number,
      lawyer: Number,
      other: Number
    }
  },
  dates: {
    filed: { type: Date, required: true },
    firstHearing: Date,
    lastSession: Date,
    decisionDate: Date,
    finalDate: Date,
    archiveDate: Date
  },
  legalBasis: {
    laws: [String],        // القوانين المطبقة
    articles: [String],    // المواد القانونية
    precedents: [String]   // السوابق القضائية
  },
  keywords: [String],
  tags: [String],
  isPublic: { type: Boolean, default: false },
  confidentialityLevel: {
    type: String,
    enum: ['public', 'restricted', 'confidential', 'top_secret'],
    default: 'restricted'
  },
  relatedCases: [{
    case: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Case'
    },
    relationship: {
      type: String,
      enum: ['appeal', 'related', 'precedent', 'consolidated']
    }
  }],
  metadata: {
    language: { type: String, default: 'ar' },
    version: { type: Number, default: 1 },
    lastModifiedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    archivalInfo: {
      reason: String,
      date: Date,
      location: String
    }
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
caseSchema.index({ caseNumber: 1 }, { unique: true });
caseSchema.index({ court: 1, status: 1 });
caseSchema.index({ type: 1, category: 1 });
caseSchema.index({ judge: 1 });
caseSchema.index({ 'dates.filed': 1 });
caseSchema.index({ status: 1, priority: 1 });
caseSchema.index({ keywords: 1 });
caseSchema.index({ 'parties.plaintiffs.name': 'text', 'parties.defendants.name': 'text', title: 'text' });

// Virtuals
caseSchema.virtual('documents', {
  ref: 'Document',
  localField: '_id',
  foreignField: 'case'
});

caseSchema.virtual('judgments', {
  ref: 'Judgment',
  localField: '_id',
  foreignField: 'case'
});

caseSchema.virtual('duration').get(function() {
  if (!this.dates.filed) return null;
  
  const endDate = this.dates.finalDate || this.dates.decisionDate || new Date();
  const startDate = this.dates.filed;
  
  return Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24));
});

caseSchema.virtual('isActive').get(function() {
  return !['decided', 'final', 'archived', 'cancelled'].includes(this.status);
});

// Static methods
caseSchema.statics.getByStatus = function(status) {
  return this.find({ status }).populate('court judge clerk');
};

caseSchema.statics.getByType = function(type) {
  return this.find({ type }).populate('court judge');
};

caseSchema.statics.getByDateRange = function(startDate, endDate) {
  return this.find({
    'dates.filed': {
      $gte: startDate,
      $lte: endDate
    }
  });
};

caseSchema.statics.searchCases = function(searchTerm) {
  return this.find({
    $or: [
      { title: { $regex: searchTerm, $options: 'i' } },
      { caseNumber: { $regex: searchTerm, $options: 'i' } },
      { description: { $regex: searchTerm, $options: 'i' } },
      { 'parties.plaintiffs.name': { $regex: searchTerm, $options: 'i' } },
      { 'parties.defendants.name': { $regex: searchTerm, $options: 'i' } }
    ]
  });
};

// Instance methods
caseSchema.methods.addTimelineEvent = function(event, description, userId) {
  this.timeline.push({
    event,
    description,
    user: userId
  });
  return this.save();
};

caseSchema.methods.addSession = function(sessionData) {
  const sessionNumber = this.sessions.length + 1;
  this.sessions.push({
    sessionNumber,
    ...sessionData
  });
  return this.save();
};

caseSchema.methods.updateStatus = function(newStatus, userId) {
  const oldStatus = this.status;
  this.status = newStatus;
  this.metadata.lastModifiedBy = userId;
  
  // Add timeline event
  this.addTimelineEvent(
    'status_change',
    `تم تغيير حالة القضية من ${oldStatus} إلى ${newStatus}`,
    userId
  );
  
  return this.save();
};

caseSchema.methods.canBeEditedBy = function(user) {
  if (user.role === 'admin') return true;
  if (user.role === 'judge' && this.judge && this.judge.toString() === user._id.toString()) return true;
  if (user.role === 'clerk' && this.clerk && this.clerk.toString() === user._id.toString()) return true;
  return false;
};

module.exports = mongoose.model('Case', caseSchema);