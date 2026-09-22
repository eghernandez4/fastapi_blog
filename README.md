# FastAPI Blog

A full-featured blog web application and RESTful API built with **FastAPI**, **SQLAlchemy 2.0 (Async)**, **aiosqlite**, **Pydantic v2**, and **Jinja2** templates.

This project demonstrates core and advanced FastAPI patterns, including asynchronous database operations with SQLAlchemy's `AsyncSession`, lifespan event management, server-side rendered HTML views with Bootstrap 5, dependency injection for database sessions, relational database modeling with cascade operations, dual-mode API/HTML exception handling, and auto-generated interactive OpenAPI documentation.

---

## Features

- **Server-Side Rendered (SSR) Web UI**:
  - Clean, responsive interface styled with **Bootstrap 5**.
  - Dynamic color theme switcher (Light / Dark / Auto modes).
  - Main blog feed with author avatars, publication timestamps, and previews.
  - Dedicated post detail pages.
  - Author post filtering (`/users/{user_id}/posts`).
  - Custom HTML error pages for browser clients.

- **RESTful API**:
  - Full CRUD operations for **Users** and **Posts**.
  - Consistent HTTP status codes (`200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `403 Forbidden`, `404 Not Found`, `422 Unprocessable Content`).
  - Strict input validation and email format verification via Pydantic v2 and `email-validator`.
  - Proper handling of partial updates (`PATCH`) and idempotent full updates (`PUT`).

- **Database & ORM**:
  - Modern **SQLAlchemy 2.0** declarative syntax (`Mapped` and `mapped_column`).
  - Fully asynchronous database layer using `AsyncSession`, `async_sessionmaker`, and `create_async_engine`.
  - Non-blocking SQLite access with **aiosqlite** (`sqlite+aiosqlite:///./blog.db`).
  - FastAPI `lifespan` handler managing asynchronous table creation and engine disposal.
  - Eager relationship loading with `selectinload` for optimized asynchronous queries.
  - Relational mapping between Users and Posts with cascade deletion.
  - Asynchronous dependency-injected session management (`get_db`).

- **Smart Dual-Mode Exception Handling**:
  - Global Starlette and RequestValidationError handlers dynamically detect request paths:
    - Requests to `/api/*` receive structured JSON error bodies.
    - Browser navigation receives styled HTML error templates.

- **Interactive Documentation**:
  - Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`) documentation out of the box.

---

## Tech Stack

| Component | Technology |
|---|---|
| **Language** | Python 3.12+ |
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ASGI Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database / ORM** | SQLite, [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async), [aiosqlite](https://github.com/omnilib/aiosqlite) |
| **Data Validation** | [Pydantic v2](https://docs.pydantic.dev/), `email-validator` |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Frontend Styling** | [Bootstrap 5.3](https://getbootstrap.com/), Google Fonts (Montserrat, Nunito) |

---

## Project Structure

```text
fastapi_blog/
├── database.py         # Async database engine (aiosqlite), Base model, and async get_db dependency
├── models.py           # SQLAlchemy ORM models (User, Post) and relationships
├── schemas.py          # Pydantic schemas for request validation and response serialization
├── main.py             # FastAPI app initialization with lifespan, async routes, static mounts, and error handlers
├── blog.db             # SQLite database file (created automatically on startup)
├── test_main.http      # HTTP requests for testing endpoints in IDE REST clients
├── templates/          # Jinja2 HTML templates
│   ├── layout.html     # Base layout with navbar, theme toggler, and footer
│   ├── home.html       # Blog feed displaying all posts
│   ├── post.html       # Individual post detail page
│   ├── user_posts.html # Posts filtered by author
│   └── error.html      # Custom user-facing error page
├── static/             # Static web assets
│   ├── css/            # Custom CSS stylesheets (main.css)
│   ├── js/             # Client-side JavaScript utilities
│   ├── icons/          # Favicon and site icons
│   └── profile_pics/   # Default fallback profile picture
├── media/              # User uploaded files (profile avatars)
│   └── profile_pics/
└── LICENSE             # MIT License
```

---

## Getting Started

### Prerequisites

- Python 3.12 or newer
- `pip` (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/eghernandez4/fastapi_blog.git
   cd fastapi_blog
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   # On Windows:
   # .venv\Scripts\activate
   ```

3. **Install the required packages:**
   ```bash
   pip install fastapi "uvicorn[standard]" sqlalchemy aiosqlite jinja2 pydantic email-validator
   ```

---

## Running the Application

### Development Server

Run the development server using `fastapi dev` or `uvicorn`:

```bash
fastapi dev main.py
```
*Or:*
```bash
uvicorn main:app --reload
```

The application will start at `http://127.0.0.1:8000`.

### Available URLs

- **Web Blog**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive Swagger UI Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI JSON Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## Endpoints Overview

### Web Pages (Server-Rendered HTML)

| Method | Path | Description |
|---|---|---|
| `GET` | `/` or `/posts` | Home page showing list of recent blog posts |
| `GET` | `/posts/{post_id}` | Detailed view of a single post |
| `GET` | `/users/{user_id}/posts` | List of posts authored by a specific user |

### REST API

#### Users (`/api/users`)

| Method | Endpoint | Status | Description |
|---|---|---|---|
| `POST` | `/api/users` | `201 Created` | Create a new user (`username`, `email`) |
| `GET` | `/api/users/{user_id}` | `200 OK` | Fetch a user by ID |
| `PATCH` | `/api/users/{user_id}` | `200 OK` | Partially update user details (`username`, `email`, `image_file`) |
| `DELETE` | `/api/users/{user_id}` | `204 No Content` | Delete a user (cascades to their posts) |
| `GET` | `/api/users/{user_id}/posts` | `200 OK` | Fetch all posts created by a specific user |

#### Posts (`/api/posts`)

| Method | Endpoint | Status | Description |
|---|---|---|---|
| `GET` | `/api/posts` | `200 OK` | Fetch all posts (includes nested author info) |
| `POST` | `/api/posts` | `201 Created` | Create a new post (`title`, `content`, `user_id`) |
| `GET` | `/api/posts/{post_id}` | `200 OK` | Fetch a single post by ID |
| `PUT` | `/api/posts/{post_id}` | `200 OK` | Full update of a post (title, content, user ID validation) |
| `PATCH` | `/api/posts/{post_id}` | `200 OK` | Partial update of a post (`title`, `content`) |
| `DELETE` | `/api/posts/{post_id}` | `204 No Content` | Delete a post by ID |

---

## Roadmap

- [ ] User authentication and authorization (JWT tokens, password hashing with bcrypt/argon2).
- [ ] User profile picture upload endpoint using `python-multipart`.
- [ ] Web forms and UI actions for creating, editing, and deleting posts directly from the browser.
- [ ] Pagination for blog posts (`limit` and `offset` query parameters).
- [ ] Search functionality and post categories/tags.

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
