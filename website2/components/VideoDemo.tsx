import React from 'react';
import { Play } from 'lucide-react';

const VideoDemo: React.FC = () => {
  return (
    <section id="video-demo" className="py-24 bg-black border-t border-white/5 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center max-w-3xl mx-auto mb-12">
           <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-neon text-sm font-bold mb-6">
              <Play className="w-4 h-4" />
              <span>Watch Demo</span>
            </div>
          <h2 className="text-3xl md:text-5xl font-bold mb-6 text-white">See it in Action</h2>
          <p className="text-gray-400 text-lg">
             A complete walkthrough of the Chat2Ticket booking flow.
          </p>
        </div>

        {/* 
            TODO: When your video is uploaded, replace the inner div below with your iframe.
            Example:
            <iframe 
              className="w-full h-full"
              src="https://www.youtube.com/embed/YOUR_VIDEO_ID" 
              title="YouTube video player" 
              frameBorder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowFullScreen
            ></iframe>
        */}
        <div className="relative w-full max-w-5xl mx-auto aspect-video rounded-2xl overflow-hidden border border-white/10 shadow-[0_0_40px_rgba(57,255,20,0.1)] bg-[#111] group">
            <iframe 
              className="w-full h-full"
              src="https://www.youtube.com/embed/-DzfgYoXdZM" 
              title="Chat2Ticket Demo" 
              frameBorder="0" 
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
              allowFullScreen
            ></iframe>
        </div>
      </div>
    </section>
  );
};

export default VideoDemo;