
import React from 'react';

const AnimatedBackground: React.FC = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute -top-40 -right-40 h-96 w-96 rounded-full bg-blue-400/20 blur-3xl" />
      <div className="absolute top-1/2 left-20 h-64 w-64 rounded-full bg-blue-300/20 blur-3xl animate-float" 
           style={{animationDelay: "-1s"}} />
      <div className="absolute bottom-40 right-20 h-80 w-80 rounded-full bg-blue-500/20 blur-3xl animate-float"
           style={{animationDelay: "-2s"}} />
      <div className="absolute -bottom-20 left-1/3 h-72 w-72 rounded-full bg-blue-400/15 blur-3xl animate-float"
           style={{animationDelay: "-3s"}} />
           
      {/* Grid pattern */}
      <div className="absolute inset-0 bg-grid-slate-200/[0.04] bg-[length:40px_40px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>
    </div>
  );
};

export default AnimatedBackground;
