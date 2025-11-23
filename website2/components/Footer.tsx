import React from 'react';
import { Github, Code, ExternalLink } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="py-12 bg-black border-t border-white/10 text-center md:text-left">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
        
        <div>
          <div className="flex items-center justify-center md:justify-start gap-2 mb-2">
             <div className="w-6 h-6 bg-neon rounded-md" />
             <span className="text-xl font-bold text-white">Chat2Ticket</span>
          </div>
          <p className="text-gray-500 text-sm">
            Built for the IBM Orchestrate Hackathon 2024.
          </p>
        </div>

        <div className="flex items-center gap-6">
          <a href="#" className="text-gray-500 hover:text-neon transition-colors flex items-center gap-2 text-sm">
            <Github className="w-4 h-4" /> Source Code
          </a>
          <a href="#" className="text-gray-500 hover:text-neon transition-colors flex items-center gap-2 text-sm">
            <Code className="w-4 h-4" /> DevPost
          </a>
          <a href="#" className="text-gray-500 hover:text-neon transition-colors flex items-center gap-2 text-sm">
            <ExternalLink className="w-4 h-4" /> IBM Orchestrate
          </a>
        </div>
      </div>
      
      <div className="mt-12 text-center text-gray-600 text-xs px-6">
        <p>Disclaimer: This is a prototype demonstration. Events and payments are processed in test mode.</p>
      </div>
    </footer>
  );
};

export default Footer;