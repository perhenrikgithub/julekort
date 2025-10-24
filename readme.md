# Julepost

A lightweight web application for creating and sending digital Christmas cards via email.

## Development

### 1. Virtual Environment and Dependencies

Create and activate a Python virtual environment, then install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 2. SCSS Compilation

To automatically compile SCSS files to CSS during development, run:

```bash
sass --watch static/scss/:static/css/ --style expanded --no-source-map
```

### 3. Environment Variables

Create a `.env` file in the project root with the following content, replacing the placeholders with your actual Gmail address, app password, and application URL (localhost or deployed URL):

```
GMAIL_USER="mailaddress@gmail.com"
GMAIL_APP_PASSWORD="xxxx yyyy zzzz qqqq"
APP_URL="http://theURL:port_if_needed.com"
```

> <b>Note:</b> [Gmail App Password](https://support.google.com/accounts/answer/185833)

### 4. Running the Application Locally

To start the FastAPI server with automatic reload enabled:

```bash
uvicorn main:app --reload
```

## Docker Containerization

Julepost can be run inside a Docker container for easier deployment and environment consistency.

#### Environment Variables

Ensure you have a `.env` file in the project root with the necessary environment variables as described [above](#3-environment-variables).

#### Build and Run

```bash
docker compose up --build -d
```

The application should be accessible at `http://APP_URL` by default, where `APP_URL` is defined in your `.env` file.
