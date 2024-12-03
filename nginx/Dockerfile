FROM nginx:stable-alpine

# Copy NGINX configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy authentication file
COPY .htpasswd /etc/nginx/.htpasswd

# Copy the web application frontend files
COPY index.html /usr/share/nginx/html
