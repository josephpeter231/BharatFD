# FAQ Project Documentation

## Overview

A Django-based FAQ management system that supports multilingual questions and answers with automatic translation capabilities. The project uses Django REST Framework for API endpoints and includes caching for better performance.

## Features

- Multilingual FAQ support (100+ languages)
- Rich text editor (CKEditor) for answers
- Automatic translation using Google Translate API
- Caching system for improved performance
- REST API endpoints
- Custom exception handling with redirection
- HTML stripping for clean answer display
- Admin interface for FAQ management

## Installation

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  
venv\Scripts\activate

# 2. Install required packages
pip install django==4.2.9
pip install djangorestframework
pip install django-ckeditor
pip install googletrans==3.1.0a0

# 3. Clone the project (if from repository)
git clone <repository-url>
cd faq_project

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver
```

## Project Structure

```markdown
faq_project/
├── faq/                    # Main application
│   ├── migrations/         # Database migrations
│   ├── admin.py           # Admin interface configuration
│   ├── models.py          # FAQ data model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL routing
│   └── tests.py           # Unit tests
└── faq_project/           # Project settings
    ├── settings.py        # Project configuration
    ├── urls.py            # Main URL routing
    └── wsgi.py            # WSGI configuration
```

## API Endpoints

### 1. FAQ List Endpoint

- **URL**: `/api/faqs/`
- **Method**: GET
- **Query Parameters**:
  -----------------

lang: Language code (e.g., 'en', 'hi', 'bn')

- **Response Format**:

```json
[
    {
        "question": "Translated question",
        "answer": "Translated answer"
    }
]
```

## Database Schema

### FAQ Model

```python
class FAQ:
    question_en: TextField      # Required
    question_hi: TextField      # Optional
    question_bn: TextField      # Optional
    answer: RichTextField      # Required
```

## Admin Interface

The admin interface is configured with:

- List display showing English questions
- Fieldsets for organizing input fields:
  - Main fields (English question and answer)
  - Translations (Hindi and Bengali questions)
- Automatic cache clearing on save

### Access Admin Interface

1. Go to `/admin/`
2. Login with superuser credentials
3. Manage FAQ entries

## Caching

The project uses Django's local memory cache:

- Cache is automatically cleared when FAQ entries are updated
- Configured in settings.py with LocMemCache backend

## Exception Handling

Custom exception handler provides:

- Redirect to FAQ list for 404 errors
- Default English language fallback
- Error logging for failed translations

## Testing

Run tests using:

```bash
python manage.py test ]
```

Test cases cover:

- Empty FAQ list handling
- Single FAQ retrieval
- Multiple FAQs retrieval
- List ordering
- Translation functionality
- English fallback
- HTML stripping

## Usage Examples

### 1. Creating FAQ via Admin Interface

1. Access `/admin/`
2. Navigate to FAQs
3. Click "Add FAQ"
4. Fill in English question and answer
5. Optional: Add translations
6. Save

### 2. Accessing FAQs via API

```bash
# Get FAQs in English
curl http://localhost:8000/api/faqs/

# Get FAQs in Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Get FAQs in Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

## Security Considerations

- Debug mode should be disabled in production
- Secret key should be changed in production
- ALLOWED_HOSTS should be properly configured
- Consider rate limiting for API endpoints
- Implement proper authentication for production use
