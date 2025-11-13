const mongoose = require('mongoose');
const Court = require('../models/Court');
require('dotenv').config();

const sampleCourts = [
  {
    name: "المحكمة العليا",
    nameEn: "Supreme Court",
    type: "supreme_court",
    level: 1,
    jurisdiction: "mixed",
    location: {
      city: "الرياض",
      region: "الرياض",
      address: "طريق الملك فهد، الرياض"
    },
    contact: {
      phone: "+966114012345",
      email: "info@supremecourt.gov.sa"
    },
    status: "active"
  },
  {
    name: "محكمة الاستئناف بالرياض",
    nameEn: "Riyadh Court of Appeal",
    type: "appeal_court",
    level: 2,
    jurisdiction: "mixed",
    location: {
      city: "الرياض",
      region: "الرياض"
    },
    status: "active"
  },
  {
    name: "المحكمة العامة بالرياض",
    nameEn: "Riyadh General Court",
    type: "general_court",
    level: 3,
    jurisdiction: "civil",
    location: {
      city: "الرياض",
      region: "الرياض"
    },
    status: "active"
  },
  {
    name: "المحكمة التجارية بالرياض",
    nameEn: "Riyadh Commercial Court",
    type: "commercial_court",
    level: 3,
    jurisdiction: "commercial",
    location: {
      city: "الرياض",
      region: "الرياض"
    },
    status: "active"
  },
  {
    name: "محكمة الأحوال الشخصية بالرياض",
    nameEn: "Riyadh Family Court",
    type: "family_court",
    level: 3,
    jurisdiction: "family",
    location: {
      city: "الرياض",
      region: "الرياض"
    },
    status: "active"
  }
];

async function seedCourts() {
  try {
    console.log('Connecting to MongoDB...');
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('Connected to MongoDB');
    
    console.log('Clearing existing courts...');
    await Court.deleteMany({});
    
    console.log('Creating sample courts...');
    for (const courtData of sampleCourts) {
      const court = new Court(courtData);
      await court.save();
      console.log(`✅ Created court: ${court.name}`);
    }
    
    console.log(`🎉 Successfully created ${sampleCourts.length} courts`);
    console.log('You can now create cases and assign them to these courts');
    
  } catch (error) {
    console.error('❌ Error seeding courts:', error);
  } finally {
    mongoose.disconnect();
  }
}

seedCourts();