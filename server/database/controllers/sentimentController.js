const { analyzeText } = require('../services/sentiment');
const { HttpError } = require('../middleware/errors');

function analyze(req, res) {
  const text = req.params.text ?? req.body?.text ?? req.query.text;
  if (!text || !String(text).trim()) throw new HttpError(400, 'Text to analyze is required');
  res.json(analyzeText(text));
}

module.exports = { analyze };
