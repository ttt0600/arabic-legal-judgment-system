const mongoose = require('mongoose');

const courtSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'اسم المحكمة مطلوب'],
    trim: true
  },
  nameEn: {
    type: String,
    trim: true
  },
  type: {
    type: String,
    required: [true, 'نوع المحكمة مطلوب'],
    enum: [
      'supreme_court',      // المحكمة العليا
      'appeal_court',       // محكمة الاستئناف
      'general_court',      // المحكمة العامة
      'criminal_court',     // المحكمة الجزائية
      'commercial_court',   // المحكمة التجارية
      'labor_court',        // محكمة العمل
      'administrative_court', // المحكمة الإدارية
      'family_court',       // محكمة الأحوال الشخصية
      'execution_court',    // محكمة التنفيذ
      'specialized_court'   // المحكمة المتخصصة
    ]
  },
  level: {
    type: Number,
    required: true,
    min: 1,
    max: 4
  },
  jurisdiction: {
    type: String,
    required: [true, 'الاختصاص مطلوب'],
    enum: [
      'civil',           // مدني
      'criminal',        // جزائي
      'commercial',      // تجاري
      'administrative',  // إداري
      'labor',          // عمالي
      'family',         // أحوال شخصية
      'execution',      // تنفيذ
      'mixed'           // مختلط
    ]
  },
  location: {
    city: {
      type: String,
      required: [true, 'المدينة مطلوبة']
    },
    region: {
      type: String,
      required: [true, 'المنطقة مطلوبة']
    },
    district: String,
    address: String,
    coordinates: {
      latitude: Number,
      longitude: Number
    }
  },
  contact: {
    phone: {
      type: String,
      match: [/^\+?[\d\s-()]+$/, 'رقم الهاتف غير صحيح']
    },
    fax: String,
    email: {
      type: String,
      match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'البريد الإلكتروني غير صحيح']
    },
    website: String
  },
  workingHours: {
    sunday: { start: String, end: String, isWorkingDay: Boolean },
    monday: { start: String, end: String, isWorkingDay: Boolean },
    tuesday: { start: String, end: String, isWorkingDay: Boolean },
    wednesday: { start: String, end: String, isWorkingDay: Boolean },
    thursday: { start: String, end: String, isWorkingDay: Boolean },
    friday: { start: String, end: String, isWorkingDay: Boolean },
    saturday: { start: String, end: String, isWorkingDay: Boolean }
  },
  establishedDate: Date,
  status: {
    type: String,
    enum: ['active', 'inactive', 'suspended'],
    default: 'active'
  },
  parentCourt: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Court'
  },
  settings: {
    caseNumberFormat: {
      type: String,
      default: 'YYYY/MM/####'
    },
    judgmentNumberFormat: {
      type: String,
      default: 'YYYY/####'
    },
    defaultLanguage: {
      type: String,
      enum: ['ar', 'en'],
      default: 'ar'
    },
    timezone: {
      type: String,
      default: 'Asia/Riyadh'
    }
  },
  statistics: {
    totalCases: { type: Number, default: 0 },
    activeCases: { type: Number, default: 0 },
    closedCases: { type: Number, default: 0 },
    totalJudgments: { type: Number, default: 0 },
    averageProcessingTime: { type: Number, default: 0 } // in days
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
courtSchema.index({ type: 1, jurisdiction: 1 });
courtSchema.index({ 'location.city': 1, 'location.region': 1 });
courtSchema.index({ status: 1 });
courtSchema.index({ level: 1 });

// Virtual for full name
courtSchema.virtual('fullName').get(function() {
  return `${this.name} - ${this.location.city}`;
});

// Virtual for sub courts
courtSchema.virtual('subCourts', {
  ref: 'Court',
  localField: '_id',
  foreignField: 'parentCourt'
});

// Static methods
courtSchema.statics.getByType = function(type) {
  return this.find({ type, status: 'active' });
};

courtSchema.statics.getByJurisdiction = function(jurisdiction) {
  return this.find({ jurisdiction, status: 'active' });
};

courtSchema.statics.getByLocation = function(city, region) {
  const filter = { status: 'active' };
  if (city) filter['location.city'] = city;
  if (region) filter['location.region'] = region;
  return this.find(filter);
};

// Instance methods
courtSchema.methods.updateStatistics = function() {
  // This would typically be called periodically to update court statistics
  // Implementation would query related collections to calculate statistics
};

courtSchema.methods.generateCaseNumber = function() {
  const format = this.settings.caseNumberFormat;
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  
  // This is a simplified version - in production, you'd query for the next sequence number
  const sequence = String(this.statistics.totalCases + 1).padStart(4, '0');
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('####', sequence);
};

courtSchema.methods.generateJudgmentNumber = function() {
  const format = this.settings.judgmentNumberFormat;
  const now = new Date();
  const year = now.getFullYear();
  
  // This is a simplified version - in production, you'd query for the next sequence number
  const sequence = String(this.statistics.totalJudgments + 1).padStart(4, '0');
  
  return format
    .replace('YYYY', year)
    .replace('####', sequence);
};

module.exports = mongoose.model('Court', courtSchema);