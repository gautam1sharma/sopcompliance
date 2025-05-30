
import React, { useState } from 'react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { File, ChevronRight, Eye, Download } from "lucide-react";

interface DocumentCardProps {
  title: string;
  type: 'SOP' | 'ISO';
  date: string;
  excerpt: string;
  onSelect?: () => void;
}

const DocumentCard: React.FC<DocumentCardProps> = ({ title, type, date, excerpt, onSelect }) => {
  const [isHovering, setIsHovering] = useState(false);
  
  const badgeColor = type === 'SOP' 
    ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' 
    : 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300';
  
  return (
    <Card 
      className="document-card group relative overflow-hidden"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      {/* Subtle gradient border effect that animates on hover */}
      <div 
        className={`absolute inset-0 bg-gradient-to-r from-blue-400 to-blue-600 opacity-0 group-hover:opacity-100 transition-opacity duration-300`} 
        style={{ height: '2px', top: 0 }} 
      />
      
      <div className="flex items-start gap-4">
        <div className="p-2 bg-blue-50 dark:bg-blue-950/50 rounded-lg">
          <File className="h-8 w-8 text-blue-500" />
        </div>
        
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold line-clamp-1">{title}</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${badgeColor}`}>
              {type}
            </span>
          </div>
          
          <p className="text-sm text-muted-foreground mt-1">
            Last updated: {date}
          </p>
          
          <p className="mt-3 text-sm line-clamp-2 text-muted-foreground">
            {excerpt}
          </p>
          
          <div className={`flex gap-2 mt-4 transition-opacity duration-300 ${isHovering ? 'opacity-100' : 'opacity-0'}`}>
            <Button 
              variant="outline" 
              size="sm" 
              className="flex items-center gap-1"
            >
              <Eye className="h-3.5 w-3.5" />
              <span>Preview</span>
            </Button>
            
            <Button 
              variant="outline" 
              size="sm" 
              className="flex items-center gap-1"
            >
              <Download className="h-3.5 w-3.5" />
              <span>Download</span>
            </Button>
            
            <Button 
              size="sm" 
              className="ml-auto flex items-center gap-1"
              onClick={onSelect}
            >
              <span>Select</span>
              <ChevronRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default DocumentCard;
