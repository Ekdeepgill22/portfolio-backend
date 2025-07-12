# Portfolio Backend API

A production-ready FastAPI backend for a portfolio website with contact form submissions and static file hosting, featuring MongoDB integration and organized project structure.

## Features

- **Contact Form API**: Secure contact form submissions with validation and MongoDB storage
- **Static File Serving**: Resume PDF downloads and certification image hosting
- **MongoDB Integration**: Async database operations with Motor driver
- **CORS Support**: Configured for frontend integration
- **Production Ready**: Proper logging, error handling, and Docker support
- **Input Validation**: Pydantic models with sanitization
- **Health Checks**: Monitoring endpoints for service health

## Project Structure

```
backend/
├── app/
│   ├── main.py               # FastAPI app instance
│   ├── models.py             # Pydantic models
│   ├── config.py             # Settings and environment variables
│   ├── routes/
│   │   ├── contact.py        # Contact form endpoints
│   │   └── static.py         # Static file serving
│   ├── services/
│   │   └── db.py             # MongoDB connection and operations
│   └── static/
│       ├── resume/
│       │   └── resume.pdf    # Resume file
│       └── certifications/
│           ├── cert1.png     # Certificate images
│           └── cert2.png
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── Dockerfile               # Docker container configuration
├── docker-compose.yml       # Multi-container setup
├── mongo-init.js            # MongoDB initialization
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/portfolio_db
DATABASE_NAME=portfolio_db

# CORS Configuration
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000", "https://your-portfolio.vercel.app"]

# Environment
ENVIRONMENT=development

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Portfolio Backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup MongoDB

**Option A: Local MongoDB**
```bash
# Install MongoDB locally or use MongoDB Atlas
# Update MONGODB_URI in .env file
```

**Option B: Docker MongoDB**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### 4. Create Static Directories

```bash
mkdir -p app/static/resume
mkdir -p app/static/certifications

# Add your resume.pdf to app/static/resume/
# Add certificate images to app/static/certifications/
```

### 5. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build

```bash
# Build the image
docker build -t portfolio-backend .

# Run the container
docker run -p 8000:8000 -e MONGODB_URI=mongodb://host.docker.internal:27017/portfolio_db portfolio-backend
```

## API Endpoints

### Contact Form
- **POST** `/api/v1/contact` - Submit contact form
- **GET** `/api/v1/contact/health` - Health check

### Static Files
- **GET** `/api/v1/resume` - Download resume PDF
- **GET** `/api/v1/static/resume/resume.pdf` - Direct resume link
- **GET** `/api/v1/certifications` - List all certifications
- **GET** `/api/v1/static/certifications/{filename}` - Serve certification image

### General
- **GET** `/` - API information
- **GET** `/health` - Application health check
- **GET** `/docs` - API documentation (development only)

## Frontend Integration

### Contact Form Example

```typescript
// Contact.tsx
const submitContactForm = async (formData: ContactFormData) => {
  try {
    const response = await fetch('http://localhost:8000/api/v1/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    
    if (!response.ok) {
      throw new Error('Failed to submit form');
    }
    
    const result = await response.json();
    console.log('Form submitted successfully:', result);
    
  } catch (error) {
    console.error('Error submitting form:', error);
  }
};
```

### Resume Download

```typescript
// Resume download link
<a href="http://localhost:8000/api/v1/resume" download>
  Download Resume
</a>
```

### Certifications Display

```typescript
// Fetch certifications
const fetchCertifications = async () => {
  const response = await fetch('http://localhost:8000/api/v1/certifications');
  const data = await response.json();
  return data.certifications;
};

// Display certification images
certifications.map(cert => (
  <img 
    key={cert.filename}
    src={`http://localhost:8000${cert.url}`}
    alt={cert.filename}
  />
))
```

## Database Schema

### Contacts Collection

```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string",
  "subject": "string",
  "message": "string",
  "created_at": "datetime",
  "ip_address": "string",
  "user_agent": "string"
}
```

## Security Features

- Input validation and sanitization
- HTML tag removal from user inputs
- Email validation
- Rate limiting ready (can be added with slowapi)
- CORS configuration
- Request logging with IP tracking

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Quality

```bash
# Format code
black app/
isort app/

# Linting
flake8 app/
mypy app/
```

## Production Deployment

### Environment Variables

```env
MONGODB_URI=mongodb://username:password@host:port/database
DATABASE_NAME=portfolio_db
ENVIRONMENT=production
CORS_ORIGINS=["https://your-portfolio.com"]
```

### Performance Optimization

1. **Database Indexes**: Already configured for email and created_at
2. **Static File Caching**: Configure CDN for static files
3. **Connection Pooling**: Motor handles this automatically
4. **Logging**: Configure structured logging for production

### Monitoring

- Health check endpoints at `/health`
- Service-specific health checks
- Request logging with correlation IDs
- Database connection monitoring

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB is running
   - Verify connection string in .env
   - Ensure network connectivity

2. **Static Files Not Found**
   - Verify files exist in app/static/ directories
   - Check file permissions
   - Ensure correct file paths

3. **CORS Issues**
   - Update CORS_ORIGINS in .env
   - Verify frontend URL is included
   - Check browser console for CORS errors

### Logs

```bash
# View application logs
docker-compose logs -f backend

# View MongoDB logs
docker-compose logs -f mongodb
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please create an issue in the GitHub repository.