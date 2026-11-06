const { Schema, model } = require('mongoose');

const reviewSchema = new Schema(
  {
    id: { type: Number, required: true, unique: true, index: true },
    name: { type: String, required: true, trim: true },
    dealership: { type: Number, required: true, index: true },
    review: { type: String, required: true, trim: true },
    purchase: { type: Boolean, default: false },
    purchase_date: { type: String, default: '' },
    car_make: { type: String, default: '' },
    car_model: { type: String, default: '' },
    car_year: { type: Number },
    rating: { type: Number, min: 1, max: 5, required: true },
    sentiment: { type: String, enum: ['positive', 'neutral', 'negative'] },
    created_at: { type: Date, default: Date.now },
  },
  { versionKey: false }
);

module.exports = model('Review', reviewSchema, 'reviews');
