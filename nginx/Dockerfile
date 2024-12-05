


# Base NGINX image
FROM nginx:alpine

# Remove default nginx.conf
RUN rm /etc/nginx/nginx.conf

# Copy your custom configuration, password file, and index.html
COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd
COPY index.html /usr/share/nginx/html/index.html

# Expose the port
EXPOSE 80
