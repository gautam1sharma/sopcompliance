import React, { useState, useRef, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { 
  Upload, 
  File, 
  FileText, 
  X, 
  CheckCircle, 
  AlertCircle,
  Cloud,
  Zap,
  Shield,
  Clock,
  BarChart3
} from "lucide-react";

interface FileWithProgress {
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
  id: string;
}

const FileUploader: React.FC = () => {
  const [files, setFiles] = useState<FileWithProgress[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [analysisMethod, setAnalysisMethod] = useState<'enhanced' | 'semantic'>('enhanced');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    handleFiles(droppedFiles);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      handleFiles(selectedFiles);
    }
  };

  const handleFiles = (newFiles: File[]) => {
    const validFiles = newFiles.filter(file => {
      const validTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
      return validTypes.includes(file.type) && file.size <= 16 * 1024 * 1024; // 16MB limit
    });

    if (validFiles.length !== newFiles.length) {
      // Show error for invalid files
      alert('Some files were skipped. Please upload only PDF, TXT, or DOCX files under 16MB.');
    }

    const filesWithProgress: FileWithProgress[] = validFiles.map(file => ({
      file,
      progress: 0,
      status: 'uploading' as const,
      id: Math.random().toString(36).substr(2, 9)
    }));

    setFiles(prev => [...prev, ...filesWithProgress]);

    // Simulate upload progress
    filesWithProgress.forEach((fileWithProgress) => {
      simulateUpload(fileWithProgress.id);
    });
  };

  const simulateUpload = (fileId: string) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 30;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        setFiles(prev => 
          prev.map(f => 
            f.id === fileId 
              ? { ...f, progress: 100, status: 'completed' as const }
              : f
          )
        );
      } else {
        setFiles(prev => 
          prev.map(f => 
            f.id === fileId 
              ? { ...f, progress }
              : f
          )
        );
      }
    }, 200);
  };

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const analyzeFiles = async () => {
    if (files.length === 0) return;
    
    setIsAnalyzing(true);
    
    // Simulate analysis
    setTimeout(() => {
      setIsAnalyzing(false);
      // Here you would typically redirect to results or show them in a modal
      alert(`Analysis completed using ${analysisMethod} method!`);
    }, 3000);
  };

  const getFileIcon = (file: File) => {
    if (file.type === 'application/pdf') {
      return <File className="h-5 w-5 text-red-500" />;
    } else if (file.type === 'text/plain') {
      return <FileText className="h-5 w-5 text-blue-500" />;
    } else {
      return <FileText className="h-5 w-5 text-green-500" />;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full space-y-8 animate-fade-in">
      {/* Header */}
      <div className="text-center space-y-4">
        <div className="inline-block p-3 rounded-2xl bg-gradient-to-br from-blue-100 to-purple-100">
          <Cloud className="h-8 w-8 text-blue-600" />
        </div>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent">
          Document Upload & Analysis
        </h2>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Upload your SOPs and policy documents for intelligent compliance analysis against ISO 27002 standards.
        </p>
      </div>

      {/* Analysis Method Selection */}
      <Card className="glass-card-strong border-0 max-w-2xl mx-auto">
        <CardContent className="p-6">
          <h3 className="text-lg font-semibold mb-4 text-center">Choose Analysis Method</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => setAnalysisMethod('enhanced')}
              className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                analysisMethod === 'enhanced' 
                  ? 'border-blue-500 bg-blue-50' 
                  : 'border-slate-200 bg-white hover:border-blue-300'
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <Zap className="h-5 w-5 text-blue-600" />
                <span className="font-semibold">Enhanced Analysis</span>
              </div>
              <p className="text-sm text-slate-600">
                Fast, keyword-based compliance checking with pattern matching
              </p>
              <Badge variant="secondary" className="mt-2">Recommended</Badge>
            </button>

            <button
              onClick={() => setAnalysisMethod('semantic')}
              className={`p-4 rounded-xl border-2 transition-all duration-300 text-left ${
                analysisMethod === 'semantic' 
                  ? 'border-purple-500 bg-purple-50' 
                  : 'border-slate-200 bg-white hover:border-purple-300'
              }`}
            >
              <div className="flex items-center gap-3 mb-2">
                <BarChart3 className="h-5 w-5 text-purple-600" />
                <span className="font-semibold">Semantic Analysis</span>
              </div>
              <p className="text-sm text-slate-600">
                AI-powered deep understanding with contextual analysis
              </p>
              <Badge variant="outline" className="mt-2">Advanced</Badge>
            </button>
          </div>
        </CardContent>
      </Card>

      {/* File Upload Area */}
      <div className="max-w-4xl mx-auto">
        <div
          className={`relative border-2 border-dashed rounded-2xl p-12 transition-all duration-300 ${
            isDragging
              ? 'border-blue-400 bg-blue-50/50 scale-[1.02]'
              : 'border-slate-300 bg-white/50 hover:border-blue-300 hover:bg-blue-50/30'
          }`}
          onDragEnter={handleDragIn}
          onDragLeave={handleDragOut}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            multiple
            accept=".pdf,.txt,.docx"
            onChange={handleFileChange}
            className="hidden"
          />
          
          <div className="text-center space-y-6">
            <div className={`mx-auto w-20 h-20 rounded-2xl flex items-center justify-center transition-all duration-300 ${
              isDragging 
                ? 'bg-blue-200 text-blue-700 scale-110' 
                : 'bg-slate-100 text-slate-600 hover:bg-blue-100 hover:text-blue-600'
            }`}>
              <Upload className="h-8 w-8" />
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">
                {isDragging ? 'Drop files here' : 'Upload your documents'}
              </h3>
              <p className="text-slate-600 mb-4">
                Drag and drop files here, or click to browse
              </p>
              
              <Button 
                onClick={() => fileInputRef.current?.click()}
                className="btn-gradient"
                size="lg"
              >
                <Upload className="mr-2 h-5 w-5" />
                Choose Files
              </Button>
            </div>
            
            <div className="flex flex-wrap justify-center gap-4 text-sm text-slate-500">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4" />
                <span>Secure upload</span>
              </div>
              <div className="flex items-center gap-2">
                <File className="h-4 w-4" />
                <span>PDF, DOCX, TXT</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-4 w-4" />
                <span>Max 16MB per file</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Uploaded Files */}
      {files.length > 0 && (
        <Card className="glass-card-strong border-0 max-w-4xl mx-auto">
          <CardContent className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold">Uploaded Files ({files.length})</h3>
              <Button
                onClick={analyzeFiles}
                disabled={files.some(f => f.status !== 'completed') || isAnalyzing}
                className="btn-gradient"
              >
                {isAnalyzing ? (
                  <>
                    <div className="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <BarChart3 className="mr-2 h-4 w-4" />
                    Start Analysis
                  </>
                )}
              </Button>
            </div>
            
            <div className="space-y-4">
              {files.map((fileWithProgress) => (
                <div 
                  key={fileWithProgress.id} 
                  className="flex items-center gap-4 p-4 border rounded-xl bg-white/50 hover:bg-white/70 transition-colors"
                >
                  <div className="flex-shrink-0">
                    {getFileIcon(fileWithProgress.file)}
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="font-medium text-slate-800 truncate">
                        {fileWithProgress.file.name}
                      </p>
                      {fileWithProgress.status === 'completed' && (
                        <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                      )}
                      {fileWithProgress.status === 'error' && (
                        <AlertCircle className="h-4 w-4 text-red-500 flex-shrink-0" />
                      )}
                    </div>
                    
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-slate-500">
                        {formatFileSize(fileWithProgress.file.size)}
                      </span>
                      
                      {fileWithProgress.status === 'uploading' && (
                        <div className="flex-1 max-w-xs">
                          <Progress value={fileWithProgress.progress} className="h-2" />
                        </div>
                      )}
                      
                      <Badge 
                        variant={
                          fileWithProgress.status === 'completed' ? 'default' :
                          fileWithProgress.status === 'error' ? 'destructive' : 'secondary'
                        }
                        className="text-xs"
                      >
                        {fileWithProgress.status === 'completed' ? 'Ready' :
                         fileWithProgress.status === 'error' ? 'Error' : 
                         `${Math.round(fileWithProgress.progress)}%`}
                      </Badge>
                    </div>
                  </div>
                  
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeFile(fileWithProgress.id)}
                    className="text-slate-400 hover:text-red-500"
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Analysis Progress */}
      {isAnalyzing && (
        <Card className="glass-card-strong border-0 max-w-2xl mx-auto">
          <CardContent className="p-6 text-center">
            <div className="space-y-4">
              <div className="animate-pulse">
                <BarChart3 className="h-12 w-12 text-blue-600 mx-auto" />
              </div>
              <h3 className="text-lg font-semibold">Analyzing Documents...</h3>
              <p className="text-slate-600">
                Running {analysisMethod} analysis against ISO 27002 standards
              </p>
              <Progress value={66} className="progress-glow" />
              <p className="text-sm text-slate-500">
                This may take a few moments depending on document size
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default FileUploader;
