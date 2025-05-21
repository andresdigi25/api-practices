# Build stage
FROM node:20-alpine as build

WORKDIR /app

# Install Angular CLI globally
RUN npm install -g @angular/cli@latest

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Build the application
RUN ng build --configuration production

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/dist/scrum-master-bot-frontend /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 