FROM python:3.9

# Set the working directory
WORKDIR /app

COPY requirements.txt /app/

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential

# Copy the local app folder to the container
COPY ./app /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["/bin/sh", "-c", "/wait-for-it.sh db:3306 -- &&  alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
