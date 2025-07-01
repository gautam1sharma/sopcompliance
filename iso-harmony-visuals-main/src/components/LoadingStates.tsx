import React from 'react';
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";

// Animated Loading Spinner
export const LoadingSpinner: React.FC<{ size?: 'sm' | 'md' | 'lg'; className?: string }> = ({ 
  size = 'md', 
  className = '' 
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  return (
    <div className={`animate-spin rounded-full border-2 border-blue-200 border-t-blue-600 ${sizeClasses[size]} ${className}`} />
  );
};

// Progress Bar with Shimmer Effect
export const ShimmerProgress: React.FC<{ 
  value: number; 
  label?: string; 
  showPercentage?: boolean;
  className?: string;
}> = ({ 
  value, 
  label, 
  showPercentage = true, 
  className = '' 
}) => {
  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-slate-700">{label}</span>
          {showPercentage && (
            <span className="text-sm text-slate-500">{value}%</span>
          )}
        </div>
      )}
      <div className="relative">
        <Progress value={value} className="h-3 progress-glow" />
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer rounded-full" />
      </div>
    </div>
  );
};

// Dashboard Skeleton
export const DashboardSkeleton: React.FC = () => {
  return (
    <div className="w-full space-y-8 animate-fade-in">
      {/* Header Skeleton */}
      <div className="flex items-center justify-between">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="flex gap-3">
          <Skeleton className="h-10 w-24" />
          <Skeleton className="h-10 w-32" />
        </div>
      </div>

      {/* Metrics Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="glass-card-strong border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-3">
                  <Skeleton className="h-4 w-24" />
                  <Skeleton className="h-8 w-16" />
                  <Skeleton className="h-3 w-32" />
                </div>
                <Skeleton className="h-12 w-12 rounded-xl" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Chart Skeleton */}
      <Card className="glass-card-strong border-0">
        <CardHeader>
          <div className="flex items-center justify-between">
            <Skeleton className="h-6 w-48" />
            <div className="flex gap-2">
              <Skeleton className="h-8 w-20" />
              <Skeleton className="h-8 w-20" />
              <Skeleton className="h-8 w-20" />
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="h-96 flex items-end justify-between gap-4 p-4">
            {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
              <div key={i} className="flex-1 space-y-2">
                <Skeleton 
                  className="w-full bg-gradient-to-t from-blue-200 to-blue-100" 
                  style={{ height: `${Math.random() * 200 + 100}px` }}
                />
                <Skeleton className="h-3 w-full" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Upload Area Skeleton
export const UploadSkeleton: React.FC = () => {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center space-y-4">
        <Skeleton className="h-16 w-16 rounded-full mx-auto" />
        <Skeleton className="h-6 w-48 mx-auto" />
        <Skeleton className="h-4 w-64 mx-auto" />
      </div>
      
      <Card className="glass-card-strong border-2 border-dashed border-slate-300">
        <CardContent className="p-12">
          <div className="text-center space-y-4">
            <div className="relative">
              <Skeleton className="h-24 w-24 rounded-2xl mx-auto" />
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent animate-shimmer rounded-2xl" />
            </div>
            <Skeleton className="h-6 w-64 mx-auto" />
            <Skeleton className="h-4 w-48 mx-auto" />
            <Skeleton className="h-10 w-32 mx-auto rounded-lg" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// File Processing Animation
export const FileProcessingLoader: React.FC<{ 
  fileName: string; 
  progress: number; 
  stage: string;
}> = ({ fileName, progress, stage }) => {
  return (
    <Card className="glass-card-strong border-0 animate-scale-in">
      <CardContent className="p-6">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="h-12 w-12 rounded-lg bg-gradient-to-br from-blue-100 to-blue-200 flex items-center justify-center">
              <LoadingSpinner size="sm" />
            </div>
            <div className="absolute -bottom-1 -right-1 h-4 w-4 bg-blue-600 rounded-full animate-pulse" />
          </div>
          
          <div className="flex-1 space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-slate-800 truncate">{fileName}</h4>
              <span className="text-sm text-slate-500">{progress}%</span>
            </div>
            
            <ShimmerProgress value={progress} className="mb-2" />
            
            <p className="text-sm text-slate-600">
              {stage} <span className="animate-pulse">...</span>
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Document Card Skeleton
export const DocumentCardSkeleton: React.FC = () => {
  return (
    <Card className="glass-card-strong border-0">
      <CardContent className="p-6">
        <div className="flex items-start gap-4">
          <Skeleton className="h-12 w-12 rounded-lg" />
          <div className="flex-1 space-y-3">
            <Skeleton className="h-5 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
            <div className="flex gap-2">
              <Skeleton className="h-6 w-16 rounded-full" />
              <Skeleton className="h-6 w-20 rounded-full" />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

// Table Skeleton
export const TableSkeleton: React.FC<{ rows?: number; columns?: number }> = ({ 
  rows = 5, 
  columns = 4 
}) => {
  return (
    <div className="space-y-4">
      {/* Table Header */}
      <div className="grid gap-4" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
        {Array.from({ length: columns }).map((_, i) => (
          <Skeleton key={i} className="h-4 w-full" />
        ))}
      </div>
      
      {/* Table Rows */}
      {Array.from({ length: rows }).map((_, rowIndex) => (
        <div 
          key={rowIndex} 
          className="grid gap-4 py-3 border-b border-slate-200" 
          style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}
        >
          {Array.from({ length: columns }).map((_, colIndex) => (
            <Skeleton 
              key={colIndex} 
              className="h-4" 
              style={{ width: `${Math.random() * 40 + 60}%` }}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

// Animated Dots Loader
export const DotsLoader: React.FC<{ className?: string }> = ({ className = '' }) => {
  return (
    <div className={`flex space-x-1 ${className}`}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="h-2 w-2 bg-blue-600 rounded-full animate-bounce"
          style={{ animationDelay: `${i * 0.1}s` }}
        />
      ))}
    </div>
  );
};

// Pulse Card Loader
export const PulseCard: React.FC<{ children?: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <Card className={`glass-card-strong border-0 animate-pulse ${className}`}>
      <CardContent className="p-6">
        {children || (
          <div className="space-y-4">
            <Skeleton className="h-6 w-3/4" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-2/3" />
          </div>
        )}
      </CardContent>
    </Card>
  );
};

// Full Page Loader
export const FullPageLoader: React.FC<{ message?: string }> = ({ 
  message = "Loading..." 
}) => {
  return (
    <div className="fixed inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="text-center space-y-4">
        <LoadingSpinner size="lg" />
        <p className="text-lg font-medium text-slate-700">{message}</p>
        <DotsLoader />
      </div>
    </div>
  );
};

export default {
  LoadingSpinner,
  ShimmerProgress,
  DashboardSkeleton,
  UploadSkeleton,
  FileProcessingLoader,
  DocumentCardSkeleton,
  TableSkeleton,
  DotsLoader,
  PulseCard,
  FullPageLoader
}; 