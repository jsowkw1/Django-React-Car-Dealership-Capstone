process.env.NODE_ENV = 'test';
delete process.env.MONGODB_URI;

const { test, before, after, beforeEach } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const { createApp } = require('../app');
const { connectDatabase, disconnectDatabase } = require('../config/db');
const { seedDatabase } = require('../seed/seed');

const app = createApp();

before(async () => {
  await connectDatabase();
});
beforeEach(async () => {
  delete process.env.API_KEY;
  await seedDatabase();
});
after(async () => {
  await disconnectDatabase();
});

test('GET / returns the service index', async () => {
  const res = await request(app).get('/').expect(200);
  assert.equal(res.body.status, 'ok');
});

test('GET /fetchDealers returns all seeded dealers', async () => {
  const res = await request(app).get('/fetchDealers').expect(200);
  assert.ok(res.body.length >= 10);
  assert.equal(res.body[0].id, 1);
  assert.equal(res.body[0]._id, undefined);
});

test('GET /fetchDealers/Kansas filters by full state name', async () => {
  const res = await request(app).get('/fetchDealers/Kansas').expect(200);
  assert.ok(res.body.length >= 3);
  assert.ok(res.body.every((d) => d.state === 'Kansas'));
});

test('GET /fetchDealers/ks filters by state code, case-insensitive', async () => {
  const res = await request(app).get('/fetchDealers/ks').expect(200);
  assert.ok(res.body.length >= 3);
});

test('GET /fetchDealers/Atlantis returns an empty list', async () => {
  const res = await request(app).get('/fetchDealers/Atlantis').expect(200);
  assert.deepEqual(res.body, []);
});

test('GET /fetchDealer/:id returns one dealer, 404 and 400 on bad ids', async () => {
  const res = await request(app).get('/fetchDealer/1').expect(200);
  assert.equal(res.body.full_name, 'Sunflower State Motors');
  await request(app).get('/fetchDealer/999').expect(404);
  await request(app).get('/fetchDealer/abc').expect(400);
});

test('GET /fetchReviews/dealer/1 returns multiple reviews with sentiment', async () => {
  const res = await request(app).get('/fetchReviews/dealer/1').expect(200);
  assert.ok(res.body.length >= 3);
  assert.ok(res.body.every((r) => r.dealership === 1 && r.sentiment));
});

test('POST /insert_review creates a review (201) and it is retrievable', async () => {
  const payload = {
    name: 'Test User', dealership: 4, review: 'Excellent and friendly staff', rating: 5,
    purchase: true, purchase_date: '2026-10-01', car_make: 'Toyota', car_model: 'Camry', car_year: 2024,
  };
  const res = await request(app).post('/insert_review').send(payload).expect(201);
  assert.equal(res.body.sentiment, 'positive');
  assert.ok(res.body.id > 14);
  const list = await request(app).get('/fetchReviews/dealer/4').expect(200);
  assert.ok(list.body.some((r) => r.id === res.body.id));
});

test('POST /insert_review validates input (400) and unknown dealer (404)', async () => {
  await request(app).post('/insert_review').send({ name: '', dealership: 1, review: '', rating: 9 }).expect(400);
  await request(app).post('/insert_review').send({ name: 'A', dealership: 500, review: 'ok', rating: 3 }).expect(404);
});

test('POST /insert_review requires X-API-Key when API_KEY is set (401)', async () => {
  process.env.API_KEY = 'secret';
  const body = { name: 'A', dealership: 1, review: 'Good', rating: 4 };
  await request(app).post('/insert_review').send(body).expect(401);
  await request(app).post('/insert_review').set('X-API-Key', 'secret').send(body).expect(201);
});

test('GET /analyze/Fantastic services is positive', async () => {
  const res = await request(app).get('/analyze/Fantastic%20services').expect(200);
  assert.equal(res.body.sentiment, 'positive');
  assert.ok(res.body.positive_words.includes('fantastic'));
});

test('sentiment analyzer handles negative and neutral text', async () => {
  const neg = await request(app).post('/analyze').send({ text: 'Terrible, rude and dishonest service' }).expect(200);
  assert.equal(neg.body.sentiment, 'negative');
  const neutral = await request(app).get('/analyze/The%20car%20is%20blue').expect(200);
  assert.equal(neutral.body.sentiment, 'neutral');
  await request(app).post('/analyze').send({}).expect(400);
});

test('unknown routes return a JSON 404', async () => {
  const res = await request(app).get('/nope').expect(404);
  assert.equal(res.body.status, 404);
});
