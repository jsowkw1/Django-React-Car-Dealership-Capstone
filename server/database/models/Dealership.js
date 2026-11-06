const { Schema, model } = require('mongoose');

const dealershipSchema = new Schema(
  {
    id: { type: Number, required: true, unique: true, index: true },
    full_name: { type: String, required: true },
    short_name: { type: String, required: true },
    address: { type: String, required: true },
    city: { type: String, required: true },
    state: { type: String, required: true, index: true },
    st: { type: String, required: true, uppercase: true, index: true },
    zip: { type: String, required: true },
    lat: Number,
    long: Number,
    phone: String,
    description: String,
    image: String,
  },
  { versionKey: false }
);

module.exports = model('Dealership', dealershipSchema, 'dealerships');
