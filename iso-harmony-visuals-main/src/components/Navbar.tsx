
import React from 'react';
import { Button } from "@/components/ui/button";
import { Search, Menu } from "lucide-react";

const Navbar: React.FC = () => {
  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="mr-4 hidden md:flex">
            <a href="/" className="mr-6 flex items-center space-x-2">
              <div className="h-6 w-6 bg-blue-600 rounded animate-pulse"></div>
              <span className="hidden font-bold sm:inline-block text-xl">DocCompare</span>
            </a>
            <nav className="flex items-center gap-6 text-sm">
              <a href="#features" className="transition-colors hover:text-foreground/80 text-foreground/60">
                Features
              </a>
              <a href="#howitworks" className="transition-colors hover:text-foreground/80 text-foreground/60">
                How It Works
              </a>
              <a href="#dashboard" className="transition-colors hover:text-foreground/80 text-foreground/60">
                Dashboard
              </a>
            </nav>
          </div>
          <Button variant="outline" size="icon" className="md:hidden">
            <Menu className="h-5 w-5" />
            <span className="sr-only">Toggle Menu</span>
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative hidden md:block">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <input
              type="search"
              placeholder="Search documents..."
              className="pl-8 h-9 rounded-md border border-input bg-background ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring px-3 py-1 text-sm w-[200px] md:w-[250px] transition-all"
            />
          </div>
          <Button size="sm" className="animate-fade-in">Get Started</Button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
