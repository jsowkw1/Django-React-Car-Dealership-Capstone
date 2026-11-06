const { HttpError } = require('./errors');

// Protects write endpoints. When API_KEY is set, callers (the Django backend)
// must send it in the X-API-Key header; otherwise the request gets a 401.
function requireApiKey(req, res, next) {
  const expected = process.env.API_KEY;
  if (!expected) return next();
  if (req.get('X-API-Key') !== expected) {
    return next(new HttpError(401, 'Unauthorized: missing or invalid X-API-Key header'));
  }
  return next();
}

module.exports = { requireApiKey };
