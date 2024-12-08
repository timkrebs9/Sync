# Sync API

[![CI/CD Pipeline](https://github.com/timkrebs9/Sync/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/timkrebs9/Sync/actions/workflows/ci-cd.yml)

[![Development Integration Pipeline](https://github.com/timkrebs9/Sync/actions/workflows/dev-integration.yml/badge.svg?branch=dev)](https://github.com/timkrebs9/Sync/actions/workflows/dev-integration.yml)

A FastAPI-based REST API for task management, designed to work with iOS applications. The API is containerized and deployed on Azure Cloud using modern CI/CD practices.

## 🚀 Features

### Current Features

- RESTful API endpoints for task management (CRUD operations)

### Planned Features

- User authentication and authorization

### Prerequisites

- Python 3.11+

### Local Development

1. Clone the repository:

### V1 Endpoints

#### Tasks

- `POST /api/v1/tasks/` - Create a new task

### Manual Deployment

bash

### V2 API Plans

1. **Enhanced Task Management**

## 🏗 Project Structure

The project follows a clean architecture pattern with clear separation of concerns:

## 🛠 Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Testing**: pytest
- **Container**: Docker
- **Cloud**: Azure
- **CI/CD**: GitHub Actions
- **Code Quality**: pre-commit hooks

## 🚦 Getting Started

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- PostgreSQL
- Azure CLI (for deployment)

### Local Development

1. Clone the repository:

```bash
git clone https://github.com/your-username/sync.git
cd sync
```

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
.\venv\Scripts\activate # Windows
```

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up pre-commit hooks:

    ```bash
    pre-commit install
    ```

3. Start the development environment:

    ```bash
    docker-compose up -d
    ````

4. Run tests:

    ```bash
    pytest tests/ -v
    ```

## 🔄 API Endpoints

### V1 Endpoints

#### Tasks

- `POST /api/v1/tasks/` - Create a new task
- `GET /api/v1/tasks/` - List all tasks
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

## 🚀 Deployment

The API is deployed on Azure using Container Registry and App Service. The deployment process is automated through GitHub Actions.

### Manual Deployment

```bash
./scripts/infra-deploy.sh
```

## 🧪 Testing

The project includes comprehensive testing:

- Unit tests
- Integration tests
- API endpoint tests
- Database interaction tests

Run tests with:
bash
pytest tests/ -v



## 📈 Future Enhancements

### V2 API Plans
1. **Enhanced Task Management**
   - Task categories and tags
   - Task priorities
   - Due dates and reminders
   - Recurring tasks

2. **User Management**
   - User registration and authentication
   - Role-based access control
   - User preferences

3. **Data Synchronization**
   - Real-time updates using WebSockets
   - Conflict resolution
   - Offline support

4. **Performance Optimizations**
   - Query optimization
   - Caching layer
   - Rate limiting

5. **Integration Features**
   - Calendar integration
   - Email notifications
   - Third-party app webhooks

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Run pre-commit hooks
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers.