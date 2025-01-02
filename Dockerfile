# Official Python runtime as the base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Node.js dependencies for Tailwind CSS
COPY package.json package-lock.json /app/
RUN npm install

# Copy .env file 
COPY .env /app/.env

# Copy the entire project to the container
COPY . /app/

# Build Tailwind CSS
RUN npm run build:tailwind

# Collect static files
RUN python manage.py collectstatic --noinput


# Expose the application's port
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taskify.wsgi:application"]
