FROM python:3.9

# Install Postgresql Client. The image runs on Linux VM so the syntax.
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
COPY ./examples ./examples

# Copy entrypoint
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Declare entry point
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Run the app
CMD [ "uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]