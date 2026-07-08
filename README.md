# FounderAI - Multi-Agent AI Startup Builder

An intelligent platform that transforms startup ideas into comprehensive business blueprints using AI agents powered by CrewAI and Gemini.

## 🚀 Features

- **Multi-Agent System**: Leverages specialized AI agents for market research, business planning, financial modeling, and technical architecture
- **RAG-Powered Insights**: Uses ChromaDB and embeddings for intelligent knowledge retrieval
- **Comprehensive Business Plans**: Generates detailed startup blueprints including market analysis, financial projections, and technical architecture
- **Real-time Progress Tracking**: Monitor agent execution in real-time
- **User Authentication**: Secure JWT-based authentication system

## 📁 Project Structure

```
founderai/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── agents/      # CrewAI agents and tasks
│   │   ├── api/         # API routes
│   │   ├── core/        # Configuration and security
│   │   ├── db/          # Database connections
│   │   ├── models/      # Pydantic models
│   │   ├── rag/         # RAG implementation
│   │   └── repositories/ # Data access layer
│   ├── Dockerfile       # Docker configuration for backend
│   └── requirements.txt # Python dependencies
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # React components
│   │   ├── context/    # React context
│   │   └── pages/      # Page components
│   └── package.json    # Node dependencies
└── render.yaml         # Render deployment configuration
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **CrewAI**: Multi-agent orchestration
- **LiteLLM**: LLM provider abstraction
- **Gemini AI**: Google's AI model for generation
- **MongoDB**: Database for user data and blueprints
- **ChromaDB**: Vector database for RAG
- **JWT**: Authentication

### Frontend
- **React**: UI library
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **Axios**: HTTP client
- **React Router**: Navigation
- **Lucide React**: Icons

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account
- Google Gemini API key
- Serper API key (for web search)

## 🚀 Local Development Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory:
```env
MONGODB_URI=your-mongodb-connection-string
MONGODB_DB_NAME=founderai
JWT_SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
SERPER_API_KEY=your-serper-api-key
FRONTEND_ORIGIN=http://localhost:5173
```

6. Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🌐 Deployment to Render

### Prerequisites
1. GitHub account with your code pushed
2. Render account (free tier works)
3. MongoDB Atlas database
4. API keys (Gemini, Serper)

### Deployment Steps

1. **Push your code to GitHub**:
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**:
   
   The following environment variables need to be set in Render (they are marked with `sync: false` in render.yaml):
   
   **Backend Service**:
   - `MONGODB_URI`: Your MongoDB connection string
   - `JWT_SECRET_KEY`: A secure random string (generate with `openssl rand -hex 32`)
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `SERPER_API_KEY`: Your Serper API key for web search
   - `FRONTEND_ORIGIN`: Your frontend URL (e.g., `https://founderai-frontend.onrender.com`)
   
   **Frontend Service**:
   - `VITE_API_BASE_URL`: Your backend URL (e.g., `https://founderai-backend.onrender.com`)

4. **Deploy**:
   - Click "Apply" to start the deployment
   - Render will build and deploy both services
   - Monitor the deployment logs for any issues

### Getting API Keys

- **MongoDB Atlas**: [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- **Google Gemini**: [ai.google.dev](https://ai.google.dev/)
- **Serper API**: [serper.dev](https://serper.dev/)

## 🐳 Docker Deployment

### Build and run with Docker:

```bash
# Backend
cd backend
docker build -t founderai-backend .
docker run -p 8000:8000 --env-file .env founderai-backend

# Frontend (optional)
cd frontend
docker build -t founderai-frontend .
docker run -p 80:80 founderai-frontend
```

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token

### Profile
- `GET /api/profile/me` - Get current user profile
- `PUT /api/profile/me` - Update user profile

### Blueprint Generation
- `POST /api/generate/blueprint` - Generate startup blueprint
- `GET /api/generate/blueprint/{blueprint_id}` - Get blueprint by ID
- `GET /api/generate/blueprints` - List user's blueprints

### Health Check
- `GET /health` - Service health check
- `GET /` - API information

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

## 🔧 Troubleshooting

### Common Issues

1. **Module Import Errors**:
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **MongoDB Connection Issues**:
   - Check MongoDB URI format
   - Ensure IP whitelist includes your IP (or use 0.0.0.0/0 for development)
   - Verify database user permissions

3. **API Key Errors**:
   - Verify all API keys are set in environment variables
   - Check API key validity and quotas

4. **CORS Issues**:
   - Ensure `FRONTEND_ORIGIN` matches your frontend URL exactly
   - Check that credentials are properly configured

5. **Render Deployment Fails**:
   - Check build logs for specific errors
   - Verify all environment variables are set
   - Ensure `render.yaml` paths are correct

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ using FastAPI, CrewAI, and React
