# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the local poetry.lock and pyproject.toml to the container at /app
COPY poetry.lock pyproject.toml /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install

# Copy the local code to the container at /app
COPY . /app