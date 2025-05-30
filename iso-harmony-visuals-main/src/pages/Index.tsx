
import React, { useState } from 'react';
import Navbar from '@/components/Navbar';
import AnimatedBackground from '@/components/AnimatedBackground';
import DocumentCard from '@/components/DocumentCard';
import ComparisonView from '@/components/ComparisonView';
import Dashboard from '@/components/Dashboard';
import FileUploader from '@/components/FileUploader';
import { Button } from '@/components/ui/button';
import { ArrowRight, FileText, ShieldCheck, BarChart2 } from 'lucide-react';

const Index = () => {
  const [selectedView, setSelectedView] = useState<'landing' | 'comparison' | 'dashboard' | 'upload'>('landing');

  return (
    <div className="min-h-screen flex flex-col">
      <AnimatedBackground />
      <Navbar />

      <main className="flex-1 container py-8">
        {selectedView === 'landing' ? (
          <div className="space-y-20">
            {/* Hero Section */}
            <section className="py-20">
              <div className="max-w-3xl mx-auto text-center">
                <div className="mb-6 inline-block">
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-blue-400 blur-lg opacity-20 rounded-full animate-pulse"></div>
                    <span className="relative bg-clip-text text-transparent bg-gradient-to-r from-blue-800 to-blue-500 dark:from-blue-400 dark:to-blue-200 text-sm font-medium px-4 py-1.5 rounded-full border border-blue-100 dark:border-blue-800">
                      ISO 27002 Compliance Made Simple
                    </span>
                  </div>
                </div>
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight mb-6 animate-fade-in">
                  Document Comparison for{' '}
                  <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-800 to-blue-500 dark:from-blue-400 dark:to-blue-200">
                    ISO Security Standards
                  </span>
                </h1>
                <p className="text-lg md:text-xl text-slate-600 dark:text-slate-400 mb-10 animate-fade-in" style={{ animationDelay: "0.1s" }}>
                  Compare your SOPs to ISO 27002 controls with powerful visualization tools. 
                  Identify compliance gaps and ensure alignment with security standards.
                </p>
                <div className="flex flex-wrap justify-center gap-4 animate-fade-in" style={{ animationDelay: "0.2s" }}>
                  <Button size="lg" onClick={() => setSelectedView('comparison')} className="animate-fade-in">
                    Get Started <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                  <Button size="lg" variant="outline" onClick={() => setSelectedView('upload')}>
                    Upload Documents
                  </Button>
                </div>
              </div>
            </section>

            {/* Features Section */}
            <section id="features" className="py-16">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold mb-4">Powerful Comparison Features</h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Our platform offers intuitive tools to analyze and compare your SOPs with ISO standards.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="document-card staggered-fade flex flex-col">
                  <div className="p-4 rounded-full bg-blue-50 w-16 h-16 flex items-center justify-center mb-6 dark:bg-blue-900/20">
                    <FileText className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <h3 className="text-xl font-bold mb-3">Document Analysis</h3>
                  <p className="text-muted-foreground flex-grow">
                    Automatically extract key information from both SOPs and ISO controls for easy comparison.
                  </p>
                  <Button variant="link" className="mt-4 p-0 justify-start">
                    Learn more <ArrowRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>

                <div className="document-card staggered-fade flex flex-col">
                  <div className="p-4 rounded-full bg-green-50 w-16 h-16 flex items-center justify-center mb-6 dark:bg-green-900/20">
                    <ShieldCheck className="h-8 w-8 text-green-600 dark:text-green-400" />
                  </div>
                  <h3 className="text-xl font-bold mb-3">Compliance Mapping</h3>
                  <p className="text-muted-foreground flex-grow">
                    Visualize how your SOPs align with ISO 27002 controls, highlighting gaps and overlaps.
                  </p>
                  <Button variant="link" className="mt-4 p-0 justify-start">
                    Learn more <ArrowRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>

                <div className="document-card staggered-fade flex flex-col">
                  <div className="p-4 rounded-full bg-amber-50 w-16 h-16 flex items-center justify-center mb-6 dark:bg-amber-900/20">
                    <BarChart2 className="h-8 w-8 text-amber-600 dark:text-amber-400" />
                  </div>
                  <h3 className="text-xl font-bold mb-3">Gap Analysis</h3>
                  <p className="text-muted-foreground flex-grow">
                    Generate detailed reports showing compliance status and recommendations for improvement.
                  </p>
                  <Button variant="link" className="mt-4 p-0 justify-start">
                    Learn more <ArrowRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>
              </div>
            </section>

            {/* How It Works Section */}
            <section id="howitworks" className="py-16">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold mb-4">How It Works</h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  A simple three-step process to ensure your documents comply with ISO standards.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                <div className="relative">
                  <div className="staggered-fade relative z-10">
                    <div className="bg-white dark:bg-slate-800 border rounded-xl p-6 shadow-sm">
                      <div className="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
                        <span className="text-xl font-bold text-blue-600 dark:text-blue-400">1</span>
                      </div>
                      <h3 className="text-xl font-medium mb-2">Upload Documents</h3>
                      <p className="text-muted-foreground">
                        Upload your SOPs and select the ISO 27002 control sections for comparison.
                      </p>
                    </div>
                  </div>
                  <div className="absolute top-1/2 left-full h-0.5 w-8 bg-blue-200 dark:bg-blue-800 hidden md:block"></div>
                </div>

                <div className="relative">
                  <div className="staggered-fade relative z-10">
                    <div className="bg-white dark:bg-slate-800 border rounded-xl p-6 shadow-sm">
                      <div className="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
                        <span className="text-xl font-bold text-blue-600 dark:text-blue-400">2</span>
                      </div>
                      <h3 className="text-xl font-medium mb-2">Compare Documents</h3>
                      <p className="text-muted-foreground">
                        Our system analyzes the documents side by side, highlighting key differences.
                      </p>
                    </div>
                  </div>
                  <div className="absolute top-1/2 left-full h-0.5 w-8 bg-blue-200 dark:bg-blue-800 hidden md:block"></div>
                </div>

                <div className="relative">
                  <div className="staggered-fade relative z-10">
                    <div className="bg-white dark:bg-slate-800 border rounded-xl p-6 shadow-sm">
                      <div className="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-4">
                        <span className="text-xl font-bold text-blue-600 dark:text-blue-400">3</span>
                      </div>
                      <h3 className="text-xl font-medium mb-2">Review Results</h3>
                      <p className="text-muted-foreground">
                        Generate compliance reports with actionable recommendations for improvement.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-center mt-16 animate-fade-in">
                <Button size="lg" onClick={() => setSelectedView('dashboard')}>
                  View Example Dashboard
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
