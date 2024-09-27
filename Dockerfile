# Use Python 3.10 slim image as the base
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc \
      curl \
      && apt-get clean \
      && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy the entire project into the container, excluding files in .dockerignore
COPY . /app

# Configure Poetry: Do not create a virtual environment as the container itself provides isolation
RUN poetry config virtualenvs.create false \
      && poetry install --no-dev --no-interaction --no-ansi

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the FastAPI application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]