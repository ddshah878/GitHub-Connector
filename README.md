# GitHub Cloud Connector

A simple backend connector that talks to the GitHub API. Built with Python and FastAPI. You give it your GitHub token, and it lets you fetch repos, manage issues, and view commits through clean REST endpoints.

---

## What it does

- Fetch repositories for any GitHub user or organisation
- List and create issues in a repository
- Fetch commits from a repository

---

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/ddshah878/GitHub-Connector.git
cd GitHub-Connector
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 3. Add your GitHub token

Create a `.env` file in the root folder:

```
GITHUB_TOKEN=ghp_your_token_here
```

You can generate a token at https://github.com/settings/tokens — just make sure to give it the `repo` scope.

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to explore and test all endpoints interactively.

---

## API Endpoints

### Repositories

```
GET /repos/?username=ddshah878
```

### Issues

```
GET  /issues/{owner}/{repo}          # list issues
POST /issues/{owner}/{repo}          # create an issue
```

Example body for creating an issue:
```json
{
  "title": "Something is broken",
  "body": "Here is what happened...",
  "labels": ["bug"]
}
```

### Commits

```
GET /commits/{owner}/{repo}
```

---

## Project structure

```
app/
├── main.py            # app entry point
├── config.py          # loads env variables
├── github_client.py   # handles all GitHub API calls
├── models/
│   └── schemas.py     # request and response shapes
└── routes/
    ├── repos.py
    ├── issues.py
    └── commits.py
```

---

## Notes

- The GitHub token is loaded from `.env` and not hardcoded
- All errors from GitHub (invalid token, not found, etc.) return clear messages
- Swagger UI at `/docs` lets you test everything without any extra tooling
