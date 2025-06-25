
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import { Search, Filter, ChevronLeft, ChevronRight, CheckCircle, XCircle, HelpCircle } from "lucide-react";

interface ComparisonViewProps {
  sopDocument?: any;
  isoDocument?: any;
}

const ComparisonView: React.FC<ComparisonViewProps> = ({
  sopDocument = { title: "Security Access Control SOP", content: sampleSopContent },
  isoDocument = { title: "ISO 27002:2022 - Access Control", content: sampleIsoContent }
}) => {
  const [currentSection, setCurrentSection] = useState(0);
  const [viewMode, setViewMode] = useState<'side-by-side' | 'differences'>('side-by-side');

  return (
    <div className="w-full bg-white dark:bg-slate-900 rounded-xl shadow-lg border border-slate-100 dark:border-slate-800 overflow-hidden animate-fade-in">
      <div className="bg-slate-50 dark:bg-slate-900 p-4 border-b border-slate-100 dark:border-slate-800">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Document Comparison</h2>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" className="flex items-center gap-1">
              <Filter className="h-4 w-4" />
              <span>Filters</span>
            </Button>
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <input
                type="search"
                placeholder="Search in documents..."
                className="pl-8 h-9 rounded-md border border-input bg-background px-3 py-1 text-sm w-[200px] lg:w-[300px]"
              />
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4 mt-4">
          <div className="text-sm font-medium text-muted-foreground flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-blue-500"></div>
            <span>{sopDocument.title}</span>
          </div>
          <Separator orientation="vertical" className="h-4" />
          <div className="text-sm font-medium text-muted-foreground flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-purple-500"></div>
            <span>{isoDocument.title}</span>
          </div>
          <div className="ml-auto">
            <Tabs defaultValue="side-by-side" className="w-[400px]">
              <TabsList>
                <TabsTrigger
                  value="side-by-side"
                  onClick={() => setViewMode('side-by-side')}
                  className="flex items-center gap-1"
                >
                  <span>Side by side</span>
                </TabsTrigger>
                <TabsTrigger
                  value="differences"
                  onClick={() => setViewMode('differences')}
                  className="flex items-center gap-1"
                >
                  <span>Show differences</span>
                </TabsTrigger>
              </TabsList>
            </Tabs>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-0 h-[600px] overflow-hidden">
        {viewMode === 'side-by-side' ? (
          <>
            <div className="border-r border-slate-100 dark:border-slate-800 p-6 overflow-y-auto">
              <h3 className="text-lg font-medium mb-4 animate-slide-in-left">SOP Document</h3>
              <div className="prose dark:prose-invert max-w-none text-sm">
                {sopDocument.content.map((paragraph: string, idx: number) => (
                  <div
                    key={idx}
                    className="mb-4 animate-slide-in-left"
                    style={{ animationDelay: `${idx * 0.05}s` }}
                  >
                    {paragraph}
                  </div>
                ))}
              </div>
            </div>

            <div className="p-6 overflow-y-auto">
              <h3 className="text-lg font-medium mb-4 animate-slide-in-right">ISO 27002 Control</h3>
              <div className="prose dark:prose-invert max-w-none text-sm">
                {isoDocument.content.map((paragraph: string, idx: number) => (
                  <div
                    key={idx}
                    className="mb-4 animate-slide-in-right"
                    style={{ animationDelay: `${idx * 0.05}s` }}
                  >
                    {paragraph}
                  </div>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="col-span-2 p-6 overflow-y-auto">
            <div className="prose dark:prose-invert max-w-none">
              {differenceContent.map((item, idx) => (
                <Card key={idx} className="mb-4 p-4 animate-fade-in" style={{ animationDelay: `${idx * 0.1}s` }}>
                  <div className="flex items-start gap-3">
                    <div className={`mt-1 ${item.status === 'high-confidence' ? 'text-green-500' :
                        item.status === 'medium-confidence' ? 'text-yellow-500' :
                          item.status === 'low-confidence' ? 'text-orange-500' :
                            item.status === 'non-compliant' ? 'text-red-500' : 'text-amber-500'}`}>
                      {item.status === 'high-confidence' ? <CheckCircle className="h-5 w-5" /> :
                        item.status === 'medium-confidence' ? <CheckCircle className="h-5 w-5" /> :
                          item.status === 'low-confidence' ? <HelpCircle className="h-5 w-5" /> :
                            item.status === 'non-compliant' ? <XCircle className="h-5 w-5" /> :
                              <HelpCircle className="h-5 w-5" />}
                    </div>
                    <div>
                      <h4 className="text-base font-medium mb-2">{item.title}</h4>
                      <div className="text-sm text-muted-foreground">{item.description}</div>
                      {item.comparison && (
                        <div className="mt-3 grid grid-cols-2 gap-4 pt-3 border-t border-slate-100 dark:border-slate-800">
                          <div>
                            <div className="text-xs font-medium mb-1 text-blue-500">SOP</div>
                            <div className="text-sm">{item.comparison.sop}</div>
                          </div>
                          <div>
                            <div className="text-xs font-medium mb-1 text-purple-500">ISO Control</div>
                            <div className="text-sm">{item.comparison.iso}</div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="bg-slate-50 dark:bg-slate-900 p-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <ChevronLeft className="h-4 w-4" />
          <span>Previous</span>
        </Button>
        <div className="text-sm text-muted-foreground">
          Section {currentSection + 1} of 5
        </div>
        <Button variant="outline" size="sm" className="flex items-center gap-1">
          <span>Next</span>
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
};

// Sample data
const sampleSopContent = [
  "1. Purpose: This Standard Operating Procedure (SOP) establishes the requirements and procedures for controlling access to company information systems and data.",
  "2. Scope: This SOP applies to all employees, contractors, consultants, temporary and other workers at [Company Name] and its subsidiaries.",
  "3. Procedures:",
  "3.1 Access Control Policy: Access to all company computing systems must be controlled. Access must be granted based on the principle of least privilege and business need-to-know.",
  "3.2 User Registration: All users must have a unique identifier (user ID) for their personal and sole use. Shared IDs are prohibited except in special circumstances when approved by the Information Security Manager.",
  "3.3 Password Management: Users must follow the company password policy which requires complex passwords changed every 90 days.",
  "3.4 Review of Access Rights: Managers must review their team members' access rights quarterly."
];

const sampleIsoContent = [
  "ISO/IEC 27002:2022 - Access Control",
  "Control 5.15: Information access should be restricted in accordance with the access control policy.",
  "Implementation guidance:",
  "a) access to information and application system functions should be restricted in accordance with the access control policy;",
  "b) providing users with the minimum necessary rights to systems, information and services to perform their role;",
  "c) ensuring appropriate authentication mechanisms are applied to control access by remote users;",
  "d) controlling the access to system utility programs capable of overriding system and application controls;",
  "e) reviewing access rights to systems, information and services on a regular basis and after any changes to access requirements."
];

const differenceContent = [
  {
    title: "Least Privilege Principle",
    description: "Both documents enforce the principle of least privilege, granting only necessary access.",
    status: "compliant",
    comparison: {
      sop: "Access must be granted based on the principle of least privilege and business need-to-know.",
      iso: "providing users with the minimum necessary rights to systems, information and services to perform their role;"
    }
  },
  {
    title: "Regular Access Review",
    description: "Both require periodic review of access rights, but with different timeframes.",
    status: "partially-compliant",
    comparison: {
      sop: "Managers must review their team members' access rights quarterly.",
      iso: "reviewing access rights to systems, information and services on a regular basis and after any changes."
    }
  },
  {
    title: "System Utility Controls",
    description: "ISO standard requires controls for system utilities, but SOP doesn't address this.",
    status: "non-compliant",
    comparison: {
      sop: "No specific mention of system utility controls in the SOP.",
      iso: "controlling the access to system utility programs capable of overriding system and application controls;"
    }
  }
];

export default ComparisonView;
