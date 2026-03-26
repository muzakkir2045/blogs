# ✍️ Flask Blog Platform

> A full-stack blogging platform where users can write, edit, and publish posts with Markdown formatting — with secure authentication and personal post ownership.

🔗 **[Live Demo](https://blog-platform-xk4c.onrender.com)**

---

## What is this?

A complete blogging web app built from scratch with Flask. Users register, log in, and get their own personal dashboard where they can create and manage blog posts written in Markdown — rendered beautifully on read.

No shared feed, no noise. Just your own space to write.

---

## Features

- **Secure Auth** — Registration and login with PBKDF2-SHA256 password hashing via Werkzeug
- **Personal Dashboard** — Each user sees only their own posts, sorted by most recent
- **Full CRUD** — Create, read, update, and delete blog posts
- **Markdown Support** — Posts are written in Markdown and rendered with `fenced_code`, `tables`, and `extra` extensions
- **Post Ownership** — Users can only edit or delete their own posts (enforced server-side with `abort(403)`)
- **Persistent Sessions** — Login sessions last 7 days via secure cookies
- **Post Excerpts** — Dashboard shows clean text previews with HTML stripped automatically

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Framework | Flask |
| Database ORM | SQLAlchemy |
| Authentication | Flask-Login + Werkzeug |
| Markdown Rendering | `markdown` (Python) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Deployment | Render |

---

## Project Structure

```
blogs/
│
├── app.py              # All routes and application logic
├── templates/
│   ├── sign_up.html    # Registration page
│   ├── login.html      # Login page
│   ├── dashboard.html  # User's post dashboard
│   ├── new_blog.html   # Create new post
│   ├── edit_blog.html  # Edit existing post
│   └── post.html       # Full post view with Markdown rendering
├── static/             # CSS and assets
├── instance/           # SQLite database (gitignored)
├── requirements.txt
└── .env                # Secret key and DB URL (gitignored)
```

---

## Getting Started

```bash
git clone https://github.com/muzakkir2045/blogs.git
cd blogs
pip install -r requirements.txt
```

Create a `.env` file:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///instance/database.db   # or PostgreSQL URL for production
```

Run the app:
```bash
flask run
```

Visit `http://localhost:5000`

---

## Screenshots

*Coming soon — dashboard, post editor, and post view.*

---

## A Few Technical Highlights

**Ownership enforcement** — Every edit and delete route checks `post.user_id != current_user.id` and returns a `403 Forbidden` if they don't match. Security isn't just at login.

**Smart excerpt generation** — The `make_excerpt()` function strips HTML tags with regex and collapses whitespace before truncating, so dashboard previews are always clean plain text regardless of what Markdown was used.

**Markdown rendering** — Posts support fenced code blocks, tables, and extended syntax via the `markdown` library's extension system.

---

*Built with Flask and SQLite. Deployed on Render.*
