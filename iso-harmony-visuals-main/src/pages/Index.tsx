import React, { useState } from 'react';
import Navbar from '@/components/Navbar';
import AnimatedBackground from '@/components/AnimatedBackground';
import DocumentCard from '@/components/DocumentCard';
import ComparisonView from '@/components/ComparisonView';
import Dashboard from '@/components/Dashboard';
import FileUploader from '@/components/FileUploader';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { ArrowRight, FileText, ShieldCheck, BarChart2, Sparkles, Zap, Target, CheckCircle2, Star, Users, Trophy, Lock } from 'lucide-react';

const Index = () => {
  const [selectedView, setSelectedView] = useState<'landing' | 'comparison' | 'dashboard' | 'upload'>('landing');

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-50 via-blue-50/30 to-indigo-50">
      <AnimatedBackground />
      <Navbar />

      <main className="flex-1 container py-8">
        {selectedView === 'landing' ? (
          <div className="space-y-32">
            {/* Enhanced Hero Section */}
            <section className="py-20 relative">
              <div className="max-w-4xl mx-auto text-center">
                {/* Floating badge with enhanced styling */}
                <div className="mb-8 inline-block">
                  <div className="relative group">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-blue-400 blur-xl opacity-30 rounded-full animate-pulse group-hover:opacity-40 transition-opacity"></div>
                    <Badge className="relative bg-white/80 backdrop-blur-md border-white/20 shadow-lg hover:shadow-xl transition-all duration-300 px-6 py-2 text-blue-700 hover:scale-105">
                      <Sparkles className="w-4 h-4 mr-2" />
                      ISO 27002 Compliance Made Simple
                    </Badge>
                  </div>
                </div>

                {/* Enhanced heading with gradient text */}
                <h1 className="text-5xl md:text-6xl lg:text-7xl font-black tracking-tight mb-8 leading-[1.1]">
                  <span className="animate-fade-in block">Document Comparison for</span>
                  <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-500 bg-clip-text text-transparent animate-fade-in block" style={{ animationDelay: "0.2s" }}>
                    ISO Security Standards
                  </span>
                </h1>

                {/* Enhanced description */}
                <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-400 mb-12 max-w-3xl mx-auto leading-relaxed animate-fade-in" style={{ animationDelay: "0.4s" }}>
                  Transform your compliance workflow with AI-powered document analysis. 
                  <span className="text-blue-600 font-semibold"> Identify gaps, ensure alignment</span>, and 
                  maintain security standards effortlessly.
                </p>

                {/* Enhanced CTA buttons */}
                <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16 animate-fade-in" style={{ animationDelay: "0.6s" }}>
                  <Button 
                    size="lg" 
                    onClick={() => setSelectedView('comparison')} 
                    className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 px-8 py-4 text-lg font-semibold group"
                  >
                    Start Analysis
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                  <Button 
                    size="lg" 
                    variant="outline" 
                    onClick={() => setSelectedView('upload')}
                    className="border-2 border-slate-200 hover:border-blue-300 hover:bg-blue-50 transition-all duration-300 px-8 py-4 text-lg font-semibold"
                  >
                    <FileText className="mr-2 h-5 w-5" />
                    Upload Documents
                  </Button>
                </div>

                {/* Trust indicators */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-2xl mx-auto animate-fade-in" style={{ animationDelay: "0.8s" }}>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-slate-800">99.9%</div>
                    <div className="text-sm text-slate-600">Accuracy</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-slate-800">10k+</div>
                    <div className="text-sm text-slate-600">Documents Analyzed</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-slate-800">500+</div>
                    <div className="text-sm text-slate-600">Organizations</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-slate-800">24/7</div>
                    <div className="text-sm text-slate-600">Support</div>
                  </div>
                </div>
              </div>
            </section>

            {/* Enhanced Features Section with Cards */}
            <section id="features" className="py-20">
              <div className="text-center mb-20">
                <Badge className="mb-4 bg-blue-100 text-blue-700 border-blue-200">
                  <Zap className="w-4 h-4 mr-2" />
                  Powerful Features
                </Badge>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                  Everything You Need for Compliance
                </h2>
                <p className="text-xl text-slate-600 max-w-3xl mx-auto">
                  Our platform offers intuitive tools to analyze and compare your SOPs with ISO standards.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                <Card className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-0 bg-white/70 backdrop-blur-sm">
                  <CardContent className="p-8">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-200 w-16 h-16 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <FileText className="h-8 w-8 text-blue-600" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4 text-slate-800">AI Document Analysis</h3>
                    <p className="text-slate-600 mb-6 leading-relaxed">
                      Advanced AI algorithms automatically extract and analyze key information from both SOPs and ISO controls for comprehensive comparison.
                    </p>
                    <div className="flex items-center gap-2 text-blue-600 font-semibold group-hover:text-blue-700">
                      <span>Learn more</span>
                      <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </CardContent>
                </Card>

                <Card className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-0 bg-white/70 backdrop-blur-sm">
                  <CardContent className="p-8">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-green-100 to-green-200 w-16 h-16 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <ShieldCheck className="h-8 w-8 text-green-600" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4 text-slate-800">Smart Compliance Mapping</h3>
                    <p className="text-slate-600 mb-6 leading-relaxed">
                      Visualize how your SOPs align with ISO 27002 controls, highlighting gaps and overlaps with intelligent recommendations.
                    </p>
                    <div className="flex items-center gap-2 text-green-600 font-semibold group-hover:text-green-700">
                      <span>Learn more</span>
                      <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </CardContent>
                </Card>

                <Card className="group hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-0 bg-white/70 backdrop-blur-sm">
                  <CardContent className="p-8">
                    <div className="p-4 rounded-2xl bg-gradient-to-br from-purple-100 to-purple-200 w-16 h-16 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                      <BarChart2 className="h-8 w-8 text-purple-600" />
                    </div>
                    <h3 className="text-2xl font-bold mb-4 text-slate-800">Comprehensive Analytics</h3>
                    <p className="text-slate-600 mb-6 leading-relaxed">
                      Generate detailed reports with actionable insights, compliance scores, and prioritized recommendations for improvement.
                    </p>
                    <div className="flex items-center gap-2 text-purple-600 font-semibold group-hover:text-purple-700">
                      <span>Learn more</span>
                      <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                    </div>
                  </CardContent>
                </Card>
              </div>
            </section>

            {/* Enhanced Process Section */}
            <section id="howitworks" className="py-20">
              <div className="text-center mb-20">
                <Badge className="mb-4 bg-purple-100 text-purple-700 border-purple-200">
                  <Target className="w-4 h-4 mr-2" />
                  How It Works
                </Badge>
                <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
                  Three Steps to Compliance
                </h2>
                <p className="text-xl text-slate-600 max-w-3xl mx-auto">
                  A streamlined process designed for efficiency and accuracy.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                {[
                  {
                    step: "1",
                    title: "Upload & Configure",
                    description: "Upload your SOPs and select relevant ISO 27002 control sections. Our system supports multiple formats and provides intelligent document preprocessing.",
                    icon: <FileText className="h-6 w-6" />,
                    color: "blue"
                  },
                  {
                    step: "2", 
                    title: "AI Analysis",
                    description: "Our advanced AI engine analyzes documents side by side, identifying key differences, similarities, and compliance gaps with unprecedented accuracy.",
                    icon: <Zap className="h-6 w-6" />,
                    color: "purple"
                  },
                  {
                    step: "3",
                    title: "Actionable Results",
                    description: "Receive comprehensive compliance reports with prioritized recommendations, visual dashboards, and export capabilities for stakeholder review.",
                    icon: <Trophy className="h-6 w-6" />,
                    color: "green"
                  }
                ].map((item, index) => (
                  <div key={index} className="relative group">
                    <Card className="p-8 h-full hover:shadow-xl transition-all duration-300 border-0 bg-white/70 backdrop-blur-sm group-hover:-translate-y-1">
                      <div className={`h-16 w-16 rounded-2xl bg-gradient-to-br from-${item.color}-100 to-${item.color}-200 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform`}>
                        <div className={`text-${item.color}-600`}>
                          {item.icon}
                        </div>
                      </div>
                      <div className={`inline-flex items-center justify-center w-8 h-8 rounded-full bg-${item.color}-600 text-white font-bold text-sm mb-4`}>
                        {item.step}
                      </div>
                      <h3 className="text-xl font-bold mb-3 text-slate-800">{item.title}</h3>
                      <p className="text-slate-600 leading-relaxed">{item.description}</p>
                    </Card>
                    {index < 2 && (
                      <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2 z-10">
                        <ArrowRight className="h-6 w-6 text-slate-300" />
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="flex justify-center mt-16">
                <Button 
                  size="lg" 
                  onClick={() => setSelectedView('dashboard')}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 px-8 py-4 text-lg font-semibold"
                >
                  <BarChart2 className="mr-2 h-5 w-5" />
                  View Live Dashboard
                </Button>
              </div>
            </section>
            
            {/* Document Section */}
            <section id="documents" className="py-16">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold mb-4">Sample Documents</h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Browse through sample SOPs and ISO controls to see how the comparison works.
                </p>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <DocumentCard 
                  title="Access Control SOP" 
                  type="SOP"
                  date="Last updated: May 10, 2025"
                  excerpt="This SOP establishes requirements for controlling access to company systems and data. It covers user registration, authentication methods, password management, and access review processes."
                  onSelect={() => setSelectedView('comparison')}
                />
                
                <DocumentCard 
                  title="ISO 27002:2022 - Access Control" 
                  type="ISO"
                  date="Last updated: Mar 15, 2025"
                  excerpt="ISO/IEC 27002:2022 control for access management. Provides guidance on restricting access to information and application systems according to business and security requirements."
                  onSelect={() => setSelectedView('comparison')}
                />
                
                <DocumentCard 
                  title="Data Protection Policy" 
                  type="SOP"
                  date="Last updated: Apr 28, 2025"
                  excerpt="This policy outlines the requirements for protecting sensitive company and customer data. It includes data classification, encryption standards, and data handling procedures."
                  onSelect={() => setSelectedView('comparison')}
                />
                
                <DocumentCard 
                  title="ISO 27002:2022 - Cryptography" 
                  type="ISO"
                  date="Last updated: Feb 05, 2025"
                  excerpt="ISO/IEC 27002:2022 control for cryptography. Ensures proper and effective use of cryptography to protect the confidentiality, authenticity and/or integrity of information."
                  onSelect={() => setSelectedView('comparison')}
                />
              </div>
            </section>
          </div>
        ) : selectedView === 'comparison' ? (
          <>
            <div className="mb-8">
              <Button variant="link" onClick={() => setSelectedView('landing')} className="mb-4 -ml-3 text-muted-foreground">
                <ArrowRight className="mr-2 h-4 w-4 rotate-180" />
                Back to Home
              </Button>
              <h1 className="text-3xl font-bold">Document Comparison</h1>
              <p className="text-muted-foreground mt-2">Compare your SOPs with ISO 27002 controls.</p>
            </div>
            <ComparisonView />
          </>
        ) : selectedView === 'dashboard' ? (
          <>
            <div className="mb-8">
              <Button variant="link" onClick={() => setSelectedView('landing')} className="mb-4 -ml-3 text-muted-foreground">
                <ArrowRight className="mr-2 h-4 w-4 rotate-180" />
                Back to Home
              </Button>
              <h1 className="text-3xl font-bold">Compliance Dashboard</h1>
              <p className="text-muted-foreground mt-2">View your organization's compliance status at a glance.</p>
            </div>
            <Dashboard />
          </>
        ) : (
          <>
            <div className="mb-8">
              <Button variant="link" onClick={() => setSelectedView('landing')} className="mb-4 -ml-3 text-muted-foreground">
                <ArrowRight className="mr-2 h-4 w-4 rotate-180" />
                Back to Home
              </Button>
              <h1 className="text-3xl font-bold">Document Upload</h1>
              <p className="text-muted-foreground mt-2">Upload SOPs and ISO documents for comparison.</p>
            </div>
            <FileUploader />
          </>
        )}
      </main>
    </div>
  );
};

export default Index;
