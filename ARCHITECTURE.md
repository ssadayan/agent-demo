# Todo List App — Architecture

## Overview

A three-tier architecture (client → API → database) with a stateless REST backend. This pattern fits because a todo app is fundamentally CRUD-driven, and separating concerns across tiers keeps each layer independently deployable and scalable.

## Tech Stack

| Layer    | Technology                |
|----------|---------------------------|
| Frontend | React 18 + Tailwind CSS   |
| Backend  | FastAPI (Python 3.11)     |
| Database | PostgreSQL 15             |
| Auth     | JWT (access/refresh) + bcrypt |
| Deploy   | Vercel (frontend) + Railway (backend + DB) |

## Key Decisions

- **REST over GraphQL** — simpler for CRUD at this scale; no nested query complexity to justify GraphQL overhead
- **PostgreSQL over MongoDB** — todo/user data is relational (foreign keys, filters by status/priority); SQL is the natural fit
- **JWT over sessions** — stateless auth works cleanly across separate Vercel/Railway origins without shared session storage
- **FastAPI over Flask/Django** — async support, automatic OpenAPI docs, Pydantic validation out of the box

## Component Diagram

```
[Browser]
    │
    ▼
[React App]  ──── Vercel (static + SSR)
    │
    │  REST + JWT Bearer
    ▼
[FastAPI]  ──── Railway (container)
    │  ├── /auth  (login, register, refresh)
    │  ├── /todos (CRUD + filters)
    │  └── middleware: JWT validation
    ▼
[PostgreSQL 15]  ──── Railway (managed)
```

## Database Schema

```sql
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE todos (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title      VARCHAR(500) NOT NULL,
    priority   SMALLINT DEFAULT 0 CHECK (priority BETWEEN 0 AND 2),
    status     VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending','in_progress','done')),
    due_date   DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_todos_user_status ON todos(user_id, status);
```
