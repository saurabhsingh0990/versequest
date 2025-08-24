# VerseQuest - AI-Powered Lyrics-to-Meaning Explainer

VerseQuest is an AI-powered web application that helps users understand the deeper meaning behind song lyrics. Using the Perplexity AI API, it provides comprehensive analysis including themes, imagery, cultural references, and more.

## Features

- Multi-language support:
  - English lyrics analysis
  - Hindi lyrics analysis
  - Auto-language detection
- Detailed meaning explanation for each line
- Theme identification and analysis
- Imagery and metaphor detection
- Cultural context and references
- Quick TL;DR summary
- Song credits and attribution
- Modern, responsive UI

## Tech Stack

### Frontend
- SvelteKit
- TypeScript
- Vite

### Backend
- FastAPI (Python)
- Perplexity AI API for lyrics analysis

### DevOps
- Docker
- Docker Compose
- GitHub Actions for CI/CD

## Prerequisites

- Node.js (v20 or later)
- Python 3.8 or later
- Docker and Docker Compose (for containerized setup)
- Perplexity AI API key

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Node.js v20 or later
- Python 3.8 or later
- Docker and Docker Compose (for containerized setup)
- A Perplexity AI API key

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/saurabhsingh0990/versequest.git
   cd versequest
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure backend environment:
   ```bash
   # Create .env file in backend directory
   echo "PPLX_API_KEY=your_api_key_here" > .env
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Set up the frontend:
   ```bash
   cd ../apps/web
   npm install
   ```

6. Configure frontend environment:
   ```bash
   # Create .env file in apps/web directory
   echo "VITE_API_URL=http://localhost:8000/api/explain" > .env
   ```

7. Start the frontend development server:
   ```bash
   npm run dev
   ```

8. Open http://localhost:5173 in your browser

### Docker Deployment

1. Clone the repository (if not already done):
   ```bash
   git clone https://github.com/saurabhsingh0990/versequest.git
   cd versequest
   ```

2. Create environment file:
   ```bash
   # Create .env file in root directory
   echo "PPLX_API_KEY=your_api_key_here" > .env
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

### Stopping the Application

- For local development: Press Ctrl+C in both terminal windows
- For Docker: Run `docker-compose down`

## Tech Stack

### Backend
- FastAPI - Modern Python web framework
- Perplexity AI API - AI-powered lyrics analysis
- Python 3.8+ - Core language
- Uvicorn - ASGI server
- Poetry - Dependency management

### Frontend
- SvelteKit - Full-stack Svelte framework
- Vite - Build tool and dev server
- TypeScript - Type-safe JavaScript
- TailwindCSS - Utility-first CSS
- DaisyUI - Tailwind CSS component library

### DevOps
- Docker - Containerization
- Docker Compose - Multi-container orchestration
- GitHub Actions - CI/CD pipeline

## Development

### Project Structure

```
├── backend/              # FastAPI backend service
│   ├── app/             # Application package
│   │   ├── api/        # API endpoints
│   │   ├── core/       # Core functionality
│   │   └── services/   # Business logic
│   ├── tests/          # Backend tests
│   └── requirements.txt # Python dependencies
├── apps/
│   └── web/            # SvelteKit frontend
│       ├── src/        # Source code
│       │   ├── lib/    # Shared components
│       │   └── routes/ # Page routes
│       └── static/     # Static assets
├── docs/               # Documentation
└── docker-compose.yml  # Docker configuration
```

### Development Workflow

1. Create feature branches from `main`
2. Follow conventional commits
3. Write tests for new features
4. Update documentation as needed
5. Submit PRs for review

### Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Use Prettier and ESLint
- Commit messages: Conventional Commits

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Perplexity AI](https://www.perplexity.ai/) for their powerful AI API
- [SvelteKit](https://kit.svelte.dev/) for the amazing frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient backend framework