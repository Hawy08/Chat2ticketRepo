import React from 'react';

// --- Official Brand Icons (Full Color Originals) ---

const WatsonIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="16" r="16" fill="#0062FF" fillOpacity="0.1"/>
    <path d="M6 16C6 11.5 8.5 7.5 12.5 5.5" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
    <path d="M10 16C10 13 11.5 10.5 14 9" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
    <path d="M26 16C26 11.5 23.5 7.5 19.5 5.5" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
    <path d="M22 16C22 13 20.5 10.5 18 9" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
    <circle cx="16" cy="16" r="3" fill="#0062FF"/>
    <path d="M16 20V26" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
    <path d="M12 26L20 26" stroke="#0062FF" strokeWidth="2" strokeLinecap="round"/>
  </svg>
);

const StripeIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path fillRule="evenodd" clipRule="evenodd" d="M11.5 12.5C11.5 11.5 12.5 11 13.8 11C15.5 11 16.8 11.5 17.5 11.8V8.5C16.5 8.2 15.2 8 14 8C10.5 8 8 9.8 8 12.8C8 17 14 16.5 14 18.5C14 19.2 13.2 19.8 12 19.8C10.5 19.8 9 19.2 8 18.8V22.2C9 22.5 10.5 22.8 12 22.8C15.8 22.8 17.5 20.8 17.5 18C17.5 13.5 11.5 14 11.5 12.5Z" fill="#635BFF"/>
  </svg>
);

const SpotifyIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="16" r="16" fill="#1DB954"/>
    <path d="M23.5 20.5C23.3 20.8 22.8 20.9 22.5 20.7C19.5 18.9 15.5 18.5 11.0 19.5C10.6 19.6 10.2 19.3 10.1 18.9C10.0 18.5 10.3 18.1 10.7 18.0C15.6 16.9 20.0 17.4 23.3 19.5C23.6 19.7 23.7 20.2 23.5 20.5ZM24.8 16.6C24.5 17.1 23.9 17.2 23.4 16.9C20.1 14.9 15.0 14.3 10.8 15.6C10.2 15.8 9.6 15.5 9.4 14.9C9.2 14.3 9.5 13.7 10.1 13.5C15.0 12.0 20.7 12.7 24.5 15.1C25.0 15.4 25.1 16.0 24.8 16.6ZM25.0 12.5C20.9 10.1 13.6 9.9 9.6 11.1C9.0 11.3 8.3 10.9 8.1 10.3C7.9 9.6 8.3 9.0 8.9 8.8C13.6 7.4 21.6 7.7 26.3 10.5C26.9 10.8 27.1 11.6 26.8 12.2C26.4 12.8 25.6 13.0 25.0 12.5Z" fill="black"/>
  </svg>
);

const MapsIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M16 4C11.6 4 8 7.6 8 12C8 16.9 14.5 25.5 14.8 25.9C15.1 26.3 15.5 26.5 16 26.5C16.5 26.5 16.9 26.3 17.2 25.9C17.5 25.5 24 16.9 24 12C24 7.6 20.4 4 16 4ZM16 16C13.8 16 12 14.2 12 12C12 9.8 13.8 8 16 8C18.2 8 20 9.8 20 12C20 14.2 18.2 16 16 16Z" fill="#EA4335"/>
    <circle cx="16" cy="12" r="2.5" fill="#1967D2"/>
  </svg>
);

const CalendarIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="5" y="6" width="22" height="22" rx="3" fill="white"/>
    <path d="M5 11H27" stroke="#F1F3F4" strokeWidth="1"/>
    <rect x="10" y="4" width="3" height="5" rx="1" fill="#1967D2"/>
    <rect x="19" y="4" width="3" height="5" rx="1" fill="#1967D2"/>
    <text x="16" y="22" fontFamily="sans-serif" fontSize="10" fontWeight="bold" fill="#1967D2" textAnchor="middle">31</text>
  </svg>
);

const GmailIcon = () => (
  <svg viewBox="0 0 32 32" className="w-8 h-8" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="8" width="24" height="16" rx="2" fill="white"/>
    <path d="M4 10L16 19L28 10" stroke="#EA4335" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M28 10V22" stroke="#34A853" strokeWidth="3" strokeLinecap="round"/>
    <path d="M4 10V22" stroke="#4285F4" strokeWidth="3" strokeLinecap="round"/>
    <path d="M26 10L16 17.5L6 10" stroke="#EA4335" strokeWidth="0" fill="none"/>
    <path d="M26 8.5L28 10" stroke="#FBBC04" strokeWidth="3" strokeLinecap="round"/>
    <path d="M6 8.5L4 10" stroke="#C5221F" strokeWidth="3" strokeLinecap="round"/>
  </svg>
);

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => (
  <div className="group p-8 rounded-3xl bg-white/5 border border-white/5 hover:border-neon/30 hover:bg-white/10 transition-all duration-300">
    <div className={`w-14 h-14 rounded-2xl bg-[#111] border border-white/10 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg group-hover:shadow-neon/20`}>
      {icon}
    </div>
    <h3 className="text-xl font-bold text-white mb-3 group-hover:text-neon transition-colors">{title}</h3>
    <p className="text-gray-400 leading-relaxed">{description}</p>
  </div>
);

const Features: React.FC = () => {
  const features = [
    {
      icon: <WatsonIcon />,
      title: "Mood-Based AI",
      description: "Our intelligent agent uses IBM Watson to analyze your mood, budget, and location to recommend events that truly resonate with how you feel right now."
    },
    {
      icon: <StripeIcon />,
      title: "In-Chat Payments",
      description: "Secure checkout powered by Stripe. Book your tickets directly within the WhatsApp conversation without ever leaving the app."
    },
    {
      icon: <MapsIcon />,
      title: "Hyper-Local Discovery",
      description: "Share your live location to find hidden gems and pop-up events happening around you within minutes using Google Maps data."
    },
    {
      icon: <SpotifyIcon />,
      title: "Spotify Integration",
      description: "After booking a concert, receive a curated Spotify playlist of the artist so you can learn the lyrics before the show."
    },
    {
      icon: <CalendarIcon />,
      title: "Calendar Auto-Sync",
      description: "Authorize the bot once, and every confirmed booking is automatically added to your Google Calendar with reminders."
    },
    {
      icon: <GmailIcon />,
      title: "Instant Confirmation",
      description: "Receive automated Gmail confirmations with QR tickets and event details immediately after successful payment."
    }
  ];

  return (
    <section id="features" className="py-24 bg-black">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white">Orchestrating your social life.</h2>
          <p className="text-gray-400 text-lg">
            Powered by IBM Orchestrate, we combine natural language processing with powerful integrations to create a seamless booking experience.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
