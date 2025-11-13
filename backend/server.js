const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Test route
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    message: 'Server is running!',
    timestamp: new Date().toISOString()
  });
});

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/legal_judgment_system')
.then(() => console.log('✅ Connected to MongoDB'))
.catch((err) => console.error('❌ MongoDB connection error:', err));

// Routes - Add them one by one to identify issues
try {
  app.use('/api/auth', require('./routes/auth'));
  console.log('✅ Auth routes loaded');
} catch (error) {
  console.error('❌ Error loading auth routes:', error.message);
}

try {
  app.use('/api/cases', require('./routes/cases'));
  console.log('✅ Cases routes loaded');
} catch (error) {
  console.error('❌ Error loading cases routes:', error.message);
}

try {
  app.use('/api/judgments', require('./routes/judgments'));
  console.log('✅ Judgments routes loaded');
} catch (error) {
  console.error('❌ Error loading judgments routes:', error.message);
}

try {
  app.use('/api/documents', require('./routes/documents'));
  console.log('✅ Documents routes loaded');
} catch (error) {
  console.error('❌ Error loading documents routes:', error.message);
}

try {
  app.use('/api/users', require('./routes/users'));
  console.log('✅ Users routes loaded');
} catch (error) {
  console.error('❌ Error loading users routes:', error.message);
}

try {
  app.use('/api/courts', require('./routes/courts'));
  console.log('✅ Courts routes loaded');
} catch (error) {
  console.error('❌ Error loading courts routes:', error.message);
}

try {
  app.use('/api/analytics', require('./routes/analytics'));
  console.log('✅ Analytics routes loaded');
} catch (error) {
  console.error('❌ Error loading analytics routes:', error.message);
}

try {
  app.use('/api/search', require('./routes/search'));
  console.log('✅ Search routes loaded');
} catch (error) {
  console.error('❌ Error loading search routes:', error.message);
}

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    message: err.message || 'خطأ في الخادم الداخلي'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ message: 'المسار المطلوب غير موجود' });
});

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📱 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 Health check: http://localhost:${PORT}/api/health`);
});

module.exports = app;