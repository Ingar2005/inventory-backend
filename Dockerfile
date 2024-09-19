FROM python:3
WORKDIR /usr/local/app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Install dependencies
COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y iputils-ping

# Copy the project files
COPY . .

# Expose the desired port
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "app:app"]
