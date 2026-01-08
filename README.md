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

### Step 3: Download Your Enhanced Resume

1. Your updated resume is now ready
2. Click "📥 Download Updated Resume" to save it
3. Use your new, perfectly matched resume for your job application!

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
│   └── resume_generator.py     # Updated resume generation
├── templates/                  # HTML templates
│   └── index.html             # Main web interface
├── uploads/                    # Uploaded resumes (created automatically)
└── processed/                  # Generated resumes (created automatically)
```

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

#### resume_generator.py
Creates updated resume:
- Maintains original formatting where possible
- Adds new points to appropriate sections
- Supports PDF, DOCX, and TXT output
- Highlights newly added content

## 🎨 Customization

### Adding More Skills to Detection

Edit the skill keywords in `modules/job_analyzer.py` and `modules/resume_parser.py` to include additional technologies or skills relevant to your industry.

### Modifying Search Suggestions

Customize the suggestion templates in `modules/web_search.py` to better match your industry or writing style.

### Changing the UI Theme

Edit the CSS in `templates/index.html` to customize colors, fonts, and layout.

## 🔒 Security Notes

- The application stores files temporarily during processing
- Uploaded files are stored with unique session IDs
- Files are stored locally on the server (not recommended for production without additional security)
- For production use, consider:
  - Adding authentication
  - Using cloud storage with encryption
  - Implementing file cleanup routines
  - Adding rate limiting
  - Using HTTPS

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