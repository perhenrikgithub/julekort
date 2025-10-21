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

Create a `.env` file in the project root directory with the following configuration:

```
GMAIL_USER="mailaddress@gmail.com"
GMAIL_APP_PASSWORD="xxxx yyyy zzzz qqqq"
```

> <b>Note:</b> Use a [Gmail App Password](https://support.google.com/accounts/answer/185833)

### 4. Running the Application

To start the FastAPI server with automatic reload enabled:

```bash
uvicorn main:app --reload
```
