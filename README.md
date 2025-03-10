# Drone Fleet Management Microservice

A modern, containerized Flask microservice for managing drone fleet data. This service provides a RESTful API for tracking drone specifications, maintenance records, and regulatory compliance information.

## Features

- 🛸 Comprehensive drone fleet management
- 📊 Detailed technical specifications tracking
- 🔧 Maintenance history logging
- 📝 Regulatory compliance management
- 🔐 Vendor relationship tracking
- 📡 Equipment and sensor management
- 🚀 Built with modern Python practices

## Tech Stack

- **Framework:** Flask 3.0
- **Database:** PostgreSQL 14
- **ORM:** SQLAlchemy 2.0
- **API Documentation:** Swagger/OpenAPI
- **Containerization:** Docker & Docker Compose
- **Schema Validation:** Marshmallow
- **Development Tools:** Black, Flake8, Pytest

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pshakespeare/Drone-Fleet-Management-Microservice.git
   cd drone_db
   ```

2. **Start the services:**
   ```bash
   docker compose up --build
   ```

3. **Access the API:**
   - API Endpoints: `http://localhost:5000/api/v1`
   - Swagger Documentation: `http://localhost:5000/api/docs`

## API Endpoints

- `/api/v1/drones`: Manage drone fleet
- `/api/v1/vendors`: Manage vendor relationships
- `/api/v1/maintenance`: Track maintenance records
- `/api/v1/equipment`: Manage drone equipment
- Full API documentation available via Swagger UI

## Development

1. **Local Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Copy `.env.example` to `.env` and configure:
   ```
   FLASK_APP=wsgi.py
   FLASK_ENV=development
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=drone_db_dev
   ```

3. **Database Migrations:**
   ```bash
   flask db upgrade
   ```

4. **Run Tests:**
   ```bash
   pytest
   ```

5. **Code Quality:**
   ```bash
   black .
   flake8
   ```

## Docker Support

- **Development:**
  ```bash
  docker compose up --build
  ```

- **Production:**
  ```bash
  docker compose -f docker-compose.prod.yml up --build
  ```

## Project Structure
```
drone_db/
├── app/
│   ├── api/          # API routes and controllers
│   ├── models/       # Database models
│   ├── schemas/      # Marshmallow schemas
│   ├── services/     # Business logic
│   ├── swagger/      # API documentation
│   └── utils/        # Utility functions
├── migrations/       # Database migrations
├── tests/           # Test suite
├── Dockerfile       # Container definition
└── docker-compose.yml
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
