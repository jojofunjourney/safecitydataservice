# Use the official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
      build-essential \
      libpq-dev \
      curl \
      && rm -rf /var/lib/apt/lists/*

# Install Poetry explicitly into /root/.local/bin
RUN curl -sSL https://install.python-poetry.org | python3 - \
      && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY . /app

# Debug: Check contents of /app after copying files
RUN echo "Contents of /app after copying files:" && ls -la /app

# Install dependencies without creating virtual environments
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Debug: Check contents of /app after installing dependencies
RUN echo "Contents of /app after installing dependencies:" && ls -la /app

# Expose port 8080 for the container
EXPOSE 8080

# Use ENTRYPOINT for dynamic environment-specific commands
ENTRYPOINT ["sh", "-c", "poetry run uvicorn app.main:app --host 0.0.0.0"]

# CMD can be overridden to specify the mode (e.g., local, prod, or stage)
# CMD ["--reload"]
