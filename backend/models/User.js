const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'الاسم مطلوب'],
    trim: true,
    maxLength: [100, 'الاسم لا يمكن أن يتجاوز 100 حرف']
  },
  email: {
    type: String,
    required: [true, 'البريد الإلكتروني مطلوب'],
    unique: true,
    lowercase: true,
    match: [/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, 'البريد الإلكتروني غير صحيح']
  },
  password: {
    type: String,
    required: [true, 'كلمة المرور مطلوبة'],
    minLength: [6, 'كلمة المرور يجب أن تكون 6 أحرف على الأقل'],
    select: false
  },
  role: {
    type: String,
    enum: ['admin', 'judge', 'clerk', 'lawyer', 'user'],
    default: 'user'
  },
  permissions: [{
    type: String,
    enum: [
      'create_case',
      'edit_case',
      'delete_case',
      'view_case',
      'create_judgment',
      'edit_judgment',
      'delete_judgment',
      'view_judgment',
      'manage_users',
      'view_analytics',
      'manage_courts',
      'export_data'
    ]
  }],
  court: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Court'
  },
  profile: {
    avatar: String,
    phone: {
      type: String,
      match: [/^\+?[\d\s-()]+$/, 'رقم الهاتف غير صحيح']
    },
    address: String,
    department: String,
    position: String,
    licenseNumber: String, // For lawyers
    specialization: [String]
  },
  preferences: {
    language: {
      type: String,
      enum: ['ar', 'en'],
      default: 'ar'
    },
    dateFormat: {
      type: String,
      enum: ['hijri', 'gregorian'],
      default: 'hijri'
    },
    notifications: {
      email: { type: Boolean, default: true },
      inApp: { type: Boolean, default: true }
    },
    theme: {
      type: String,
      enum: ['light', 'dark', 'auto'],
      default: 'light'
    }
  },
  lastLogin: Date,
  loginAttempts: { type: Number, default: 0 },
  lockUntil: Date,
  isActive: { type: Boolean, default: true },
  emailVerified: { type: Boolean, default: false },
  resetPasswordToken: String,
  resetPasswordExpire: Date
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});

// Indexes
userSchema.index({ email: 1 });
userSchema.index({ role: 1 });
userSchema.index({ court: 1 });
userSchema.index({ 'profile.licenseNumber': 1 });

// Virtual for account lock status
userSchema.virtual('isLocked').get(function() {
  return !!(this.lockUntil && this.lockUntil > Date.now());
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  const salt = await bcrypt.genSalt(12);
  this.password = await bcrypt.hash(this.password, salt);
  next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return await bcrypt.compare(candidatePassword, this.password);
};

// Increment login attempts
userSchema.methods.incLoginAttempts = function() {
  // If we have a previous lock that has expired, restart at 1
  if (this.lockUntil && this.lockUntil < Date.now()) {
    return this.updateOne({
      $unset: { lockUntil: 1 },
      $set: { loginAttempts: 1 }
    });
  }
  
  const updates = { $inc: { loginAttempts: 1 } };
  
  // Lock account after 5 failed attempts for 2 hours
  if (this.loginAttempts + 1 >= 5 && !this.isLocked) {
    updates.$set = { lockUntil: Date.now() + 2 * 60 * 60 * 1000 };
  }
  
  return this.updateOne(updates);
};

// Reset login attempts
userSchema.methods.resetLoginAttempts = function() {
  return this.updateOne({
    $unset: { loginAttempts: 1, lockUntil: 1 }
  });
};

// Get user permissions based on role
userSchema.methods.getEffectivePermissions = function() {
  const rolePermissions = {
    admin: [
      'create_case', 'edit_case', 'delete_case', 'view_case',
      'create_judgment', 'edit_judgment', 'delete_judgment', 'view_judgment',
      'manage_users', 'view_analytics', 'manage_courts', 'export_data'
    ],
    judge: [
      'create_case', 'edit_case', 'view_case',
      'create_judgment', 'edit_judgment', 'view_judgment',
      'view_analytics', 'export_data'
    ],
    clerk: [
      'create_case', 'edit_case', 'view_case',
      'view_judgment', 'export_data'
    ],
    lawyer: [
      'view_case', 'view_judgment'
    ],
    user: [
      'view_case', 'view_judgment'
    ]
  };
  
  return [...new Set([...rolePermissions[this.role] || [], ...this.permissions])];
};

module.exports = mongoose.model('User', userSchema);