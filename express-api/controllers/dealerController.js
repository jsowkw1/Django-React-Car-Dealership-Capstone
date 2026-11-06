const Dealership = require('../models/Dealership');
const { HttpError } = require('../middleware/errors');

const escapeRegex = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

async function getAllDealers(req, res) {
  const dealers = await Dealership.find({}, { _id: 0 }).sort({ id: 1 }).lean();
  res.json(dealers);
}

// Accepts a full state name ("Kansas") or a two-letter code ("KS"), any case.
async function getDealersByState(req, res) {
  const state = String(req.params.state || '').trim();
  if (!state) throw new HttpError(400, 'State is required');
  const exact = new RegExp(`^${escapeRegex(state)}$`, 'i');
  const dealers = await Dealership.find({ $or: [{ state: exact }, { st: exact }] }, { _id: 0 })
    .sort({ id: 1 })
    .lean();
  res.json(dealers);
}

async function getDealerById(req, res) {
  const id = Number(req.params.id);
  if (!Number.isInteger(id) || id < 1) throw new HttpError(400, 'Dealer id must be a positive integer');
  const dealer = await Dealership.findOne({ id }, { _id: 0 }).lean();
  if (!dealer) throw new HttpError(404, `Dealer ${id} not found`);
  res.json(dealer);
}

module.exports = { getAllDealers, getDealersByState, getDealerById };
