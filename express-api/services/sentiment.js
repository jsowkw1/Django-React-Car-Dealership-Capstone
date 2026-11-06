const Sentiment = require('sentiment');

// Lexicon-based analyzer (AFINN-165 word list with negation handling).
// Every known word is scored from -5 to +5; the comparative score is the
// total divided by the number of tokens, which is mapped to a label.
const analyzer = new Sentiment();
const THRESHOLD = 0.05;

function analyzeText(text) {
  const result = analyzer.analyze(String(text));
  let sentiment = 'neutral';
  if (result.comparative > THRESHOLD) sentiment = 'positive';
  else if (result.comparative < -THRESHOLD) sentiment = 'negative';
  return {
    text: String(text),
    sentiment,
    score: result.score,
    comparative: Number(result.comparative.toFixed(4)),
    positive_words: result.positive,
    negative_words: result.negative,
    analyzer: 'AFINN-165 lexicon (npm sentiment)',
  };
}

module.exports = { analyzeText };
