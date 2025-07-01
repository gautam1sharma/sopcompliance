import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  FileText, 
  File, 
  ChevronRight,
  BarChart3,
  TrendingUp,
  Shield,
  Target,
  Clock,
  Users,
  Zap,
  Eye,
  Download,
  RefreshCw
} from "lucide-react";

const Dashboard: React.FC = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => setIsRefreshing(false), 2000);
  };

  return (
    <div className="w-full animate-fade-in space-y-8">
      {/* Header Section */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
            Compliance Dashboard
          </h2>
          <p className="text-slate-600 mt-2">Overview of your organization's ISO 27002 compliance status</p>
        </div>
        <div className="flex gap-3">
          <Button 
            variant="outline" 
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="hover-glow"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
          <Button className="btn-gradient">
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>
      
      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="glass-card-strong group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-0">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 mb-2">Total Documents</p>
                <div className="text-3xl font-bold text-slate-800">24</div>
                <div className="flex items-center mt-2 text-sm">
                  <TrendingUp className="h-4 w-4 text-green-500 mr-1" />
                  <span className="text-green-600">+12% from last month</span>
                </div>
              </div>
              <div className="p-3 rounded-xl bg-gradient-to-br from-blue-100 to-blue-200 group-hover:scale-110 transition-transform">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="glass-card-strong group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-0">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 mb-2">Compliance Score</p>
                <div className="text-3xl font-bold text-green-600">78%</div>
                <Progress value={78} className="mt-3 progress-glow" />
              </div>
              <div className="p-3 rounded-xl bg-gradient-to-br from-green-100 to-green-200 group-hover:scale-110 transition-transform">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="glass-card-strong group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-0">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 mb-2">Critical Issues</p>
                <div className="text-3xl font-bold text-red-500">7</div>
                <div className="flex gap-2 mt-2">
                  <Badge variant="destructive" className="text-xs">2 Critical</Badge>
                  <Badge variant="secondary" className="text-xs">5 Moderate</Badge>
                </div>
              </div>
              <div className="p-3 rounded-xl bg-gradient-to-br from-red-100 to-red-200 group-hover:scale-110 transition-transform">
                <AlertTriangle className="h-6 w-6 text-red-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card-strong group hover:shadow-2xl transition-all duration-300 hover:-translate-y-1 border-0">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600 mb-2">Last Updated</p>
                <div className="text-lg font-semibold text-slate-800">2 hours ago</div>
                <div className="flex items-center mt-2 text-sm text-slate-500">
                  <Users className="h-4 w-4 mr-1" />
                  <span>by Security Team</span>
                </div>
              </div>
              <div className="p-3 rounded-xl bg-gradient-to-br from-purple-100 to-purple-200 group-hover:scale-110 transition-transform">
                <Clock className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
      
      {/* Main Content Tabs */}
      <div className="mt-8">
        <Tabs defaultValue="compliance" className="w-full">
          <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:grid-cols-4 gap-1 bg-white/50 backdrop-blur-sm p-1 rounded-xl">
            <TabsTrigger value="compliance" className="data-[state=active]:bg-white data-[state=active]:shadow-md">
              <BarChart3 className="h-4 w-4 mr-2" />
              Compliance
            </TabsTrigger>
            <TabsTrigger value="documents" className="data-[state=active]:bg-white data-[state=active]:shadow-md">
              <FileText className="h-4 w-4 mr-2" />
              Documents
            </TabsTrigger>
            <TabsTrigger value="issues" className="data-[state=active]:bg-white data-[state=active]:shadow-md">
              <AlertTriangle className="h-4 w-4 mr-2" />
              Issues
            </TabsTrigger>
            <TabsTrigger value="analytics" className="data-[state=active]:bg-white data-[state=active]:shadow-md">
              <TrendingUp className="h-4 w-4 mr-2" />
              Analytics
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="compliance" className="mt-6 animate-fade-in">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Compliance Overview */}
              <Card className="glass-card-strong border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Target className="h-5 w-5 text-blue-600" />
                    Compliance by Control Category
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {complianceData.map((item, idx) => (
                      <div key={idx} className="staggered-fade">
                        <div className="flex justify-between items-center mb-2">
                          <div className="font-medium text-slate-700">{item.category}</div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-bold">{item.complianceRate}%</span>
                            {item.complianceRate >= 80 ? (
                              <CheckCircle className="h-4 w-4 text-green-500" />
                            ) : item.complianceRate >= 60 ? (
                              <AlertTriangle className="h-4 w-4 text-yellow-500" />
                            ) : (
                              <XCircle className="h-4 w-4 text-red-500" />
                            )}
                          </div>
                        </div>
                        <Progress 
                          value={item.complianceRate} 
                          className="h-3 progress-glow"
                        />
                        <div className="flex justify-between text-xs text-slate-500 mt-1">
                          <span>{item.compliant} compliant</span>
                          <span>{item.total} total controls</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Risk Assessment */}
              <Card className="glass-card-strong border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="h-5 w-5 text-green-600" />
                    Risk Assessment Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {riskData.map((risk, idx) => (
                      <div key={idx} className="p-4 rounded-lg border bg-white/50 staggered-fade">
                        <div className="flex items-center gap-3">
                          <div className={`p-2 rounded-full ${
                            risk.level === 'High' ? 'bg-red-100 text-red-600' :
                            risk.level === 'Medium' ? 'bg-yellow-100 text-yellow-600' :
                            'bg-green-100 text-green-600'
                          }`}>
                            <Shield className="h-4 w-4" />
                          </div>
                          <div className="flex-1">
                            <div className="font-semibold text-slate-800">{risk.category}</div>
                            <div className="text-sm text-slate-600">{risk.description}</div>
                            <Badge 
                              variant={risk.level === 'High' ? 'destructive' : 
                                     risk.level === 'Medium' ? 'default' : 'secondary'}
                              className="mt-2"
                            >
                              {risk.level} Risk
                            </Badge>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
          
          <TabsContent value="documents" className="mt-6">
            <Card className="glass-card-strong border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5 text-blue-600" />
                  Recently Updated Documents
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {recentDocuments.map((doc, idx) => (
                    <div 
                      key={idx} 
                      className="flex items-center justify-between p-4 border rounded-xl hover:bg-slate-50/50 transition-colors staggered-fade group"
                    >
                      <div className="flex items-center gap-4">
                        <div className="p-2 bg-blue-100 rounded-lg group-hover:scale-110 transition-transform">
                          <File className="h-4 w-4 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-medium text-slate-800">{doc.title}</div>
                          <div className="text-sm text-slate-500">Updated {doc.updatedTime}</div>
                          <Badge variant="outline" className="mt-1">
                            {doc.status}
                          </Badge>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <Button variant="ghost" size="sm" className="hover-glow">
                          <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon">
                          <ChevronRight className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          
          <TabsContent value="issues" className="mt-6">
            <Card className="glass-card-strong border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-red-600" />
                  Compliance Issues & Recommendations
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {complianceIssues.map((issue, idx) => (
                    <div 
                      key={idx} 
                      className="p-6 border rounded-xl bg-white/50 staggered-fade hover:shadow-md transition-all"
                    >
                      <div className="flex items-start gap-4">
                        <div className={`mt-1 p-2 rounded-full ${
                          issue.severity === 'critical' ? 'bg-red-100 text-red-600' : 
                          issue.severity === 'moderate' ? 'bg-yellow-100 text-yellow-600' : 
                          'bg-blue-100 text-blue-600'
                        }`}>
                          {issue.severity === 'critical' ? <XCircle className="h-5 w-5" /> : 
                           issue.severity === 'moderate' ? <AlertTriangle className="h-5 w-5" /> : 
                           <BarChart3 className="h-5 w-5" />}
                        </div>
                        <div className="flex-1">
                          <div className="font-semibold text-lg text-slate-800 mb-2">{issue.title}</div>
                          <div className="text-slate-600 mb-4">{issue.description}</div>
                          <div className="flex items-center gap-4 mb-4">
                            <Badge variant="outline">{issue.document}</Badge>
                            <span className="text-sm text-slate-500">Identified {issue.date}</span>
                          </div>
                          <div className="bg-blue-50 p-4 rounded-lg">
                            <div className="text-sm font-medium text-blue-800 mb-2">Recommended Action:</div>
                            <div className="text-sm text-blue-700">{issue.recommendation}</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="mt-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card className="glass-card-strong border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    Compliance Trends
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="text-center p-8 border-2 border-dashed border-slate-300 rounded-lg">
                      <BarChart3 className="h-12 w-12 text-slate-400 mx-auto mb-4" />
                      <p className="text-slate-500">Interactive charts coming soon...</p>
                      <p className="text-sm text-slate-400 mt-2">
                        This will show compliance trends over time
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="glass-card-strong border-0">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-purple-600" />
                    Performance Metrics
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {performanceMetrics.map((metric, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-white/50 rounded-lg staggered-fade">
                        <div>
                          <div className="font-medium text-slate-800">{metric.name}</div>
                          <div className="text-sm text-slate-500">{metric.description}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-slate-800">{metric.value}</div>
                          <div className="text-sm text-slate-500">{metric.unit}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

// Enhanced data with more realistic values
const complianceData = [
  { category: "Access Control", complianceRate: 92, compliant: 23, total: 25 },
  { category: "Cryptography", complianceRate: 85, compliant: 17, total: 20 },
  { category: "Physical Security", complianceRate: 76, compliant: 19, total: 25 },
  { category: "Operations Security", complianceRate: 64, compliant: 16, total: 25 },
  { category: "Communications Security", complianceRate: 83, compliant: 20, total: 24 },
];

const recentDocuments = [
  { 
    title: "Access Control Policy v2.1", 
    updatedTime: "2 hours ago", 
    status: "Compliant" 
  },
  { 
    title: "Data Protection Guidelines", 
    updatedTime: "1 day ago", 
    status: "Needs Review" 
  },
  { 
    title: "Network Security Standards", 
    updatedTime: "3 days ago", 
    status: "Compliant" 
  },
  { 
    title: "Incident Response Plan", 
    updatedTime: "1 week ago", 
    status: "Non-Compliant" 
  }
];

const complianceIssues = [
  {
    title: "Missing Password Complexity Requirements",
    description: "The current access control policy does not specify minimum password complexity requirements as outlined in ISO 27002 control 9.4.3.",
    document: "Access Control Policy",
    date: "2 days ago",
    severity: "critical",
    recommendation: "Update the access control policy to include specific password complexity requirements including minimum length, character sets, and expiration policies."
  },
  {
    title: "Incomplete Asset Inventory",
    description: "Several IT assets are not properly documented in the asset management system, creating potential security gaps.",
    document: "Asset Management Register",
    date: "5 days ago",
    severity: "moderate",
    recommendation: "Conduct a comprehensive audit of all IT assets and update the asset inventory to include missing items with proper classification."
  },
  {
    title: "Backup Recovery Testing",
    description: "Business continuity plans lack recent backup recovery testing documentation.",
    document: "Business Continuity Plan",
    date: "1 week ago",
    severity: "moderate",
    recommendation: "Schedule quarterly backup recovery tests and document the results to ensure business continuity capabilities."
  }
];

const riskData = [
  {
    category: "Data Protection",
    level: "High",
    description: "Inadequate encryption for sensitive data at rest"
  },
  {
    category: "Access Management",
    level: "Medium", 
    description: "Incomplete privilege access reviews"
  },
  {
    category: "Network Security",
    level: "Low",
    description: "Minor firewall configuration gaps"
  }
];

const performanceMetrics = [
  {
    name: "Avg. Analysis Time",
    value: "2.3",
    unit: "minutes",
    description: "Time to analyze documents"
  },
  {
    name: "Detection Accuracy",
    value: "94.7",
    unit: "%",
    description: "Compliance gap detection rate"
  },
  {
    name: "Process Efficiency",
    value: "87",
    unit: "score",
    description: "Overall process optimization"
  }
];

export default Dashboard;
