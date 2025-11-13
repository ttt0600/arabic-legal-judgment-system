const mongoose = require('mongoose');
const User = require('../models/User');
require('dotenv').config();

async function createAdmin() {
  try {
    console.log('Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('Connected to MongoDB');
    
    const adminExists = await User.findOne({ email: 'admin@court.gov.sa' });
    if (adminExists) {
      console.log('Admin user already exists');
      console.log('Email: admin@court.gov.sa');
      console.log('You can use the existing account');
      return;
    }

    const admin = new User({
      name: 'المدير العام',
      email: 'admin@court.gov.sa',
      password: 'Admin123!',
      role: 'admin',
      isActive: true,
      emailVerified: true
    });

    await admin.save();
    console.log('✅ Admin user created successfully');
    console.log('📧 Email: admin@court.gov.sa');
    console.log('🔑 Password: Admin123!');
    console.log('🔗 Login at: http://localhost:3000');
    
  } catch (error) {
    console.error('❌ Error creating admin:', error.message);
  } finally {
    mongoose.disconnect();
  }
}

createAdmin();