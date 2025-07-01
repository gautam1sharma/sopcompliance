import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Area, AreaChart, Tooltip } from 'recharts';
import { 
  Activity, Zap, Database, Clock, Cpu, HardDrive, 
  Wifi, AlertCircle, CheckCircle, TrendingUp
} from "lucide-react";

interface PerformanceMetrics {
  timestamp: number;
  cpuUsage: number;
  memoryUsage: number;
  analysisSpeed: number;
  responseTime: number;
  activeUsers: number;
  documentsProcessed: number;
}

const PerformanceMonitor: React.FC = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics[]>([]);
  const [currentMetrics, setCurrentMetrics] = useState<PerformanceMetrics>({
    timestamp: Date.now(),
    cpuUsage: 0,
    memoryUsage: 0,
    analysisSpeed: 0,
    responseTime: 0,
    activeUsers: 0,
    documentsProcessed: 0
  });
  const [isMonitoring, setIsMonitoring] = useState(true);

  // Simulate real-time metrics
  useEffect(() => {
    if (!isMonitoring) return;

    const interval = setInterval(() => {
      const newMetric: PerformanceMetrics = {
        timestamp: Date.now(),
        cpuUsage: 30 + Math.random() * 40, // 30-70%
        memoryUsage: 40 + Math.random() * 30, // 40-70%
        analysisSpeed: 80 + Math.random() * 20, // 80-100 docs/min
        responseTime: 200 + Math.random() * 300, // 200-500ms
        activeUsers: 15 + Math.floor(Math.random() * 10), // 15-25 users
        documentsProcessed: Math.floor(Math.random() * 5) // 0-5 per interval
      };

      setCurrentMetrics(newMetric);
      setMetrics(prev => {
        const updated = [...prev, newMetric];
        return updated.slice(-20); // Keep last 20 data points
      });
    }, 2000);

    return () => clearInterval(interval);
  }, [isMonitoring]);

  const getStatusColor = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return 'text-red-500';
    if (value >= thresholds.warning) return 'text-yellow-500';
    return 'text-green-500';
  };

  const getStatusIcon = (value: number, thresholds: { warning: number; critical: number }) => {
    if (value >= thresholds.critical) return <AlertCircle className="h-4 w-4 text-red-500" />;
    if (value >= thresholds.warning) return <AlertCircle className="h-4 w-4 text-yellow-500" />;
    return <CheckCircle className="h-4 w-4 text-green-500" />;
  };

  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-card-strong p-3 border-0 shadow-xl">
          <p className="text-sm font-medium">{formatTime(label)}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}
              {entry.name.includes('Usage') && '%'}
              {entry.name.includes('Time') && 'ms'}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-2xl font-bold text-slate-800">System Performance</h3>
          <p className="text-slate-600">Real-time monitoring dashboard</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2">
            <div className={`h-2 w-2 rounded-full ${isMonitoring ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`} />
            <span className="text-sm text-slate-600">
              {isMonitoring ? 'Live' : 'Paused'}
            </span>
          </div>
          <Badge variant="outline" className="text-xs">
            Updated {formatTime(currentMetrics.timestamp)}
          </Badge>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* CPU Usage */}
        <Card className="glass-card-strong border-0 hover:shadow-lg transition-all duration-300">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-gradient-to-br from-blue-100 to-blue-200">
                  <Cpu className="h-4 w-4 text-blue-600" />
                </div>
                <span className="text-sm font-medium text-slate-700">CPU Usage</span>
              </div>
              {getStatusIcon(currentMetrics.cpuUsage, { warning: 60, critical: 80 })}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className={`text-2xl font-bold ${getStatusColor(currentMetrics.cpuUsage, { warning: 60, critical: 80 })}`}>
                  {currentMetrics.cpuUsage.toFixed(1)}%
                </span>
              </div>
              <Progress value={currentMetrics.cpuUsage} className="h-2" />
            </div>
          </CardContent>
        </Card>

        {/* Memory Usage */}
        <Card className="glass-card-strong border-0 hover:shadow-lg transition-all duration-300">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-gradient-to-br from-purple-100 to-purple-200">
                  <HardDrive className="h-4 w-4 text-purple-600" />
                </div>
                <span className="text-sm font-medium text-slate-700">Memory</span>
              </div>
              {getStatusIcon(currentMetrics.memoryUsage, { warning: 70, critical: 85 })}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className={`text-2xl font-bold ${getStatusColor(currentMetrics.memoryUsage, { warning: 70, critical: 85 })}`}>
                  {currentMetrics.memoryUsage.toFixed(1)}%
                </span>
              </div>
              <Progress value={currentMetrics.memoryUsage} className="h-2" />
            </div>
          </CardContent>
        </Card>

        {/* Response Time */}
        <Card className="glass-card-strong border-0 hover:shadow-lg transition-all duration-300">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-gradient-to-br from-green-100 to-green-200">
                  <Clock className="h-4 w-4 text-green-600" />
                </div>
                <span className="text-sm font-medium text-slate-700">Response</span>
              </div>
              {getStatusIcon(currentMetrics.responseTime, { warning: 400, critical: 600 })}
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className={`text-2xl font-bold ${getStatusColor(currentMetrics.responseTime, { warning: 400, critical: 600 })}`}>
                  {currentMetrics.responseTime.toFixed(0)}ms
                </span>
              </div>
              <div className="text-xs text-slate-500">
                Avg. API response time
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Active Users */}
        <Card className="glass-card-strong border-0 hover:shadow-lg transition-all duration-300">
          <CardContent className="p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 rounded-lg bg-gradient-to-br from-orange-100 to-orange-200">
                  <Activity className="h-4 w-4 text-orange-600" />
                </div>
                <span className="text-sm font-medium text-slate-700">Users</span>
              </div>
              <TrendingUp className="h-4 w-4 text-green-500" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-slate-800">
                  {currentMetrics.activeUsers}
                </span>
              </div>
              <div className="text-xs text-slate-500">
                Active sessions
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* CPU & Memory Trends */}
        <Card className="glass-card-strong border-0">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Cpu className="h-5 w-5 text-blue-600" />
              System Resources
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={metrics}>
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={formatTime}
                    fontSize={12}
                  />
                  <YAxis fontSize={12} />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="cpuUsage"
                    stackId="1"
                    stroke="#3b82f6"
                    fill="#3b82f6"
                    fillOpacity={0.3}
                    name="CPU Usage"
                  />
                  <Area
                    type="monotone"
                    dataKey="memoryUsage"
                    stackId="2"
                    stroke="#8b5cf6"
                    fill="#8b5cf6"
                    fillOpacity={0.3}
                    name="Memory Usage"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Response Time Trends */}
        <Card className="glass-card-strong border-0">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-green-600" />
              Performance Metrics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={metrics}>
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={formatTime}
                    fontSize={12}
                  />
                  <YAxis fontSize={12} />
                  <Tooltip content={<CustomTooltip />} />
                  <Line
                    type="monotone"
                    dataKey="responseTime"
                    stroke="#10b981"
                    strokeWidth={2}
                    dot={false}
                    name="Response Time"
                  />
                  <Line
                    type="monotone"
                    dataKey="analysisSpeed"
                    stroke="#f59e0b"
                    strokeWidth={2}
                    dot={false}
                    name="Analysis Speed"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Status Summary */}
      <Card className="glass-card-strong border-0">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5 text-slate-600" />
            System Status Summary
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700">Analysis Engine</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Processing Speed</span>
                  <Badge variant="outline" className="text-green-600">
                    {currentMetrics.analysisSpeed.toFixed(0)} docs/min
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Queue Status</span>
                  <Badge variant="outline" className="text-blue-600">
                    Empty
                  </Badge>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700">AI Models</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Semantic Model</span>
                  <Badge variant="outline" className="text-green-600">
                    Active
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Enhanced Model</span>
                  <Badge variant="outline" className="text-green-600">
                    Active
                  </Badge>
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h4 className="font-semibold text-slate-700">Database</h4>
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Connection</span>
                  <Badge variant="outline" className="text-green-600">
                    Healthy
                  </Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-slate-600">Cache Hit Rate</span>
                  <Badge variant="outline" className="text-blue-600">
                    94.2%
                  </Badge>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PerformanceMonitor; 