/**
 * LabValueCard.jsx
 * Renders a single lab test result as a card.
 * Shows name, value + unit, color-coded status badge,
 * and a plain-English explanation for abnormal values.
 *
 * Status colors: normal=green, high=orange, low=blue, critical=red
 */

import "./LabValueCard.css";

const STATUS_META = {
  normal:   { label: "Normal",   symbol: "✓" },
  high:     { label: "High",     symbol: "↑" },
  low:      { label: "Low",      symbol: "↓" },
  critical: { label: "Critical", symbol: "⚠" },
};

function LabValueCard({ name, value, unit, status, explanation }) {
  const meta = STATUS_META[status] || STATUS_META.normal;

  return (
    <div className={`lab-card lab-card--${status}`}>
      <div className="lab-card__header">
        <span className="lab-card__name">{name}</span>
        <span className={`lab-card__badge lab-card__badge--${status}`}>
          <span className="badge-symbol" aria-hidden="true">{meta.symbol}</span>
          {meta.label}
        </span>
      </div>

      <div className="lab-card__value">
        <span className="lab-card__number">{value}</span>
        {unit && <span className="lab-card__unit">{unit}</span>}
      </div>

      {explanation && (
        <p className="lab-card__explanation">{explanation}</p>
      )}
    </div>
  );
}

export default LabValueCard;