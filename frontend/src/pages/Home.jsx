import { Link } from "react-router-dom";

function Home() {
  return (
    <main className="home-page">
      <section className="hero">
        <div className="hero-content">
          <span className="eyebrow">A GREENER WAY TO SHOP</span>
          <h1>Better choices.<br /><span>Greener future.</span></h1>
          <p>
            Discover everyday products, compare their environmental impact,
            and make choices that are kinder to our planet.
          </p>
          <Link className="primary-button" to="/products">
            Explore products <span>→</span>
          </Link>

          <div className="hero-stats">
            <div><strong>Thoughtful</strong><small>product discovery</small></div>
            <div><strong>Eco-aware</strong><small>shopping choices</small></div>
            <div><strong>Easy</strong><small>product comparison</small></div>
          </div>
        </div>

        <div className="hero-art">
          <div className="art-circle"></div>
          <div className="floating-card top-card">
            🌱 <span>Small choices,<br />big impact</span>
          </div>
          <div className="plant">🪴</div>
          <div className="floating-card bottom-card">
            ♻️ <span>Shop with<br />the planet in mind</span>
          </div>
        </div>
      </section>

      <section className="benefits">
        <div><span>🌍</span><div><strong>Planet-conscious</strong><small>Explore greener alternatives</small></div></div>
        <div><span>⚖️</span><div><strong>Compare products</strong><small>Make informed decisions</small></div></div>
        <div><span>🛒</span><div><strong>Shop smarter</strong><small>Find what fits your needs</small></div></div>
      </section>

      <section className="home-discover">
        <span className="eyebrow">YOUR NEXT BETTER CHOICE</span>
        <h2>Small changes start here.</h2>
        <p>Explore everyday essentials and compare options before making your choice.</p>
        <div className="home-actions">
          <Link className="primary-button" to="/products">Browse products →</Link>
          <Link className="secondary-button" to="/compare">Compare products</Link>
        </div>
      </section>
    </main>
  );
}

export default Home;