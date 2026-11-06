require('dotenv').config({ quiet: true });
const { createApp } = require('./app');
const { connectDatabase } = require('./config/db');
const { seedIfEmpty } = require('./seed/seed');

const PORT = Number(process.env.PORT) || 3030;

async function start() {
  await connectDatabase();
  const seeded = await seedIfEmpty();
  if (seeded) console.log(`[seed] Database was empty: inserted ${seeded.dealerships} dealerships, ${seeded.reviews} reviews`);
  createApp().listen(PORT, () => console.log(`[api] Express API listening on http://localhost:${PORT}`));
}

start().catch((err) => {
  console.error('[api] Failed to start', err);
  process.exit(1);
});
