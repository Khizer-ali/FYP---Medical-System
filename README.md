# Clinical Assistant - Agentic Workflow System

A comprehensive clinical assistant system built with Python (Flask backend) and HTML frontend, featuring an agentic workflow architecture with a master agent controlling multiple specialized sub-agents.

## Features

### Master Agent
- Orchestrates and coordinates all sub-agents
- Manages patient context aggregation
- Provides unified interface for all operations

### Sub-Agents

1. **Document Agent** 📄
   - Upload medical reports (PDF, TXT, Images)
   - Automatic text extraction and parsing
   - OCR support for scanned documents
   - Stores parsed content in database

2. **Vitals Agent** 📊
   - Record patient vital signs:
     - Temperature (°C)
     - Weight (kg)
     - Height (cm)
     - Blood Pressure (mmHg)
     - Heart Rate (bpm)
     - Respiratory Rate (per min)
     - Oxygen Saturation (%)
   - Data validation
   - Historical tracking

3. **Family History Agent** 👨‍👩‍👧‍👦
   - Record family medical history
   - Relation tracking
   - Age of onset information
   - Additional notes

4. **Medical Chatbot Agent** 💬
   - AI-powered medical assistant
   - Uses patient context from all agents
   - Answers questions based on patient records
   - Easy model switching via Hugging Face

5. **Image Agent** 🖼️
   - Upload medical images (X-Ray, CT, MRI, etc.)
   - Image validation and processing
   - Metadata storage
   - Support for DICOM format

6. **Teeth X-Ray Agent** 🦷
   - Annotate individual teeth on an interactive dental chart
   - Persist findings (root canal, cavity, both) per patient
   - Share dental context with the chatbot agent

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **AI Models**: Hugging Face Transformers
- **Document Processing**: PyPDF2, pytesseract, pdf2image
- **Image Processing**: Pillow

## Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (for document parsing):
   - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

4. **Create upload directories** (automatically created on first run):
   - `uploads/documents/`
   - `uploads/images/`

## Configuration

1. **Environment Variables** (optional):
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///clinical_assistant.db
   ```

2. **Model Configuration**:
   To change the chatbot model, edit `agents/chatbot_agent.py`:
   ```python
   self.model_name = "your-preferred-model"  # e.g., "microsoft/DialoGPT-large"
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

## Usage

### 1. Create a Patient
- Go to the dashboard
- Enter patient name (reference number is auto-generated)
- Click "Create Patient"

### 2. Upload Documents
- Select a patient
- Go to "Documents" tab
- Upload PDF, TXT, or image files
- Documents are automatically parsed and stored

### 3. Record Vitals
- Go to "Vitals" tab
- Enter patient vital signs
- All fields are optional
- Data is validated before storage

### 4. Add Family History
- Go to "Family History" tab
- Enter condition, relation, and other details
- Multiple entries can be added

### 5. Upload Medical Images
- Go to "Images" tab
- Upload medical images
- Add description and type

### 6. Chat with Medical Assistant
- Go to "Chatbot" tab
- Ask questions about the patient
- The chatbot uses all stored patient data as context

## Project Structure

```
Medical System/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database models
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── agents/               # Agent implementations
│   ├── __init__.py
│   ├── master_agent.py   # Master agent controller
│   ├── document_agent.py
│   ├── vitals_agent.py
│   ├── family_history_agent.py
│   ├── chatbot_agent.py
│   └── image_agent.py
├── templates/            # HTML templates
│   ├── index.html        # Dashboard
│   └── patient_detail.html
└── uploads/              # Uploaded files (created automatically)
    ├── documents/
    └── images/
```

## API Endpoints

### Patients
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Create new patient
- `GET /api/patients/<id>` - Get patient by ID
- `GET /api/patients/<id>/context` - Get full patient context

### Documents
- `POST /api/patients/<id>/documents` - Upload document
- `GET /api/patients/<id>/documents` - Get all documents

### Vitals
- `POST /api/patients/<id>/vitals` - Record vitals
- `GET /api/patients/<id>/vitals` - Get all vitals

### Family History
- `POST /api/patients/<id>/family-history` - Add family history
- `GET /api/patients/<id>/family-history` - Get family history

### Images
- `POST /api/patients/<id>/images` - Upload image
- `GET /api/patients/<id>/images` - Get all images

### Dental (Teeth Agent)
- `GET /api/patients/<id>/teeth` - Get saved tooth annotations
- `POST /api/patients/<id>/teeth` - Create/Update/Delete a tooth annotation

### Chatbot
- `POST /api/patients/<id>/chat` - Chat with medical assistant

## Customizing Models

The chatbot agent uses Hugging Face models. To change the model:

1. Edit `agents/chatbot_agent.py`
2. Change the `model_name` variable:
   ```python
   self.model_name = "your-model-name"
   ```
3. Popular alternatives:
   - `microsoft/DialoGPT-large`
   - `facebook/blenderbot-400M-distill`
   - `google/flan-t5-base`

## Database

The application uses SQLite by default. To use PostgreSQL or MySQL:

1. Update `config.py` with your database URL
2. Install appropriate database driver:
   - PostgreSQL: `pip install psycopg2-binary`
   - MySQL: `pip install pymysql`

## Security Notes

⚠️ **Important**: This is a development system. For production use:
- Change the SECRET_KEY
- Use a production database
- Implement authentication/authorization
- Add input sanitization
- Use HTTPS
- Implement file upload size limits
- Add rate limiting

## Troubleshooting

### Tesseract OCR not found
- Ensure Tesseract is installed and in your PATH
- On Windows, you may need to set the path in code:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### Model download issues
- First run will download the model from Hugging Face
- Ensure you have internet connection
- Models can be large (several GB)

### Database errors
- Delete `clinical_assistant.db` to reset the database
- Ensure write permissions in the project directory

## License

This project is created for educational purposes as part of a Final Year Project.

## Support

For issues or questions, please refer to the project documentation or contact the development team.

