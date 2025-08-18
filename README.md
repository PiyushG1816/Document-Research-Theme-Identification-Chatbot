# Document-Research-Theme-Identification-Chatbot 

A Document-Research-Theme-Identification-Chatbot is a system that allows users to upload documents and query them using natural language. The system extracts relevant information from documents and provides contextual answers with citations.

## Features

- **Document Upload**: Support for PDF, TXT, and image files (PNG, JPG, JPEG)
- **OCR Processing**: Extracts text from images and scanned documents
- **Semantic Search**: Uses embeddings to find relevant document chunks
- **AI-Powered Answers**: Generates contextual responses using Google's Gemini AI
- **Citation Tracking**: Provides page, paragraph, and sentence-level citations
- **Web Interface**: Clean React frontend for easy interaction

## Tech Stack

### Backend
- **FastAPI**: Web framework for the API
- **ChromaDB**: Vector database for document storage and similarity search
- **Google Gemini**: Large language model for generating responses
- **Sentence Transformers**: For creating document embeddings
- **OCR Libraries**: Text extraction from images and PDFs

### Frontend
- **React**: User interface framework
- **HTML/CSS**: Styling and layout

## Project Structure

```
project/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py          # Configuration settings
│   │   ├── models/
│   │   │   └── request.py         # Pydantic request models
│   │   ├── services/
│   │   │   ├── chroma.py          # ChromaDB operations
│   │   │   ├── gemini.py          # Gemini AI integration
│   │   │   ├── files.py           # File handling
│   │   │   └── ocr.py             # OCR text extraction
│   │   └── api/
|   |        └──  routes.py        # API endpoints
│   └── main.py                    # FastAPI application entry point
├── frontend/
│   ├── src/
│   │   ├── App.js                 # Main React component
│   │   ├── App.css                # Styling
│   │   └── index.js               # React entry point
│   └── public/
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Google API Key (for Gemini)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Document-Research-Theme-Identification-Chatbot/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file inside backend/:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Run the backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd rag-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://127.0.0.1:8000
   ```

4. **Run the frontend**
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000`

## Usage

### Uploading Documents

1. Open the web interface
2. Set the Backend API URL (default: `http://127.0.0.1:8000`)
3. Choose a file (PDF, TXT, PNG, JPG, JPEG)
4. Click "Upload" button
5. Wait for processing confirmation

### Querying Documents

1. Enter your question in the query field
2. Click "Search" button
3. View results in the table format:
   - **Document ID**: Unique identifier for the document chunk
   - **Theme**: AI-generated topic/theme of the content
   - **Extracted Answer**: Relevant answer to your query
   - **Citations**: Source information (filename, page, paragraph)

## API Endpoints

### POST `/upload/`
Upload and process a document file.

### POST `/query/`
Query uploaded documents.

**Request Body**:
```json
{
  "query": "your question here",
  "top_k": 3
}
```

**Response**:
```json
{
  "results": [
    {
      "document_id": "filename_0",
      "theme": "Topic",
      "extracted_answer": "Answer text",
      "citations": [
        {
          "filename": "document.pdf",
          "page": 1,
          "paragraph": 2,
          "sentence": 1
        }
      ]
    }
  ]
}
```

## Configuration

### Chunking Strategy
- **Chunk Size**: 500 characters
- **Splitting**: By paragraphs and sentences
- **Metadata**: Page, paragraph, and sentence tracking

### Embedding Model
- **Model**: `all-MiniLM-L6-v2`
- **Provider**: Sentence Transformers

### AI Model
- **Model**: `gemini-1.5-flash-latest`
- **Temperature**: 0.3
- **Max Tokens**: 2000

## Troubleshooting

### Common Issues

1. **Blank screen after query**
   - Check browser console for React rendering errors
   - Verify backend is running and accessible
   - Check API URL configuration

2. **Upload fails**
   - Ensure file format is supported
   - Check file size limits
   - Verify backend has write permissions to uploads directory

3. **No results returned**
   - Verify documents were uploaded successfully
   - Check if query is relevant to uploaded content
   - Review ChromaDB storage and embedding process

4. **Gemini API errors**
   - Verify Google API key is valid and has Gemini access
   - Check API rate limits and quotas
   - Review network connectivity

### Debug Mode

Enable detailed logging by checking the browser console for:
- API request/response details
- Data structure information
- Error messages and stack traces

## Limitations

- File size limits depend on server configuration
- OCR accuracy varies with image quality
- Gemini API rate limits apply
- ChromaDB storage is local (not distributed)
- No user authentication or session management

## Future Enhancements

- [ ] User authentication and document ownership
- [ ] Support for more file formats (DOCX, PPTX)
- [ ] Improved OCR with preprocessing
- [ ] Document versioning and update capabilities
- [ ] Advanced search filters and sorting
- [ ] Export results functionality
- [ ] Multi-language support
- [ ] Cloud deployment guides

