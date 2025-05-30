
import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Upload, FileText, File, X, Check, ArrowRight } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

const FileUploader: React.FC = () => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const { toast } = useToast();
  
  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else {
      setDragActive(false);
    }
  };
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files));
    }
  };
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFiles(Array.from(e.target.files));
    }
  };
  
  const handleFiles = (newFiles: File[]) => {
    // Filter to only accept .doc, .docx, .pdf files
    const validFiles = newFiles.filter(file => 
      file.type === 'application/pdf' || 
      file.type === 'application/msword' ||
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    );
    
    if (validFiles.length !== newFiles.length) {
      toast({
        title: "Invalid file type",
        description: "Only PDF and Word documents are accepted.",
        variant: "destructive"
      });
    }
    
    if (validFiles.length > 0) {
      setFiles(prev => [...prev, ...validFiles]);
      toast({
        title: "Files added",
        description: `${validFiles.length} file(s) added successfully.`
      });
    }
  };
  
  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };
  
  const uploadFiles = () => {
    if (files.length === 0) return;
    
    setUploading(true);
    
    // Simulate upload
    setTimeout(() => {
      setUploading(false);
      toast({
        title: "Upload complete",
        description: `${files.length} file(s) uploaded successfully.`,
      });
      setFiles([]);
    }, 2000);
  };
  
  const getFileIcon = (file: File) => {
    if (file.type === 'application/pdf') {
      return <FileText className="h-5 w-5 text-red-500" />;
    } else {
      return <File className="h-5 w-5 text-blue-500" />;
    }
  };

  return (
    <Card className="w-full p-6 animate-fade-in">
      <h2 className="text-xl font-bold mb-6">Document Upload</h2>
      
      <Tabs defaultValue="upload">
        <TabsList className="grid grid-cols-2 mb-6">
          <TabsTrigger value="upload">Upload Documents</TabsTrigger>
          <TabsTrigger value="library">Document Library</TabsTrigger>
        </TabsList>
        
        <TabsContent value="upload">
          <div 
            className={`border-2 border-dashed rounded-lg p-10 transition-colors duration-300 ${
              dragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-950/30' : 'border-gray-300 dark:border-gray-700'
            }`}
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center text-center">
              <div className="mb-4 p-3 rounded-full bg-blue-50 dark:bg-blue-900/20">
                <Upload className="h-6 w-6 text-blue-500" />
              </div>
              <h3 className="text-lg font-medium">Drag and drop your documents</h3>
              <p className="text-sm text-muted-foreground mt-1 mb-4">
                Supports PDF and Word documents up to 10MB
              </p>
              <Button 
                variant="outline" 
                onClick={() => document.getElementById('file-upload')?.click()}
              >
                Select Files
              </Button>
              <input 
                id="file-upload" 
                type="file" 
                multiple 
                className="hidden" 
                accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={handleFileChange}
              />
            </div>
          </div>
          
          {files.length > 0 && (
            <div className="mt-8 animate-fade-in">
              <h3 className="text-lg font-semibold mb-4">Files to Upload ({files.length})</h3>
              <div className="space-y-3">
                {files.map((file, index) => (
                  <div 
                    key={index} 
                    className="flex items-center justify-between p-3 border rounded-lg bg-slate-50 dark:bg-slate-800/50"
                  >
                    <div className="flex items-center gap-3">
                      {getFileIcon(file)}
                      <div>
                        <div className="font-medium text-sm">{file.name}</div>
                        <div className="text-xs text-muted-foreground">
                          {(file.size / 1024 / 1024).toFixed(2)} MB
                        </div>
                      </div>
                    </div>
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      className="h-8 w-8 p-0"
                      onClick={() => removeFile(index)}
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                ))}
              </div>
              
              <div className="flex justify-end mt-6">
                <Button 
                  onClick={uploadFiles} 
                  disabled={uploading}
                  className="flex items-center gap-2"
                >
                  {uploading ? (
                    <>
                      <div className="h-4 w-4 rounded-full border-2 border-t-transparent border-white animate-spin"></div>
                      <span>Uploading...</span>
                    </>
                  ) : (
                    <>
                      <span>Upload {files.length} file{files.length > 1 ? 's' : ''}</span>
                      <ArrowRight className="h-4 w-4" />
                    </>
                  )}
                </Button>
              </div>
            </div>
          )}
        </TabsContent>
        
        <TabsContent value="library">
          <div className="grid grid-cols-1 gap-4">
            {libraryDocuments.map((doc, idx) => (
              <div 
                key={idx} 
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors animate-fade-in"
                style={{ animationDelay: `${idx * 0.05}s` }}
              >
                <div className="flex items-center gap-4">
                  <div className="p-2 bg-blue-50 dark:bg-blue-900/30 rounded">
                    {doc.type === 'pdf' ? 
                      <FileText className="h-5 w-5 text-red-500" /> : 
                      <File className="h-5 w-5 text-blue-500" />
                    }
                  </div>
                  <div>
                    <div className="font-medium">{doc.name}</div>
                    <div className="text-xs text-muted-foreground flex items-center gap-3 mt-1">
                      <span>{doc.type.toUpperCase()}</span>
                      <span>•</span>
                      <span>{doc.size}</span>
                      <span>•</span>
                      <span>Uploaded {doc.uploadedDate}</span>
                    </div>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button variant="outline" size="sm" className="h-8">
                    View
                  </Button>
                  <Button size="sm" className="h-8">
                    Select
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </Card>
  );
};

const libraryDocuments = [
  { 
    name: "Access Control SOP v2.1", 
    type: "pdf", 
    size: "1.2 MB", 
    uploadedDate: "2 days ago"
  },
  { 
    name: "ISO 27002:2022 - Access Control", 
    type: "docx", 
    size: "890 KB", 
    uploadedDate: "1 week ago"
  },
  { 
    name: "Password Policy SOP", 
    type: "pdf", 
    size: "760 KB", 
    uploadedDate: "2 weeks ago"
  },
  { 
    name: "ISO 27002:2022 - Cryptography", 
    type: "docx", 
    size: "1.1 MB", 
    uploadedDate: "1 month ago"
  }
];

export default FileUploader;
