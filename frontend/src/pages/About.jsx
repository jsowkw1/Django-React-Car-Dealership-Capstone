const img = (id) => `https://images.unsplash.com/photo-${id}?w=480&h=480&q=70&auto=format&fit=crop&crop=faces`;

// Fictional demonstration team (stock portraits from Unsplash).
const TEAM = [
  { name: 'Daniel Morgan', role: 'Chief Executive Officer', photo: img('1507003211169-0a1dd7228f2d'),
    email: 'daniel.morgan@bestcars-demo.com', bio: 'Twenty years in automotive retail. Daniel built the Best Cars network around one idea: transparent, review-driven car buying.' },
  { name: 'Sarah Mitchell', role: 'Head of Dealer Relations', photo: img('1494790108377-be9c29b29330'),
    email: 'sarah.mitchell@bestcars-demo.com', bio: 'Sarah onboards and audits every partner dealership, making sure each one meets our service and pricing standards.' },
  { name: 'James Carter', role: 'Lead Software Engineer', photo: img('1500648767791-00dcc994a43e'),
    email: 'james.carter@bestcars-demo.com', bio: 'James leads the Django, React and Node.js platform, including the review sentiment analysis service.' },
  { name: 'Olivia Bennett', role: 'Customer Experience Manager', photo: img('1438761681033-6461ffad8d80'),
    email: 'olivia.bennett@bestcars-demo.com', bio: 'Olivia and her team answer customer questions and help resolve any issue raised in a review within 48 hours.' },
];

export default function About() {
  return (
    <>
      <section className="page-hero" style={{ backgroundImage: 'linear-gradient(rgba(11,31,58,.82), rgba(11,31,58,.82)), url(https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1600&q=70&auto=format&fit=crop)' }}>
        <div className="container">
          <span className="eyebrow">About Us</span>
          <h1>Driving trust in car buying since 2009</h1>
          <p>
            Best Cars is a national network of independent and franchise dealerships. We publish honest customer
            reviews, analyse their sentiment automatically and work with dealers to keep service quality high.
          </p>
        </div>
      </section>
      <div className="container page">
        <div className="values">
          <div className="card value"><h3>🔍 Transparency</h3><p>Every review is published as written, with its rating and detected sentiment.</p></div>
          <div className="card value"><h3>🤝 Verified dealers</h3><p>Partner dealerships are inspected for fair pricing and customer care.</p></div>
          <div className="card value"><h3>⚡ Fast support</h3><p>Our team follows up on negative experiences within two business days.</p></div>
        </div>
        <h2 className="section-title center">Meet our team</h2>
        <p className="muted center">Demonstration team — fictional profiles created for this capstone project.</p>
        <div className="team">
          {TEAM.map((m) => (
            <article className="card team-card" key={m.email}>
              <img src={m.photo} alt={`Portrait of ${m.name}`} />
              <div className="card-body">
                <h3>{m.name}</h3>
                <p className="role">{m.role}</p>
                <p className="desc">{m.bio}</p>
                <a href={`mailto:${m.email}`} className="email">✉ {m.email}</a>
              </div>
            </article>
          ))}
        </div>
      </div>
    </>
  );
}
