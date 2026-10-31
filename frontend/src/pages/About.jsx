import { Link } from "react-router-dom";

function About() {
  return (
    <main>
      {/* ── Hero ─────────────────────────────────────────── */}
      <section className="about-hero" aria-labelledby="about-heading">
        <div style={{ maxWidth: "var(--max-w-content)", margin: "0 auto" }}>
          <span className="eyebrow">Our purpose</span>
          <h1 id="about-heading">
            Making greener choices <em>simpler.</em>
          </h1>
          <p className="about-intro">
            GreenCart helps people explore sustainable alternatives and make
            more informed everyday shopping decisions — without the overwhelm.
          </p>
        </div>
      </section>

      {/* ── Mission cards ────────────────────────────────── */}
      <div className="section-wrap">
        <section className="about-grid" aria-labelledby="mission-heading">
          <h2 id="mission-heading" className="sr-only">Our mission, approach, and principles</h2>

          <article className="about-card">
            <div className="about-card-icon" aria-hidden="true">🌍</div>
            <h2>Our mission</h2>
            <p>
              Make sustainability easier to understand and more accessible in
              everyday shopping. We believe small individual choices, made
              consistently, create meaningful collective change.
            </p>
          </article>

          <article className="about-card">
            <div className="about-card-icon" aria-hidden="true">⚖️</div>
            <h2>Our approach</h2>
            <p>
              Help shoppers compare products using clear information and
              meaningful criteria like durability, packaging, and repairability —
              not just marketing claims.
            </p>
          </article>

          <article className="about-card">
            <div className="about-card-icon" aria-hidden="true">🌱</div>
            <h2>Our principle</h2>
            <p>
              Encourage thoughtful choices without making shopping unnecessarily
              complicated. Greener living should be achievable, not aspirational.
            </p>
          </article>
        </section>

        {/* ── CTA ─────────────────────────────────────────── */}
        <div className="about-cta" role="complementary" aria-label="Start shopping">
          <h2>Ready to shop with purpose?</h2>
          <p>
            Explore our full product catalogue and compare sustainability
            scores side by side — for free, always.
          </p>
          <div style={{ display: "flex", gap: "var(--space-4)", justifyContent: "center", flexWrap: "wrap" }}>
            <Link className="primary-button" to="/products">
              Browse products ↗
            </Link>
            <Link className="secondary-button" to="/compare">
              Compare products
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}

export default About;