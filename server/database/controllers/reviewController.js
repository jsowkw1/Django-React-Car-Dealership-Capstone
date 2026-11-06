const Review = require('../models/Review');
const Dealership = require('../models/Dealership');
const { HttpError } = require('../middleware/errors');
const { analyzeText } = require('../services/sentiment');

const projection = { _id: 0 };

async function getAllReviews(req, res) {
  const reviews = await Review.find({}, projection).sort({ id: 1 }).lean();
  res.json(reviews);
}

async function getReviewsByDealer(req, res) {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) throw new HttpError(400, 'Dealer id must be a positive integer');
  const reviews = await Review.find({ dealership: id }, projection).sort({ id: -1 }).lean();
  res.json(reviews);
}

function validateReview(body) {
  if (!body || typeof body !== 'object') return ['Request body must be a JSON object'];
  const errors = [];
  if (!String(body.name || '').trim()) errors.push('name is required');
  const dealership = Number(body.dealership);
  if (!Number.isInteger(dealership) || dealership < 1) errors.push('dealership must be a positive integer');
  if (!String(body.review || '').trim()) errors.push('review is required');
  if (String(body.review || '').length > 2000) errors.push('review must be at most 2000 characters');
  const rating = Number(body.rating);
  if (!Number.isInteger(rating) || rating < 1 || rating > 5) errors.push('rating must be an integer from 1 to 5');
  if (body.car_year !== undefined && body.car_year !== '' && body.car_year !== null) {
    const year = Number(body.car_year);
    if (!Number.isInteger(year) || year < 1950 || year > 2030) errors.push('car_year must be between 1950 and 2030');
  }
  return errors;
}

async function insertReview(req, res) {
  const errors = validateReview(req.body);
  if (errors.length) throw new HttpError(400, errors.join('; '));
  const dealershipId = Number(req.body.dealership);
  if (!(await Dealership.exists({ id: dealershipId }))) throw new HttpError(404, `Dealer ${dealershipId} not found`);

  const last = await Review.findOne({}, { id: 1 }).sort({ id: -1 }).lean();
  const review = await Review.create({
    id: last ? last.id + 1 : 1,
    name: String(req.body.name).trim(),
    dealership: dealershipId,
    review: String(req.body.review).trim(),
    purchase: req.body.purchase === true || req.body.purchase === 'true',
    purchase_date: req.body.purchase_date || '',
    car_make: req.body.car_make || '',
    car_model: req.body.car_model || '',
    car_year: req.body.car_year ? Number(req.body.car_year) : undefined,
    rating: Number(req.body.rating),
    sentiment: analyzeText(req.body.review).sentiment,
  });
  const { _id, ...saved } = review.toObject();
  res.status(201).json(saved);
}

module.exports = { getAllReviews, getReviewsByDealer, insertReview, validateReview };
