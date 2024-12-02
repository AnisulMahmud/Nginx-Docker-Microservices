# Use Node.js image
FROM node:14

# Set working directory
WORKDIR /app

# Copy app files
COPY app.js .

# Install required dependencies
RUN npm install express

# Expose the required port
EXPOSE 8200

# Command to run the app
CMD ["node", "app.js"]
