# Use Python 3.8.5 as the base image
FROM python:3.8.5

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /code/


# Run database migrations
RUN python manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
