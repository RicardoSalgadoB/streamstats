# Extending airflow to add etl requirements
FROM apache/airflow:3.1.0

# Change user for base installations
USER root

# Install OpenJDK-17
RUN apt update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-arm64/
RUN export JAVA_HOME

# Switch back to airflow user
USER airflow

# Copy ETL requirements
COPY /scripts/requirements.txt /tmp/requirements.txt

# Install additional ETL dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Add your ETL scripts to Python path
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/scripts"