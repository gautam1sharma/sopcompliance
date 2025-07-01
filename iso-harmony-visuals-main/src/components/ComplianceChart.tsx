import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  LineChart, Line, Area, AreaChart
} from 'recharts';
import { 
  BarChart3, PieChart as PieIcon, Radar as RadarIcon, TrendingUp,
  Download, Maximize2, RefreshCw, Filter, Eye
} from "lucide-react";

const ComplianceChart: React.FC = () => {
  const [activeChart, setActiveChart] = useState<'bar' | 'pie' | 'radar' | 'trend'>('bar');
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Enhanced mock data for visualizations
  const complianceData = [
    { category: "Access Control", score: 85, total: 14, compliant: 12, target: 90 },
    { category: "Asset Management", score: 78, total: 10, compliant: 8, target: 85 },
    { category: "Cryptography", score: 92, total: 8, compliant: 7, target: 95 },
    { category: "Physical Security", score: 88, total: 15, compliant: 13, target: 90 },
    { category: "Operations Security", score: 74, total: 13, compliant: 10, target: 80 },
    { category: "Communications Security", score: 81, total: 7, compliant: 6, target: 85 },
    { category: "System Acquisition", score: 76, total: 11, compliant: 8, target: 85 },
    { category: "Supplier Relationships", score: 69, total: 5, compliant: 3, target: 75 },
    { category: "Incident Management", score: 95, total: 7, compliant: 7, target: 95 },
    { category: "Business Continuity", score: 83, total: 6, compliant: 5, target: 90 }
  ];

  const trendData = [
    { month: "Jan", score: 65, target: 75, incidents: 12 },
    { month: "Feb", score: 68, target: 75, incidents: 10 },
    { month: "Mar", score: 72, target: 80, incidents: 8 },
    { month: "Apr", score: 75, target: 80, incidents: 6 },
    { month: "May", score: 78, target: 85, incidents: 5 },
    { month: "Jun", score: 81, target: 85, incidents: 4 }
  ];

  const riskData = [
    { subject: "Confidentiality", A: 85, B: 90, fullMark: 100 },
    { subject: "Integrity", A: 78, B: 85, fullMark: 100 },
    { subject: "Availability", A: 92, B: 95, fullMark: 100 },
    { subject: "Authentication", A: 88, B: 90, fullMark: 100 },
    { subject: "Authorization", A: 74, B: 80, fullMark: 100 },
    { subject: "Non-repudiation", A: 81, B: 85, fullMark: 100 }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-card-strong p-4 border-0 shadow-xl">
          <p className="font-semibold text-slate-800">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value}
              {entry.name === 'score' && '%'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const getInsights = () => {
    const avgScore = complianceData.reduce((sum, item) => sum + item.score, 0) / complianceData.length;
    const highPerformers = complianceData.filter(item => item.score >= 85).length;
    const needsAttention = complianceData.filter(item => item.score < 75).length;
    
    return {
      avgScore: Math.round(avgScore),
      highPerformers,
      needsAttention,
      trend: trendData[trendData.length - 1].score > trendData[0].score ? 'improving' : 'declining'
    };
  };

  const insights = getInsights();

  return (
    <div className={`w-full animate-fade-in ${isFullscreen ? 'fixed inset-0 z-50 bg-white p-6' : ''}`}>
      <Card className="glass-card-strong border-0 h-full">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="flex items-center gap-2 text-2xl">
                <BarChart3 className="h-6 w-6 text-blue-600" />
                Compliance Analytics
              </CardTitle>
              <p className="text-slate-600 mt-1">Interactive compliance data visualization</p>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" className="hover-glow">
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </Button>
              <Button variant="outline" size="sm" className="hover-glow">
                <Download className="h-4 w-4 mr-2" />
                Export
              </Button>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="hover-glow"
              >
                <Maximize2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          {/* Insights Summary */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="text-center p-4 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200">
              <div className="text-2xl font-bold text-blue-600">{insights.avgScore}%</div>
              <div className="text-sm text-slate-600">Average Score</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-gradient-to-br from-green-50 to-green-100 border border-green-200">
              <div className="text-2xl font-bold text-green-600">{insights.highPerformers}</div>
              <div className="text-sm text-slate-600">High Performers</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-gradient-to-br from-orange-50 to-orange-100 border border-orange-200">
              <div className="text-2xl font-bold text-orange-600">{insights.needsAttention}</div>
              <div className="text-sm text-slate-600">Need Attention</div>
            </div>
            <div className="text-center p-4 rounded-xl bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200">
              <div className="flex items-center justify-center gap-1">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                <span className="text-lg font-bold text-purple-600 capitalize">{insights.trend}</span>
              </div>
              <div className="text-sm text-slate-600">Trend</div>
            </div>
          </div>

          {/* Chart Type Selector */}
          <Tabs value={activeChart} onValueChange={(value: any) => setActiveChart(value)} className="w-full">
            <TabsList className="grid w-full grid-cols-4 mb-6 bg-white/50 backdrop-blur-sm">
              <TabsTrigger value="bar" className="flex items-center gap-2">
                <BarChart3 className="h-4 w-4" />
                Bar Chart
              </TabsTrigger>
              <TabsTrigger value="pie" className="flex items-center gap-2">
                <PieIcon className="h-4 w-4" />
                Distribution
              </TabsTrigger>
              <TabsTrigger value="radar" className="flex items-center gap-2">
                <RadarIcon className="h-4 w-4" />
                Risk Profile
              </TabsTrigger>
              <TabsTrigger value="trend" className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                Trends
              </TabsTrigger>
            </TabsList>

            <TabsContent value="bar" className="mt-6">
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={complianceData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="category" 
                      angle={-45}
                      textAnchor="end"
                      height={100}
                      fontSize={12}
                    />
                    <YAxis />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="score" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="target" fill="#e2e8f0" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>

            <TabsContent value="pie" className="mt-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="h-96">
                  <h3 className="text-lg font-semibold mb-4 text-center">Compliance Distribution</h3>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={complianceData}
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        fill="#8884d8"
                        dataKey="score"
                        label={({ name, value }) => `${name}: ${value}%`}
                      >
                        {complianceData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip content={<CustomTooltip />} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-3">
                  <h3 className="text-lg font-semibold mb-4">Category Breakdown</h3>
                  {complianceData.map((item, index) => (
                    <div key={item.category} className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                      <div className="flex items-center gap-3">
                        <div 
                          className="w-4 h-4 rounded" 
                          style={{ backgroundColor: COLORS[index % COLORS.length] }}
                        />
                        <span className="font-medium">{item.category}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Badge variant={item.score >= 85 ? "default" : item.score >= 75 ? "secondary" : "destructive"}>
                          {item.score}%
                        </Badge>
                        <span className="text-sm text-slate-500">{item.compliant}/{item.total}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </TabsContent>

            <TabsContent value="radar" className="mt-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-4 text-center">Security Risk Assessment</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={riskData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    <Radar
                      name="Current"
                      dataKey="A"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                    <Radar
                      name="Target"
                      dataKey="B"
                      stroke="#10b981"
                      fill="#10b981"
                      fillOpacity={0.1}
                      strokeWidth={2}
                    />
                    <Tooltip content={<CustomTooltip />} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>

            <TabsContent value="trend" className="mt-6">
              <div className="h-96">
                <h3 className="text-lg font-semibold mb-4 text-center">Compliance Trends Over Time</h3>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip content={<CustomTooltip />} />
                    <Area
                      type="monotone"
                      dataKey="score"
                      stroke="#3b82f6"
                      fill="url(#colorScore)"
                      strokeWidth={3}
                    />
                    <Line
                      type="monotone"
                      dataKey="target"
                      stroke="#10b981"
                      strokeWidth={2}
                      strokeDasharray="5 5"
                    />
                    <defs>
                      <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                      </linearGradient>
                    </defs>
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  );
};

export default ComplianceChart; 