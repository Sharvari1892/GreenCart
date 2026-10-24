function About() {
  return (
    <main className="content-page">
      <span className="eyebrow">OUR PURPOSE</span>
      <h1>Making greener choices <span>simpler.</span></h1>
      <p className="page-intro">
        GreenCart helps people explore sustainable alternatives and make
        more informed everyday shopping decisions.
      </p>

      <section className="about-grid">
        <article>
          <span>🌍</span>
          <h2>Our mission</h2>
          <p>Make sustainability easier to understand and more accessible in everyday shopping.</p>
        </article>
        <article>
          <span>⚖️</span>
          <h2>Our approach</h2>
          <p>Help shoppers compare products using clear information and meaningful criteria.</p>
        </article>
        <article>
          <span>🌱</span>
          <h2>Our principle</h2>
          <p>Encourage thoughtful choices without making shopping unnecessarily complicated.</p>
        </article>
      </section>
    </main>
  );
}

export default About;