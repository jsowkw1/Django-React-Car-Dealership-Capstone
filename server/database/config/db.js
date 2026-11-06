const mongoose = require('mongoose');

let memoryServer = null;

/**
 * Connects Mongoose to MongoDB.
 * Uses MONGODB_URI when provided (e.g. MongoDB Atlas or a local mongod);
 * otherwise starts an embedded MongoDB (mongodb-memory-server) so the API
 * runs with zero external setup. Set MONGO_DATA_DIR to persist embedded data.
 */
async function connectDatabase(uri = process.env.MONGODB_URI) {
  if (!uri) {
    const { MongoMemoryServer } = require('mongodb-memory-server');
    const instance = { dbName: 'dealershipsDB' };
    // Keeps the embedded server small enough for 512 MB free-tier containers.
    if (process.env.MONGO_CACHE_GB) instance.args = ['--wiredTigerCacheSizeGB', process.env.MONGO_CACHE_GB];
    if (process.env.MONGO_DATA_DIR) {
      instance.dbPath = process.env.MONGO_DATA_DIR;
      instance.storageEngine = 'wiredTiger';
    }
    memoryServer = await MongoMemoryServer.create({ instance });
    uri = memoryServer.getUri();
    console.log(`[db] Embedded MongoDB started at ${uri}`);
  }
  await mongoose.connect(uri, { dbName: process.env.MONGODB_DB || 'dealershipsDB' });
  console.log('[db] Connected to MongoDB');
  return mongoose.connection;
}

async function disconnectDatabase() {
  await mongoose.disconnect();
  if (memoryServer) {
    await memoryServer.stop();
    memoryServer = null;
  }
}

module.exports = { connectDatabase, disconnectDatabase };
