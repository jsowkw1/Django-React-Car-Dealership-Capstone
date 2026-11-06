const { Router } = require('express');
const dealers = require('../controllers/dealerController');
const reviews = require('../controllers/reviewController');
const sentiment = require('../controllers/sentimentController');
const { requireApiKey } = require('../middleware/apiKey');

const router = Router();

router.get('/', (req, res) => {
  res.json({
    service: 'Car Dealership Express API',
    status: 'ok',
    endpoints: [
      'GET  /fetchDealers',
      'GET  /fetchDealers/:state',
      'GET  /fetchDealer/:id',
      'GET  /fetchReviews',
      'GET  /fetchReviews/dealer/:id',
      'POST /insert_review',
      'GET  /analyze/:text',
      'POST /analyze',
    ],
  });
});

router.get('/fetchDealers', dealers.getAllDealers);
router.get('/fetchDealers/:state', dealers.getDealersByState);
router.get('/fetchDealer/:id', dealers.getDealerById);
router.get('/fetchReviews', reviews.getAllReviews);
router.get('/fetchReviews/dealer/:id', reviews.getReviewsByDealer);
router.post('/insert_review', requireApiKey, reviews.insertReview);
router.get('/analyze/:text', sentiment.analyze);
router.post('/analyze', sentiment.analyze);

module.exports = router;
