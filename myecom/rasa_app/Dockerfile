# Use official Rasa image
FROM rasa/rasa:3.6.2

# Set working directory
WORKDIR /app

# Copy your Rasa project (domain.yml, config.yml, data/, models/, etc.)
COPY . /app

# Expose Rasa’s default API port
EXPOSE 5005

# Run Rasa server with API enabled and CORS open
CMD ["rasa", "run", "--enable-api", "--cors", "*", "-p", "5005"]
