# Scrum Master Bot

A voice-enabled Scrum Master bot that helps conduct daily standups with team members. The bot uses Ollama for generating jokes and responses, and provides a web interface for managing standups.

## Features

- Voice input for team member updates
- Automatic joke generation based on updates
- Standup history tracking
- Web interface for managing standups
- Microphone selection
- Team member management

## Prerequisites

### Option 1: Local Development
- Python 3.8+
- Node.js 16+
- Ollama installed and running locally
- Angular CLI installed globally (`npm install -g @angular/cli`)

### Option 2: Docker
- Docker
- Docker Compose
- Ollama installed and running locally

## Project Structure

```
scrum-master-bot/
├── backend/           # FastAPI backend
│   ├── main.py       # Main FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # Angular frontend
│   ├── src/
│   │   └── app/
│   │       ├── app.component.ts
│   │       └── app.module.ts
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```

## Setup and Running

### Option 1: Local Development

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd scrum-master-bot/backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python main.py
   ```

The backend will be available at `http://localhost:8000`

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd scrum-master-bot/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   ng serve
   ```

The frontend will be available at `http://localhost:4200`

### Option 2: Docker Setup

1. Make sure Ollama is running on your host machine
2. Navigate to the project root:
   ```bash
   cd scrum-master-bot
   ```

3. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

The application will be available at:
- Frontend: `http://localhost`
- Backend API: `http://localhost:8000`

## Usage

1. Open your browser and navigate to the frontend URL
2. Select your microphone from the dropdown
3. Start adding team members and their updates
4. Each update will generate a joke
5. End the standup when all team members have provided their updates
6. View standup history in the bottom section

## API Endpoints

- `GET /api/microphones` - List available microphones
- `POST /api/select-microphone` - Select a microphone
- `POST /api/add-team-member` - Add a team member's update
- `POST /api/end-standup` - End the current standup
- `GET /api/standup-history` - Get standup history

## Notes for Docker Users

- The backend container connects to Ollama running on your host machine using `host.docker.internal`
- Standup data is persisted in the `backend/standups` directory
- The frontend container serves the built Angular application through nginx
- API requests from the frontend are automatically proxied to the backend

## Contributing

Feel free to submit issues and enhancement requests! 