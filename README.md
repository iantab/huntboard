# HuntBoard

A full-stack job application tracker built as a portfolio project. Manage your job search with a drag-and-drop Kanban board, contact tracking, and interview scheduling.

## Tech Stack

**Frontend**
- React 19, TypeScript, Vite, Bun
- Tailwind CSS 4, dnd-kit, TanStack Query, React Router 7

**Backend**
- Django 5.2, Django REST Framework, SimpleJWT
- PostgreSQL, django-filter, django-cors-headers

## Features

- **Kanban board** — drag-and-drop cards across status columns (Wishlist, Applied, Interviewing, Offer, Rejected)
- **JWT authentication** — secure login with automatic token refresh
- **Application CRUD** — create and manage job applications with linked contacts and interview records
- **Filtering & search** — filter applications by status, company, role, and date
- **Status history** — automatic audit log of every status change per application

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+ and [Bun](https://bun.sh)
- PostgreSQL 15+

### Backend

```bash
cd server

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp ../.env.example ../.env
# Edit .env with your database credentials and secret key

# Run migrations and start the development server
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v1`.

### Frontend

```bash
cd client

# Install dependencies
bun install

# Configure environment variables
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > .env

# Start the development server
bun run dev
```

The app will be available at `http://localhost:5173`.
