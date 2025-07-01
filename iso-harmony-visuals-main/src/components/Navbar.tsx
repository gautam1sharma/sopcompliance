import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import NotificationCenter from './NotificationCenter';
import { 
  Shield, 
  Menu, 
  X, 
  ChevronDown,
  FileText,
  BarChart3,
  Settings,
  User,
  LogOut,
  Moon,
  Sun
} from "lucide-react";

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
    // In a real app, you'd implement actual dark mode logic here
  };

  return (
    <nav className={`sticky top-0 z-50 transition-all duration-300 ${
      isScrolled 
        ? 'bg-white/90 backdrop-blur-lg border-b border-white/20 shadow-lg' 
        : 'bg-white/80 backdrop-blur-md border-b border-white/10'
    }`}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="relative group">
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur-lg opacity-30 group-hover:opacity-50 transition-opacity"></div>
              <div className="relative w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform">
                <Shield className="h-6 w-6 text-white" />
              </div>
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                ISO Compliance
              </h1>
              <p className="text-xs text-slate-500 -mt-1">Checker</p>
            </div>
            <Badge variant="secondary" className="hidden sm:flex text-xs">
              v2.0
            </Badge>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <a href="#features" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Features
            </a>
            <a href="#howitworks" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              How It Works
            </a>
            <a href="#documents" className="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Documents
            </a>
            <div className="relative group">
              <button className="flex items-center text-slate-600 hover:text-blue-600 transition-colors font-medium">
                Resources
                <ChevronDown className="h-4 w-4 ml-1 group-hover:rotate-180 transition-transform" />
              </button>
              <div className="absolute top-full left-0 mt-2 w-48 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform group-hover:translate-y-0 translate-y-2">
                <div className="bg-white/90 backdrop-blur-lg rounded-xl shadow-xl border border-white/20 py-2">
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 transition-colors">
                    <FileText className="h-4 w-4 mr-3 text-blue-600" />
                    Documentation
                  </a>
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 transition-colors">
                    <BarChart3 className="h-4 w-4 mr-3 text-green-600" />
                    API Reference
                  </a>
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 transition-colors">
                    <Settings className="h-4 w-4 mr-3 text-purple-600" />
                    Support
                  </a>
                </div>
              </div>
            </div>
          </div>

          {/* Desktop Actions */}
          <div className="hidden md:flex items-center space-x-4">
            <NotificationCenter />
            
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleDarkMode}
              className="text-slate-600 hover:text-blue-600"
            >
              {isDarkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
            </Button>
            
            <div className="relative group">
              <Button variant="ghost" size="sm" className="flex items-center space-x-2">
                <User className="h-4 w-4" />
                <span className="text-sm">Account</span>
                <ChevronDown className="h-3 w-3 group-hover:rotate-180 transition-transform" />
              </Button>
              <div className="absolute top-full right-0 mt-2 w-48 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 transform group-hover:translate-y-0 translate-y-2">
                <div className="bg-white/90 backdrop-blur-lg rounded-xl shadow-xl border border-white/20 py-2">
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 transition-colors">
                    <User className="h-4 w-4 mr-3 text-blue-600" />
                    Profile
                  </a>
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-slate-700 hover:bg-blue-50 transition-colors">
                    <Settings className="h-4 w-4 mr-3 text-slate-600" />
                    Settings
                  </a>
                  <hr className="my-1 border-slate-200" />
                  <a href="#" className="flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors">
                    <LogOut className="h-4 w-4 mr-3" />
                    Sign Out
                  </a>
                </div>
              </div>
            </div>

            <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all">
              Get Started
            </Button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleMenu}
              className="text-slate-600"
            >
              {isMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden absolute top-16 left-0 right-0 bg-white/95 backdrop-blur-lg border-b border-white/20 shadow-lg animate-fade-in">
            <div className="px-4 py-6 space-y-4">
              <div className="space-y-3">
                <a 
                  href="#features" 
                  className="block text-slate-700 hover:text-blue-600 transition-colors font-medium py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Features
                </a>
                <a 
                  href="#howitworks" 
                  className="block text-slate-700 hover:text-blue-600 transition-colors font-medium py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  How It Works
                </a>
                <a 
                  href="#documents" 
                  className="block text-slate-700 hover:text-blue-600 transition-colors font-medium py-2"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Documents
                </a>
                
                <div className="border-t border-slate-200 pt-3">
                  <h4 className="text-sm font-semibold text-slate-500 mb-2">Resources</h4>
                  <div className="space-y-2 pl-4">
                    <a href="#" className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1">
                      <FileText className="h-4 w-4 mr-2" />
                      Documentation
                    </a>
                    <a href="#" className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1">
                      <BarChart3 className="h-4 w-4 mr-2" />
                      API Reference
                    </a>
                    <a href="#" className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1">
                      <Settings className="h-4 w-4 mr-2" />
                      Support
                    </a>
                  </div>
                </div>

                <div className="border-t border-slate-200 pt-3">
                  <h4 className="text-sm font-semibold text-slate-500 mb-2">Account</h4>
                  <div className="space-y-2 pl-4">
                    <a href="#" className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1">
                      <User className="h-4 w-4 mr-2" />
                      Profile
                    </a>
                    <a href="#" className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1">
                      <Settings className="h-4 w-4 mr-2" />
                      Settings
                    </a>
                    <button 
                      onClick={toggleDarkMode}
                      className="flex items-center text-slate-600 hover:text-blue-600 transition-colors py-1 w-full text-left"
                    >
                      {isDarkMode ? <Sun className="h-4 w-4 mr-2" /> : <Moon className="h-4 w-4 mr-2" />}
                      {isDarkMode ? 'Light Mode' : 'Dark Mode'}
                    </button>
                  </div>
                </div>
              </div>

              <div className="pt-4 space-y-3">
                <Button 
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Get Started
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Sign In
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
