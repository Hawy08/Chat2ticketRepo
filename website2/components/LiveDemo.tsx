import React from 'react';
import { Smartphone, Terminal } from 'lucide-react';

const LiveDemo: React.FC = () => {
  return (
    <section id="demo" className="py-24 bg-black relative overflow-hidden">
      <div className="max-w-6xl mx-auto px-6">
        <div className="bg-[#0a0a0a] rounded-3xl p-8 md:p-16 flex flex-col md:flex-row items-center gap-12 border border-neon/30 shadow-[0_0_40px_rgba(57,255,20,0.15)]">
          
          {/* Text Content */}
          <div className="flex-1 text-center md:text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-neon/10 text-neon text-sm font-bold mb-6 border border-neon/20">
              <Smartphone className="w-4 h-4" />
              <span>Live Demo Available</span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Try Chat2Ticket now.
            </h2>
            <p className="text-lg text-gray-300 mb-8 leading-relaxed">
              Experience the future of event booking. Scan the QR code to connect with our AI sandbox on WhatsApp.
            </p>
            
            <div className="space-y-6 max-w-lg mx-auto md:mx-0">
                 <div className="flex items-start gap-4 text-left">
                    <div className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center font-bold shrink-0 text-lg">1</div>
                    <div>
                        <h4 className="text-white font-bold text-lg">Scan the QR Code</h4>
                        <p className="text-gray-400">Open your camera or WhatsApp to scan.</p>
                    </div>
                 </div>
                 <div className="flex items-start gap-4 text-left">
                    <div className="w-8 h-8 rounded-full bg-neon text-black flex items-center justify-center font-bold shrink-0 text-lg">2</div>
                    <div>
                        <h4 className="text-white font-bold text-lg">Send the Activation Code</h4>
                        <p className="text-gray-400 mb-3">You must send this exact text to connect:</p>
                        <div className="inline-flex items-center gap-3 bg-black px-5 py-4 rounded-xl border border-neon/50 shadow-[0_0_15px_rgba(57,255,20,0.2)]">
                            <Terminal className="w-5 h-5 text-neon" />
                            <span className="font-mono text-xl text-neon font-bold tracking-wide">join blue-noise</span>
                        </div>
                    </div>
                 </div>
            </div>

          </div>

          {/* QR Code Container */}
          <div className="flex-1 flex flex-col items-center justify-center relative">
            <div className="relative bg-white p-4 rounded-2xl rotate-0 hover:scale-105 transition-transform duration-300 shadow-[0_0_50px_rgba(57,255,20,0.4)] ring-4 ring-neon/20">
               {/* QR Code pointing to WhatsApp with pre-filled text */}
               <img 
                 src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://wa.me/14155238886?text=join%20blue-noise&color=000000&bgcolor=FFFFFF" 
                 alt="Scan to chat on WhatsApp" 
                 className="w-64 h-64 md:w-80 md:h-80 object-contain mix-blend-multiply"
               />
            </div>
            <div className="mt-8 text-center">
                <p className="text-gray-400 text-sm mb-2 uppercase tracking-widest text-[10px]">Twilio Sandbox Number</p>
                <p className="text-2xl font-mono text-white font-bold tracking-wider select-all">+1 (415) 523-8886</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LiveDemo;