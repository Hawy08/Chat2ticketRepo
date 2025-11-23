import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import Workflow from './components/Workflow';
import Presentation from './components/Presentation';
import VideoDemo from './components/VideoDemo';
import LiveDemo from './components/LiveDemo';
import Footer from './components/Footer';

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Hero />
        <Features />
        <Workflow />
        <Presentation />
        <VideoDemo />
        <LiveDemo />
      </main>
      <Footer />
    </div>
  );
};

export default App;