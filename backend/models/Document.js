const mongoose = require('mongoose');

const documentSchema = new mongoose.Schema({
  title: {
    type: String,
    required: [true, 'عنوان الوثيقة مطلوب'],
    trim: true,
    maxLength: [200, 'عنوان الوثيقة لا يمكن أن يتجاوز 200 حرف']
  },
  description: {
    type: String,
    maxLength: [500, 'وصف الوثيقة لا يمكن أن يتجاوز 500 حرف']
  },
  type: {
    type: String,
    required: [true, 'نوع الوثيقة مطلوب'],
    enum: [
      'petition',         // صحيفة دعوى
      'response',         // رد على الدعوى
      'evidence',         // أدلة
      'contract',         // عقد
      'certificate',      // شهادة
      'expert_report',    // تقرير خبير
      'witness_testimony', // شهادة شاهد
      'correspondence',   // مراسلات
      'court_order',      // أمر محكمة
      'judgment',         // حكم
      'appeal',          // استئناف
      'execution_order',  // أمر تنفيذ
      'other'            // أخرى
    ]
  },
  category: {
    type: String,
    required: [true, 'فئة الوثيقة مطلوبة']
  },
  subcategory: String,
  case: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Case'
  },
  judgment: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Judgment'
  },
  file: {
    filename: {
      type: String,
      required: [true, 'اسم الملف مطلوب']
    },
    originalName: String,
    path: {
      type: String,
      required: [true, 'مسار الملف مطلوب']
    },
    size: {
      type: Number,
      required: [true, 'حجم الملف مطلوب']
    },
    mimeType: {
      type: String,
      required: [true, 'نوع الملف مطلوب']
    },
    extension: String,
    checksum: String, // للتحقق من سلامة الملف
    pages: Number     // عدد الصفحات للملفات النصية
  },
  content: {
    text: String,           // النص المستخرج من الملف
    summary: String,        // ملخص المحتوى
    keywords: [String],     // الكلمات المفتاحية المستخرجة
    entities: [{           // الكيانات المستخرجة (أسماء، تواريخ، مبالغ)
      type: String,        // person, organization, location, date, amount
      value: String,
      confidence: Number
    }],
    language: {
      type: String,
      enum: ['ar', 'en', 'mixed'],
      default: 'ar'
    }
  },
  metadata: {
    author: String,
    creator: String,
    subject: String,
    creationDate: Date,
    modificationDate: Date,
    application: String,    // التطبيق المستخدم لإنشاء الملف
    producer: String,
    version: String
  },
  access: {
    confidentialityLevel: {
      type: String,
      enum: ['public', 'internal', 'confidential', 'restricted'],
      default: 'internal'
    },
    permissions: [{
      user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      role: String,
      actions: [String]      // view, download, edit, delete
    }],
    viewHistory: [{
      user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
      },
      viewDate: Date,
      ipAddress: String,
      duration: Number       // مدة العرض بالثواني
    }]
  },
  processing: {
    status: {
      type: String,
      enum: ['uploaded', 'processing', 'processed', 'failed'],
      default: 'uploaded'
    },
    ocrPerformed: { type: Boolean, default: false },
    textExtracted: { type: Boolean, default: false },
    indexed: { type: Boolean, default: false },
    virus_scanned: { type: Boolean, default: false },
    processingLog: [{
      step: String,
      status: String,
      timestamp: Date,
      error: String
    }]
  },
  versions: [{
    version: Number,
    filename: String,
    path: String,
    size: Number,
    uploadDate: Date,
    uploadedBy: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    changes: String,
    active: { type: Boolean, default: false }
  }],
  signatures: [{
    signer: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    signDate: Date,
    signatureType: {
      type: String,
      enum: ['digital', 'electronic', 'handwritten_scan']
    },
    certificate: String,
    valid: { type: Boolean, default: true }
  }],
  tags: [String],
  notes: [{
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User'
    },
    note: String,
    date: { type: Date, default: Date.now },
    type: {
      type: String,
      enum: ['comment', 'revision', 'approval', 'rejection']
    }
  }],
  relatedDocuments: [{
    document: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'Document'
    },
    relationship: {
      type: String,
      enum: ['attachment', 'reference', 'version', 'translation']
    }
  }],
  dates: {
    uploaded: { type: Date, default: Date.now },
    lastViewed: Date,
    lastModified: Date,
    expiryDate: Date,
    archiveDate: Date
  },
  status: {
    type: String,
    enum: ['active', 'archived', 'deleted', 'expired'],
    default: 'active'
  },
  uploadedBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: [true, 'رافع الملف مطلوب']
  },
  court: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Court'
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
documentSchema.index({ case: 1, type: 1 });
documentSchema.index({ judgment: 1 });
documentSchema.index({ uploadedBy: 1 });
documentSchema.index({ court: 1 });
documentSchema.index({ type: 1, category: 1 });
documentSchema.index({ 'dates.uploaded': -1 });
documentSchema.index({ status: 1 });
documentSchema.index({ tags: 1 });

// Full text search index
documentSchema.index({
  title: 'text',
  description: 'text',
  'content.text': 'text',
  'content.summary': 'text',
  'content.keywords': 'text'
});

// Compound indexes
documentSchema.index({ case: 1, type: 1, status: 1 });
documentSchema.index({ uploadedBy: 1, 'dates.uploaded': -1 });

// Virtuals
documentSchema.virtual('fileSize').get(function() {
  const size = this.file.size;
  if (size < 1024) return size + ' B';
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB';
  if (size < 1024 * 1024 * 1024) return (size / (1024 * 1024)).toFixed(1) + ' MB';
  return (size / (1024 * 1024 * 1024)).toFixed(1) + ' GB';
});

documentSchema.virtual('isExpired').get(function() {
  return this.dates.expiryDate && this.dates.expiryDate < new Date();
});

documentSchema.virtual('canDownload').get(function() {
  return this.status === 'active' && !this.isExpired;
});

documentSchema.virtual('currentVersion').get(function() {
  return this.versions.find(v => v.active) || null;
});

// Static methods
documentSchema.statics.getByType = function(type) {
  return this.find({ type, status: 'active' }).populate('case uploadedBy');
};

documentSchema.statics.getByCase = function(caseId) {
  return this.find({ case: caseId, status: 'active' })
    .sort({ 'dates.uploaded': -1 })
    .populate('uploadedBy');
};

documentSchema.statics.getByUploader = function(userId) {
  return this.find({ uploadedBy: userId })
    .sort({ 'dates.uploaded': -1 })
    .populate('case');
};

documentSchema.statics.searchDocuments = function(searchTerm, options = {}) {
  const query = {
    $and: [
      { status: 'active' },
      {
        $text: { $search: searchTerm }
      }
    ]
  };
  
  if (options.type) query.$and.push({ type: options.type });
  if (options.case) query.$and.push({ case: options.case });
  if (options.court) query.$and.push({ court: options.court });
  if (options.uploadedBy) query.$and.push({ uploadedBy: options.uploadedBy });
  
  return this.find(query, { score: { $meta: 'textScore' } })
    .sort({ score: { $meta: 'textScore' } })
    .populate('case uploadedBy');
};

// Instance methods
documentSchema.methods.addVersion = function(fileData, userId, changes) {
  // Deactivate current version
  this.versions.forEach(v => v.active = false);
  
  // Add new version
  this.versions.push({
    version: this.versions.length + 1,
    filename: fileData.filename,
    path: fileData.path,
    size: fileData.size,
    uploadDate: new Date(),
    uploadedBy: userId,
    changes,
    active: true
  });
  
  // Update main file info
  this.file = fileData;
  this.dates.lastModified = new Date();
  
  return this.save();
};

documentSchema.methods.addNote = function(userId, note, type = 'comment') {
  this.notes.push({
    user: userId,
    note,
    type
  });
  return this.save();
};

documentSchema.methods.addSignature = function(signatureData) {
  this.signatures.push(signatureData);
  return this.save();
};

documentSchema.methods.logView = function(userId, ipAddress, duration = null) {
  this.access.viewHistory.push({
    user: userId,
    viewDate: new Date(),
    ipAddress,
    duration
  });
  this.dates.lastViewed = new Date();
  return this.save();
};

documentSchema.methods.canBeAccessedBy = function(user) {
  // Admin can access all documents
  if (user.role === 'admin') return true;
  
  // Owner can access their documents
  if (this.uploadedBy.toString() === user._id.toString()) return true;
  
  // Check specific permissions
  const permission = this.access.permissions.find(p => 
    p.user.toString() === user._id.toString()
  );
  if (permission && permission.actions.includes('view')) return true;
  
  // Check case access
  if (this.case) {
    // Users involved in the case can view its documents
    return true; // This would need more complex logic based on case parties
  }
  
  // Public documents
  if (this.access.confidentialityLevel === 'public') return true;
  
  return false;
};

documentSchema.methods.extractText = async function() {
  // This would integrate with OCR services or PDF parsers
  // For now, it's a placeholder
  if (this.file.mimeType === 'application/pdf') {
    // Use PDF parser
    this.processing.status = 'processing';
    await this.save();
    
    try {
      // PDF text extraction logic would go here
      this.processing.textExtracted = true;
      this.processing.status = 'processed';
    } catch (error) {
      this.processing.status = 'failed';
      this.processing.processingLog.push({
        step: 'text_extraction',
        status: 'failed',
        timestamp: new Date(),
        error: error.message
      });
    }
    
    await this.save();
  }
};

// Pre-save middleware
documentSchema.pre('save', function(next) {
  // Set file extension if not set
  if (!this.file.extension && this.file.filename) {
    const ext = this.file.filename.split('.').pop();
    this.file.extension = ext;
  }
  
  // Update modification date
  if (this.isModified() && !this.isNew) {
    this.dates.lastModified = new Date();
  }
  
  next();
});

// Post-save middleware
documentSchema.post('save', function() {
  // Trigger text extraction for new documents
  if (this.processing.status === 'uploaded' && !this.processing.textExtracted) {
    this.extractText().catch(console.error);
  }
});

module.exports = mongoose.model('Document', documentSchema);