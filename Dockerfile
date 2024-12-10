# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /gogrok

# Copy the current directory contents into the container at /gogrok 
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port the app runs on
EXPOSE 8000

# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
