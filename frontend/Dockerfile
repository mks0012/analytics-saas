FROM node:20-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Build the Next.js app
RUN npm run build

# Expose the Next.js port
EXPOSE 3000

# Start the application
CMD ["npm", "run", "start"]