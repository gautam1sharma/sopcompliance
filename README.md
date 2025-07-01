# 🛡️ ISO 27002 Compliance Checker - Modern Edition

A cutting-edge compliance analysis platform that helps organizations assess their Standard Operating Procedures (SOPs) against ISO 27002:2022 information security controls with AI-powered insights and modern visualization.

## ✨ Key Features

### 🎯 **Core Functionality**
- **AI-Powered Analysis**: Dual analysis modes (Enhanced & Semantic) for comprehensive compliance checking
- **Interactive Dashboards**: Real-time compliance scoring with modern data visualization
- **Document Upload**: Secure drag-and-drop interface with progress tracking
- **Gap Analysis**: Intelligent identification of compliance gaps with actionable recommendations

### 🎨 **Modern Design**
- **Glass Morphism UI**: Contemporary design with backdrop blur effects
- **Responsive Layout**: Optimized for desktop, tablet, and mobile devices
- **Advanced Animations**: Micro-interactions and smooth transitions
- **Professional Branding**: Gradient logos, modern typography, and cohesive color scheme

### 📊 **Enhanced Visualizations**
- **Interactive Charts**: Bar, pie, and radar charts with real-time data
- **Compliance Metrics**: Visual progress indicators and trend analysis
- **Risk Assessment**: Color-coded severity levels and recommendations
- **Export Capabilities**: Professional report generation (Coming Soon)

## 🚀 Quick Start

### Frontend (React Application)

1. **Navigate to the frontend directory:**
   ```bash
   cd iso-harmony-visuals-main
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   ```
   http://localhost:5173
   ```

### Backend (Flask API)

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key-here
   ```

4. **Start the Flask server:**
   ```bash
   python app.py
   ```

5. **API will be available at:**
   ```
   http://localhost:5000
   ```

## 🏗️ Architecture

```
📁 Project Root
├── 🎨 iso-harmony-visuals-main/     # Modern React Frontend
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── ui/                  # shadcn/ui component library
│   │   │   ├── Dashboard.tsx        # Enhanced dashboard with analytics
│   │   │   ├── FileUploader.tsx     # Modern drag-and-drop uploader
│   │   │   ├── Navbar.tsx           # Professional navigation
│   │   │   └── ComplianceChart.tsx  # Interactive data visualization
│   │   ├── pages/
│   │   │   └── Index.tsx            # Modernized landing page
│   │   └── index.css                # Enhanced styles and animations
│   └── package.json                 # Modern dependencies
├── ⚙️ Backend/                      # Python Flask API
│   ├── app.py                       # Main application
│   ├── enhanced_compliance_checker.py
│   ├── semantic_compliance_checker.py
│   └── utils/                       # Utilities and helpers
├── 📊 iso_standards/                # ISO 27002 reference data
└── 📁 uploads/                      # Document storage
```

## 🛠️ Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Accessible component library
- **Recharts** - Interactive data visualization
- **Lucide React** - Modern icon library
- **Vite** - Fast build tool

### Backend
- **Flask** - Lightweight web framework
- **Python 3.8+** - Backend language
- **PyPDF2** - PDF processing
- **Sentence Transformers** - AI/ML for semantic analysis
- **Marshmallow** - Data validation

## 🎨 Design System

### Color Palette
- **Primary**: Blue gradient (`from-blue-600 to-purple-600`)
- **Success**: Green (`text-green-600`)
- **Warning**: Yellow (`text-yellow-600`)
- **Error**: Red (`text-red-600`)
- **Neutral**: Slate shades

### Typography
- **Headings**: Inter font, bold weights
- **Body**: Inter font, regular weight
- **Gradient Text**: Blue to purple gradients

### Components
- **Glass Cards**: `glass-card-strong` utility class
- **Hover Effects**: Scale and shadow transitions
- **Animations**: Fade-in, slide, and pulse effects

## 🔧 Configuration

### Environment Variables

**Frontend** (`.env`):
```env
VITE_API_URL=http://localhost:5000
VITE_APP_VERSION=2.0.0
```

**Backend**:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
LOG_LEVEL=INFO
MODEL_CACHE_DIR=./.model_cache
```

### Customization

**Modify Analysis Methods:**
Edit `enhanced_compliance_checker.py` or `semantic_compliance_checker.py`

**Update ISO Standards:**
Modify `iso_standards/iso27002.json`

**Customize UI:**
Edit components in `iso-harmony-visuals-main/src/components/`

## 📱 Usage Guide

### 1. Document Upload
- Drag and drop PDF, DOCX, or TXT files
- Select analysis method (Enhanced or Semantic)
- Monitor upload progress with real-time indicators

### 2. Analysis Dashboard
- View comprehensive compliance metrics
- Explore interactive charts and visualizations
- Review detailed gap analysis and recommendations

### 3. Export Reports
- Generate professional compliance reports
- Export data in multiple formats
- Share insights with stakeholders

## 🔒 Security Features

- **File Validation**: Secure upload with type and size checking
- **Content Sanitization**: XSS and injection protection
- **Security Headers**: CSRF, XSS, and clickjacking protection
- **Input Validation**: Comprehensive data validation
- **Audit Logging**: Detailed security event logging

## 🚀 Deployment

### Production Deployment

**Frontend (Vercel/Netlify):**
```bash
npm run build
# Deploy the 'dist' folder
```

**Backend (Docker):**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **shadcn/ui** for the excellent component library
- **Tailwind CSS** for utility-first styling
- **Recharts** for data visualization
- **ISO/IEC 27002:2022** for security control standards

---

**Built with ❤️ for modern compliance management**
