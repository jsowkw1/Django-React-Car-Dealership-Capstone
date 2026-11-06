export function Stars({ value, size = 'md' }) {
  const rounded = Math.round(value || 0);
  return (
    <span className={`stars stars-${size}`} aria-label={`${value} out of 5 stars`}>
      {[1, 2, 3, 4, 5].map((i) => (
        <span key={i} className={i <= rounded ? 'star on' : 'star'}>★</span>
      ))}
    </span>
  );
}

const SENTIMENT_ICONS = { positive: '😊', neutral: '😐', negative: '☹️' };

export function SentimentBadge({ sentiment = 'neutral' }) {
  return (
    <span className={`badge badge-${sentiment}`} title={`Sentiment: ${sentiment}`}>
      {SENTIMENT_ICONS[sentiment] || SENTIMENT_ICONS.neutral} {sentiment}
    </span>
  );
}

export function Alert({ type = 'info', children, onClose }) {
  if (!children) return null;
  return (
    <div className={`alert alert-${type}`} role="alert">
      <span>{children}</span>
      {onClose && <button className="alert-close" onClick={onClose} aria-label="Dismiss">×</button>}
    </div>
  );
}

export function Spinner({ label = 'Loading…' }) {
  return <div className="spinner-wrap"><div className="spinner" /> <span>{label}</span></div>;
}

export function DealerImage({ src, alt }) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      onError={(e) => { e.currentTarget.classList.add('img-fallback'); e.currentTarget.removeAttribute('src'); }}
    />
  );
}
