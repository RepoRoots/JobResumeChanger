# JobResumeChanger

A web application that analyzes your resume against job descriptions and helps you optimize it for a 100% match.

## Features

- **Resume Upload**: Supports PDF and DOCX formats
- **Job Description Analysis**: Extracts key requirements, skills, and technologies
- **Gap Analysis**: Identifies missing points in your resume
- **Web Search Integration**: Finds relevant information to enhance your resume
- **Interactive Enhancement**: Choose where and how to add missing points
- **Resume Modification**: Automatically updates your resume with new content
- **Download**: Get your optimized resume in the original format

## How It Works

1. **Upload** your resume (PDF or DOCX)
2. **Paste** the job description you're targeting
3. **Analyze** to see your current match score and missing requirements
4. **Enhance** by selecting which points to add and where
5. **Search** for relevant information to include
6. **Download** your optimized resume

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd JobResumeChanger
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
JobResumeChanger/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Stylesheet
│   └── js/
│       └── main.js        # Frontend JavaScript
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py   # PDF/DOCX parsing
│   ├── job_analyzer.py    # Job description analysis
│   ├── resume_analyzer.py # Resume gap analysis
│   ├── web_search.py      # Web search integration
│   └── resume_modifier.py # Resume modification
├── uploads/               # Temporary upload storage
└── downloads/             # Modified resume storage
```

## Usage Tips

1. **Use DOCX format** for best results when modifying resumes (PDF modifications are more limited)
2. **Provide context** when adding skills to get better generated content
3. **Review generated content** before applying changes
4. **Target specific projects** to make additions more relevant

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/analyze` | POST | Analyze resume against job description |
| `/search` | POST | Search for skill/technology information |
| `/generate-content` | POST | Generate resume content |
| `/modify` | POST | Apply modifications to resume |
| `/download` | GET | Download modified resume |
| `/cleanup` | POST | Clean up temporary files |

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **PDF Processing**: PyMuPDF
- **DOCX Processing**: python-docx
- **Web Search**: DuckDuckGo HTML search

## Configuration

Set the following environment variables for production:

```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV="production"
```

## License

MIT License
