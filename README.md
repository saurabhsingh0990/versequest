# VerseQuest

VerseQuest is an AI-backed lyrics analysis application. It pairs a FastAPI backend with a SvelteKit frontend to analyze song lyrics and return structured meaning, themes, imagery, tone, and cultural notes.

## Features

- Line-by-line lyric explanation
- TL;DR song summary
- Theme and imagery extraction
- Cultural notes and tone classification
- FastAPI backend with Perplexity AI integration
- Responsive SvelteKit frontend

## Tech stack

- Backend: Python, FastAPI, Uvicorn, requests, python-dotenv
- Frontend: SvelteKit, Vite, TypeScript
- Containers: Docker, Docker Compose

## Prerequisites

- Node.js 20+
- Python 3.8+
- Docker and Docker Compose (optional)
- A Perplexity AI API key

## Getting started

### Local development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd versequest
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Create the backend environment file:
   ```bash
   cat > backend/.env <<'EOF'
   PPLX_API_KEY=your_api_key_here
   EOF
   ```

4. Start the backend service:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. Install frontend dependencies:
   ```bash
   cd ../apps/web
   npm install
   ```

6. Start the frontend:
   ```bash
   npm run dev
   ```

7. Open the app in your browser:
   ```text
   http://localhost:5173
   ```

### Docker development

1. Create a root `.env` file with your API key:
   ```bash
   cat > .env <<'EOF'
   PPLX_API_KEY=your_api_key_here
   EOF
   ```

2. Build and start containers:
   ```bash
   docker compose up --build
   ```

3. Access the application:
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`

## Environment variables

- `PPLX_API_KEY` — required by the backend
- `VITE_API_URL` — frontend API endpoint, e.g. `http://localhost:8000/api/explain`

## Project structure

```text
versequest/
├── apps/web/          # SvelteKit frontend
│   ├── src/           # Frontend source files
│   └── static/        # Static assets
├── backend/           # FastAPI backend
│   ├── main.py        # API entrypoint
│   └── requirements.txt
├── docker-compose.yml # Docker setup
└── docs/              # Project documentation
```

## Security

- Keep all API keys and secrets out of version control.
- `.env` files are ignored by the repository.
- Use example files or documentation for config templates.

## Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit your changes.
4. Push and open a pull request.

## License

This project is provided as-is. Add a license file to define terms.
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