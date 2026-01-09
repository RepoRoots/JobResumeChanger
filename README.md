# JobResumeChanger

A powerful web application that automatically tailors your resume to match any job description perfectly. Upload your resume, paste a job description, and let the AI find missing points and enhance your resume to achieve a 100% match.

## 🌟 Features

- **Smart Analysis**: Automatically analyzes job descriptions to extract key requirements, skills, and qualifications
- **Resume Parsing**: Supports PDF, DOCX, and TXT resume formats
- **Gap Detection**: Identifies missing points in your resume compared to job requirements
- **Web Search Integration**: Provides intelligent suggestions and examples for missing skills
- **Interactive UI**: Easy-to-use interface to specify where to add missing points
- **Resume Generation**: Creates an updated resume with all enhancements in PDF, DOCX, or TXT format
- **Section Mapping**: Intelligently maps missing points to appropriate resume sections
- **ATS Compliance Checker**: ✨ NEW! Check how well your resume performs with Applicant Tracking Systems
- **ATS Score & Grading**: Get detailed scoring on format, structure, keywords, and content quality
- **Optimization Suggestions**: Receive actionable recommendations to improve your ATS score

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/RepoRoots/JobResumeChanger.git
cd JobResumeChanger
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. The application will be running and ready to use!

## 📖 How to Use

### Step 1: Upload Your Resume and Job Description

1. Click "Choose File" and select your resume (PDF, DOCX, or TXT format)
2. Paste the complete job description in the text area
3. Click "Analyze & Find Missing Points"

### Step 2: Review and Add Missing Points

1. The application will display all missing points found in your resume
2. For each missing point:
   - Click "🔍 Search & Add" to get suggestions and examples
   - Select the appropriate section in your resume
   - Optionally specify which project this relates to
   - Add any additional details or metrics
   - Click "Add to Resume"
3. Skip any points you don't want to include
4. Once done, click "Generate Updated Resume"

### Step 3: Check ATS Compliance Score

1. Before downloading, click "🔍 Check ATS Score" to see how well your resume performs with Applicant Tracking Systems
2. View your overall ATS score (0-100%) with a letter grade
3. See detailed breakdown of:
   - Format Compatibility
   - Structure Quality
   - Keyword Optimization
   - Content Quality
4. Review prioritized recommendations to improve your score
5. Click "🚀 View Optimization Tips" for specific suggestions on:
   - Formatting best practices
   - Section improvements
   - Keyword additions
   - Content enhancements

### Step 4: Download Your Enhanced Resume

1. Your updated resume is now ready and ATS-optimized
2. Click "📥 Download Updated Resume" to save it
3. Use your new, perfectly matched and ATS-friendly resume for your job application!

## 🏗️ Project Structure

```
JobResumeChanger/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── modules/                    # Core functionality modules
│   ├── __init__.py
│   ├── resume_parser.py        # Resume parsing and text extraction
│   ├── job_analyzer.py         # Job description analysis
│   ├── comparison_engine.py    # Resume vs. job comparison
│   ├── web_search.py           # Search and suggestion engine
│   ├── resume_generator.py     # Updated resume generation
│   └── ats_checker.py          # ATS compliance scoring and optimization
├── services/                   # Service layer (OOP architecture)
│   ├── __init__.py
│   ├── resume_service.py       # Resume business logic service
│   └── session_service.py      # Session management service
├── templates/                  # HTML templates
│   └── index.html             # Main web interface
├── uploads/                    # Uploaded resumes (created automatically)
└── processed/                  # Generated resumes (created automatically)
```

## 🏗️ Architecture

The application follows **Object-Oriented Programming (OOP) principles** with a clean, layered architecture:

### Service Layer
- **ResumeService**: Encapsulates resume operations (upload, parse, analyze, generate)
- **SessionService**: Manages user session state and data persistence

### Controller Layer
- **ResumeController**: Handles HTTP requests and coordinates services

### Application Layer
- **JobResumeChangerApp**: Main application orchestrator
- **ApplicationConfig**: Centralized configuration management

**OOP Patterns Used**:
- Service Layer Pattern
- Dependency Injection
- Controller Pattern
- Factory Pattern (create_app)
- Composition over Inheritance

See [OOP_ARCHITECTURE.md](OOP_ARCHITECTURE.md) for detailed architecture documentation.

## 🔧 Technical Details

### Modules

#### resume_parser.py
Extracts text and structure from resume files:
- Supports PDF, DOCX, and TXT formats
- Identifies sections (Experience, Skills, Education, etc.)
- Extracts skills, work experience, and education details

#### job_analyzer.py
Analyzes job descriptions to extract:
- Technical skills required
- Soft skills needed
- Experience level expectations
- Education requirements
- Key responsibilities

#### comparison_engine.py
Compares resume with job requirements:
- Identifies missing technical skills
- Finds gaps in soft skills
- Checks responsibility alignment
- Validates education requirements
- Assesses experience match

#### web_search.py
Provides intelligent suggestions:
- Generates context-aware examples
- Offers resume-ready bullet points
- Suggests action-oriented phrases
- Provides industry-standard wording

#### ats_checker.py
Checks ATS compliance and optimization:
- Calculates comprehensive ATS scores (0-100%)
- Evaluates format compatibility (no tables, graphics, complex formatting)
- Assesses structure quality (proper sections, contact info placement)
- Analyzes keyword optimization (action verbs, technical skills, soft skills)
- Checks content quality (quantifiable achievements, concise writing)
- Generates prioritized recommendations for improvement
- Provides specific optimization suggestions by category

#### resume_generator.py
Creates updated resume:
- Maintains original formatting where possible
- Adds new points to appropriate sections
- Supports PDF, DOCX, and TXT output
- Highlights newly added content

## 📊 ATS Compliance Feature

The ATS (Applicant Tracking System) compliance feature helps ensure your resume passes through automated screening systems used by most companies.

### What is ATS?

Applicant Tracking Systems are software applications that help companies manage their recruitment process. They scan and parse resumes before human recruiters see them. Many qualified candidates are filtered out because their resumes aren't ATS-friendly.

### ATS Scoring Components

The ATS checker evaluates four key areas:

1. **Format Compatibility (30% weight)**
   - Checks for simple, parseable formatting
   - Detects problematic elements (tables, graphics, headers/footers)
   - Validates proper use of bullet points
   - Ensures adequate text density and line breaks

2. **Structure Quality (30% weight)**
   - Verifies presence of essential sections (Experience, Education, Skills)
   - Checks for contact information placement
   - Evaluates section organization
   - Assesses overall resume structure

3. **Keyword Optimization (25% weight)**
   - Analyzes action verb usage
   - Counts technical keywords
   - Evaluates soft skills inclusion
   - Matches keywords against job requirements
   - Checks appropriate keyword density

4. **Content Quality (15% weight)**
   - Looks for quantifiable achievements
   - Checks for outdated phrases
   - Evaluates sentence length and conciseness
   - Validates professional writing style

### Score Grading

- **A (90-100%)**: Excellent ATS compatibility
- **B (80-89%)**: Good compatibility with minor improvements needed
- **C (70-79%)**: Fair compatibility, several improvements recommended
- **D (60-69%)**: Poor compatibility, significant changes needed
- **F (<60%)**: Very poor compatibility, major restructuring required

### Optimization Suggestions

The system provides categorized recommendations:
- **Formatting**: Font choices, file formats, layout tips
- **Sections**: Missing or weak sections to add
- **Keywords**: Specific keywords and phrases to include
- **Content**: Writing improvements and best practices

## 🎨 Customization

### Adding More Skills to Detection

Edit the skill keywords in `modules/job_analyzer.py` and `modules/resume_parser.py` to include additional technologies or skills relevant to your industry.

### Modifying Search Suggestions

Customize the suggestion templates in `modules/web_search.py` to better match your industry or writing style.

### Changing the UI Theme

Edit the CSS in `templates/index.html` to customize colors, fonts, and layout.

## 🔒 Security Notes

**Important: This application is designed for development and personal use. Do not deploy to production without proper security measures.**

- The application stores files temporarily during processing
- Uploaded files are stored with unique session IDs
- Files are stored locally on the server (not recommended for production without additional security)
- Debug mode is disabled in production when FLASK_ENV=production is set

### For Production Deployment:

**Required:**
1. Set environment variable: `FLASK_ENV=production`
2. Set a secure secret key: `SECRET_KEY=<your-secure-random-key>`
3. Use a production WSGI server (e.g., Gunicorn, uWSGI) instead of Flask's built-in server
4. Enable HTTPS/SSL certificates

**Recommended:**
- Add user authentication and authorization
- Use cloud storage with encryption for file uploads
- Implement automatic file cleanup routines
- Add rate limiting to prevent abuse
- Set up logging and monitoring
- Use a reverse proxy (nginx, Apache)
- Implement CSRF protection
- Add input validation and sanitization
- Set up a firewall and security groups

**Example Production Setup:**
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Run with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available for personal and educational use.

## 💡 Tips for Best Results

1. **Be Comprehensive**: Paste the complete job description for better analysis
2. **Add Details**: When adding points, include specific metrics and achievements
3. **Choose Wisely**: Select appropriate sections for each missing point
4. **Review Carefully**: Review the generated resume before using it
5. **Customize Further**: Use the generated resume as a base and add personal touches

## 🐛 Troubleshooting

### "Error processing upload"
- Ensure your resume file is in PDF, DOCX, or TXT format
- Check that the file size is under 16MB
- Try converting your resume to a different format

### "No missing points found"
- Your resume may already be well-aligned with the job description
- Try with a more detailed job description
- Ensure the job description contains specific requirements

### Resume generation fails
- Check that you've added at least one point
- Ensure you have write permissions in the application directory
- Try generating in TXT format first

## 🌐 Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 📞 Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Made with ❤️ to help job seekers land their dream jobs!**