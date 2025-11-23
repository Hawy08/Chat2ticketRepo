import React from 'react';
import { MessageSquare, Search, CreditCard, PartyPopper } from 'lucide-react';

const Workflow: React.FC = () => {
  const steps = [
    {
      id: 1,
      icon: <MessageSquare />,
      title: "Chat",
      desc: "Say 'Hello' and describe your mood or budget."
    },
    {
      id: 2,
      icon: <Search />,
      title: "Discover",
      desc: "AI suggests curated events matching your vibe."
    },
    {
      id: 3,
      icon: <CreditCard />,
      title: "Book",
      desc: "Pay securely via Stripe inside WhatsApp."
    },
    {
      id: 4,
      icon: <PartyPopper />,
      title: "Experience",
      desc: "Get Calendar sync & Spotify playlists instantly."
    }
  ];

  return (
    <section id="workflow" className="py-24 border-y border-white/5 bg-black relative overflow-hidden">
       {/* Decorative line (Solid now, no gradient) */}
       <div className="absolute top-1/2 left-0 w-full h-px bg-white/5 hidden md:block" />

      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="mb-16">
           <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">How it works</h2>
           <p className="text-gray-400">From zero to booked in four simple steps.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 md:gap-6">
          {steps.map((step) => (
            <div key={step.id} className="relative flex flex-col items-center text-center group">
              <div className="w-16 h-16 rounded-full bg-[#1E1E1E] border border-white/10 flex items-center justify-center text-white mb-6 relative z-10 group-hover:scale-110 group-hover:border-neon transition-all duration-300 shadow-lg shadow-black/50">
                {step.icon}
                <div className="absolute -top-2 -right-2 w-6 h-6 bg-neon rounded-full flex items-center justify-center text-xs font-bold text-black">
                  {step.id}
                </div>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{step.title}</h3>
              <p className="text-sm text-gray-400 max-w-[200px]">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Workflow;