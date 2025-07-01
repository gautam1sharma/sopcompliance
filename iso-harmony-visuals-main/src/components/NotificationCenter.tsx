import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  Bell, X, CheckCircle, AlertTriangle, Info, AlertCircle,
  Clock, User, FileText, Shield, TrendingUp, Settings,
  BellRing, Volume2, VolumeX
} from "lucide-react";

interface Notification {
  id: string;
  type: 'success' | 'warning' | 'error' | 'info';
  title: string;
  message: string;
  timestamp: Date;
  read: boolean;
  category: 'compliance' | 'system' | 'security' | 'analysis';
  priority: 'low' | 'medium' | 'high' | 'critical';
  actionUrl?: string;
}

const NotificationCenter: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [filter, setFilter] = useState<'all' | 'unread' | 'high'>('all');

  // Mock real-time notifications
  useEffect(() => {
    const mockNotifications: Notification[] = [
      {
        id: '1',
        type: 'success',
        title: 'Analysis Complete',
        message: 'ISO 27002 compliance analysis for "Security Policy v2.1" has been completed with a 78% compliance score.',
        timestamp: new Date(Date.now() - 2 * 60 * 1000),
        read: false,
        category: 'analysis',
        priority: 'medium'
      },
      {
        id: '2',
        type: 'warning',
        title: 'Compliance Gap Detected',
        message: 'Critical gaps found in Access Control section. 3 high-priority recommendations require immediate attention.',
        timestamp: new Date(Date.now() - 15 * 60 * 1000),
        read: false,
        category: 'compliance',
        priority: 'high'
      },
      {
        id: '3',
        type: 'info',
        title: 'System Update',
        message: 'New ISO 27002:2022 control mappings have been added to the knowledge base.',
        timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000),
        read: true,
        category: 'system',
        priority: 'low'
      }
    ];

    setNotifications(mockNotifications);
  }, []);

  const getIcon = (type: string) => {
    switch (type) {
      case 'success': return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'warning': return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      case 'error': return <AlertCircle className="h-5 w-5 text-red-500" />;
      default: return <Info className="h-5 w-5 text-blue-500" />;
    }
  };

  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <div className="relative">
      <Button
        variant="outline"
        size="sm"
        onClick={() => setIsOpen(!isOpen)}
        className="relative hover-glow"
      >
        <Bell className="h-4 w-4" />
        {unreadCount > 0 && (
          <Badge className="absolute -top-2 -right-2 h-5 w-5 p-0 text-xs bg-red-500 text-white animate-pulse">
            {unreadCount}
          </Badge>
        )}
      </Button>

      {isOpen && (
        <Card className="absolute right-0 top-12 w-96 glass-card-strong border-0 shadow-2xl z-50">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Notifications</span>
              <Button variant="ghost" size="sm" onClick={() => setIsOpen(false)}>
                <X className="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {notifications.map((notification) => (
                <div key={notification.id} className="p-3 rounded-lg bg-white/50 border">
                  <div className="flex items-start gap-3">
                    {getIcon(notification.type)}
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">{notification.title}</h4>
                      <p className="text-xs text-slate-600 mt-1">{notification.message}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default NotificationCenter; 