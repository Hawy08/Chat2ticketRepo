import React from 'react';
import { FileText, ExternalLink } from 'lucide-react';

const Presentation: React.FC = () => {
  return (
    <section id="presentation" className="py-24 bg-black border-t border-white/5 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-12">
           <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-neon text-sm font-bold mb-6">
              <FileText className="w-4 h-4" />
              <span>Hackathon Pitch</span>
            </div>
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white">Project Presentation</h2>
          <p className="text-gray-400 text-lg">
            Deep dive into our architecture, market analysis, and future roadmap.
          </p>
        </div>

        <div className="relative w-full max-w-5xl mx-auto aspect-video rounded-2xl overflow-hidden border border-white/10 shadow-[0_0_40px_rgba(57,255,20,0.1)] bg-[#111]">
          <iframe 
            src="https://drive.google.com/file/d/1nee_WgMjIlNW0rJwbCOC21ltu5KcJuIx/preview" 
            className="absolute top-0 left-0 w-full h-full"
            allow="autoplay"
            title="Project Presentation"
          ></iframe>
        </div>

        <div className="flex justify-center mt-8">
            <a 
                href="https://drive.google.com/file/d/1nee_WgMjIlNW0rJwbCOC21ltu5KcJuIx/view?ts=69230164" 
                target="_blank" 
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-6 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-full text-white font-medium transition-all group"
            >
                <span>Open PDF in New Tab</span>
                <ExternalLink className="w-4 h-4 group-hover:text-neon transition-colors" />
            </a>
        </div>
      </div>
    </section>
  );
};

export default Presentation;