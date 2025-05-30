
import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { 
  CheckCircle, 
  XCircle, 
  HelpCircle, 
  FileText, 
  File, 
  ChevronRight,
  BarChart3
} from "lucide-react";

const Dashboard: React.FC = () => {
  return (
    <div className="w-full animate-fade-in">
      <h2 className="text-2xl font-bold mb-6">Compliance Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Summary Cards */}
        <Card className="staggered-fade">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Documents
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-3xl font-bold">24</div>
              <div className="p-2 bg-blue-50 dark:bg-blue-900/30 rounded-full">
                <FileText className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              12 SOPs, 12 ISO Controls
            </p>
          </CardContent>
        </Card>
        
        <Card className="staggered-fade">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Compliance Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-3xl font-bold text-green-500">78%</div>
              <div className="p-2 bg-green-50 dark:bg-green-900/30 rounded-full">
                <CheckCircle className="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
            </div>
            <Progress value={78} className="mt-2" />
          </CardContent>
        </Card>
        
        <Card className="staggered-fade">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Non-Compliance Issues
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="text-3xl font-bold text-red-500">7</div>
              <div className="p-2 bg-red-50 dark:bg-red-900/30 rounded-full">
                <XCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
              </div>
            </div>
            <div className="flex items-center gap-3 mt-2">
              <div className="flex items-center gap-1 text-xs">
                <span className="h-2 w-2 bg-red-500 rounded-full"></span>
                <span>Critical: 2</span>
              </div>
              <div className="flex items-center gap-1 text-xs">
                <span className="h-2 w-2 bg-amber-500 rounded-full"></span>
                <span>Moderate: 5</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      <div className="mt-8">
        <Tabs defaultValue="compliance" className="w-full">
          <TabsList>
            <TabsTrigger value="compliance">Compliance Overview</TabsTrigger>
            <TabsTrigger value="documents">Recent Documents</TabsTrigger>
            <TabsTrigger value="issues">Issues</TabsTrigger>
          </TabsList>
          
          <TabsContent value="compliance" className="mt-6 animate-fade-in">
            <Card>
              <CardHeader>
                <CardTitle>Compliance by Control Category</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complianceData.map((item, idx) => (
                    <div key={idx} className="staggered-fade">
                      <div className="flex justify-between items-center mb-1">
                        <div className="text-sm font-medium">{item.category}</div>
                        <div className="text-sm font-medium">{item.complianceRate}%</div>
                      </div>
                      <Progress value={item.complianceRate} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="documents" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Recently Updated Documents</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentDocuments.map((doc, idx) => (
                    <div 
                      key={idx} 
                      className="flex items-center justify-between p-3 border rounded-md hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors staggered-fade"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-1.5 bg-blue-50 dark:bg-blue-900/30 rounded">
                          <File className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                        </div>
                        <div>
                          <div className="text-sm font-medium">{doc.title}</div>
                          <div className="text-xs text-muted-foreground">Updated {doc.updatedTime}</div>
                        </div>
                      </div>
                      <Button variant="ghost" size="icon">
                        <ChevronRight className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="issues" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Compliance Issues</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complianceIssues.map((issue, idx) => (
                    <div 
                      key={idx} 
                      className="p-4 border rounded-lg staggered-fade"
                    >
                      <div className="flex items-start gap-3">
                        <div className={`mt-0.5 ${
                          issue.severity === 'critical' ? 'text-red-500' : 
                          issue.severity === 'moderate' ? 'text-amber-500' : 
                          'text-blue-500'
                        }`}>
                          {issue.severity === 'critical' ? <XCircle className="h-5 w-5" /> : 
                           issue.severity === 'moderate' ? <HelpCircle className="h-5 w-5" /> : 
                           <BarChart3 className="h-5 w-5" />}
                        </div>
                        <div>
                          <div className="font-medium">{issue.title}</div>
                          <div className="text-sm text-muted-foreground mt-1">{issue.description}</div>
                          <div className="flex items-center gap-4 mt-3">
                            <div className="text-xs px-2 py-0.5 rounded bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                              {issue.document}
                            </div>
                            <div className="text-xs text-muted-foreground">
                              Identified {issue.date}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

const complianceData = [
  { category: "Access Control", complianceRate: 92 },
  { category: "Cryptography", complianceRate: 85 },
  { category: "Physical Security", complianceRate: 76 },
  { category: "Operations Security", complianceRate: 64 },
  { category: "Communications Security", complianceRate: 83 },
];

const recentDocuments = [
  { title: "Data Protection & Privacy SOP", updatedTime: "2 hours ago" },
  { title: "ISO 27002 - Information Security Controls", updatedTime: "1 day ago" },
  { title: "System Access Control Procedure", updatedTime: "3 days ago" },
  { title: "Incident Response Plan", updatedTime: "1 week ago" },
];

const complianceIssues = [
  { 
    title: "Missing Backup Verification Process", 
    description: "ISO 27002 requires regular testing of backups, but the current SOP does not include a verification procedure.",
    severity: "critical",
    document: "Backup Management SOP",
    date: "3 days ago"
  },
  { 
    title: "Outdated Encryption Standards", 
    description: "Current encryption methods do not meet the minimum requirements specified in ISO 27002:2022.",
    severity: "critical",
    document: "Data Encryption SOP",
    date: "1 week ago"
  },
  { 
    title: "Incomplete Access Review Process", 
    description: "Access reviews are performed annually, but ISO 27002 recommends quarterly reviews for sensitive systems.",
    severity: "moderate",
    document: "Access Management SOP",
    date: "2 weeks ago"
  },
];

export default Dashboard;
