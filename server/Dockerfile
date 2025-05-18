FROM node:18-alpine

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the server code
COPY . .

# Expose the server port
EXPOSE 5000

# Start the server
CMD ["node", "server.js"] 