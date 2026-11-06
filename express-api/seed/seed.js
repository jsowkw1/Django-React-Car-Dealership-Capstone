const Dealership = require('../models/Dealership');
const Review = require('../models/Review');
const { analyzeText } = require('../services/sentiment');
const dealerships = require('./dealerships.json');
const reviews = require('./reviews.json');

/** Replaces all dealers and reviews with the demonstration data set. */
async function seedDatabase() {
  await Dealership.deleteMany({});
  await Review.deleteMany({});
  await Dealership.insertMany(dealerships);
  await Review.insertMany(reviews.map((r) => ({ ...r, sentiment: analyzeText(r.review).sentiment })));
  return { dealerships: dealerships.length, reviews: reviews.length };
}

/** Seeds only when the dealers collection is empty (used on server start). */
async function seedIfEmpty() {
  if ((await Dealership.estimatedDocumentCount()) > 0) return null;
  return seedDatabase();
}

module.exports = { seedDatabase, seedIfEmpty };

if (require.main === module) {
  require('dotenv').config({ quiet: true });
  const { connectDatabase, disconnectDatabase } = require('../config/db');
  (async () => {
    await connectDatabase();
    const counts = await seedDatabase();
    console.log(`[seed] Inserted ${counts.dealerships} dealerships and ${counts.reviews} reviews`);
    await disconnectDatabase();
  })().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
