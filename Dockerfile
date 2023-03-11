# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster
# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
# Environment variables required:
# - WEED_ALLOWED_GUILDS: comma-separated list of allowed guild IDs
# - WEED_DEBUG: "True" or "False"
# - TOKEN: your bot token
# - OPENAI_API_KEY: your OpenAI API key
# Run bot.py when the container launches
CMD ["python", "bot.py"]
