import React from 'react';
import { Link } from 'react-router-dom';
import styles from './LandingPage.module.scss';

function LandingPage() {
  return (
    <div className={styles.LandingPage}>
      <header className={styles.Header}>
        <h1>Elevate Your Videos with Seamless Logo Integration</h1>
        <p>Transform ordinary scenes into dynamic branding opportunities.</p>
        <Link className={styles.CtaButton} to="/login">Get Started Now</Link>
      </header>

      <section className={styles.FeaturesSection}>
        <h2>Why Choose Our Video Enhancement Tool?</h2>
        <ul>
          <li><strong>Easy Logo Placement:</strong> Upload your video and logo, select the scene, and let our tool handle the rest.</li>
          <li><strong>Advanced Scene Replacement:</strong> Replace screens or billboards with custom content, perfect for targeted placements.</li>
          <li><strong>High-Quality Rendering:</strong> Supports up to 4K resolution, preserving video quality.</li>
          <li><strong>User-Friendly Interface:</strong> No technical skills required, ideal for all users.</li>
          <li><strong>Fast Processing:</strong> Get your video ready in minutes.</li>
        </ul>
      </section>

      <section className={styles.HowItWorksSection}>
        <h2>How It Works</h2>
        <ol>
          <li><strong>Upload Your Video:</strong> Choose any video you want to enhance.</li>
          <li><strong>Select the Scene:</strong> Navigate to the scene or screen you want to modify.</li>
          <li><strong>Add Your Logo:</strong> Upload your branding or ad image, adjust size and position.</li>
          <li><strong>Preview and Adjust:</strong> Watch a live preview and make any tweaks.</li>
          <li><strong>Download and Share:</strong> Export your video and share it across platforms.</li>
        </ol>
      </section>

      <section className={styles.TestimonialsSection}>
        <h2>What Our Users Are Saying</h2>
        <blockquote>
          "This tool has revolutionized our marketing efforts. It's incredibly easy to use and the results are phenomenal!"
          <footer>— Alex Martinez, Digital Marketer</footer>
        </blockquote>
        <blockquote>
          "I was amazed at how quickly I could add our company logo to our promotional videos. Highly recommend!"
          <footer>— Sarah Lee, Content Creator</footer>
        </blockquote>
      </section>
    </div>
  );
}

export default LandingPage;
