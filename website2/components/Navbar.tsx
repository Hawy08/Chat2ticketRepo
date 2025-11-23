import React, { useState, useEffect } from 'react';
import { Bot, Menu, X } from 'lucide-react';

const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (id: string) => {
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMobileMenuOpen(false);
    }
  };

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-black border-b border-white/10 py-4' : 'bg-transparent py-6'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        <div className="flex items-center gap-2 cursor-pointer" onClick={() => scrollToSection('hero')}>
          <div className="w-10 h-10 rounded-xl bg-neon flex items-center justify-center">
            <Bot className="text-black w-6 h-6" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">Chat2Ticket</span>
        </div>

        {/* Desktop Nav */}
        <div className="hidden md:flex items-center gap-6 lg:gap-8">
          <button onClick={() => scrollToSection('features')} className="text-sm font-medium text-gray-300 hover:text-neon transition-colors">Features</button>
          <button onClick={() => scrollToSection('workflow')} className="text-sm font-medium text-gray-300 hover:text-neon transition-colors">How it Works</button>
          <button onClick={() => scrollToSection('presentation')} className="text-sm font-medium text-gray-300 hover:text-neon transition-colors">Pitch Deck</button>
          <button onClick={() => scrollToSection('video-demo')} className="text-sm font-medium text-gray-300 hover:text-neon transition-colors">Video</button>
          <button 
            onClick={() => scrollToSection('demo')} 
            className="bg-white text-black px-5 py-2.5 rounded-full text-sm font-bold hover:bg-neon hover:text-black transition-all duration-300"
          >
            Try Demo
          </button>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden">
          <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="text-white p-2 hover:text-neon">
            {isMobileMenuOpen ? <X /> : <Menu />}
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-black border-b border-white/10 p-6 flex flex-col gap-4 shadow-2xl">
          <button onClick={() => scrollToSection('features')} className="text-left text-gray-300 hover:text-neon py-2">Features</button>
          <button onClick={() => scrollToSection('workflow')} className="text-left text-gray-300 hover:text-neon py-2">How it Works</button>
          <button onClick={() => scrollToSection('presentation')} className="text-left text-gray-300 hover:text-neon py-2">Pitch Deck</button>
          <button onClick={() => scrollToSection('video-demo')} className="text-left text-gray-300 hover:text-neon py-2">Video</button>
          <button 
            onClick={() => scrollToSection('demo')} 
            className="bg-neon text-black px-5 py-3 rounded-lg text-center font-bold"
          >
            Try Demo
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;