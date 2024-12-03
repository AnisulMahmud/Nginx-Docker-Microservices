# FROM nginx:stable-alpine

# # Copy NGINX configuration file
# COPY nginx.conf /etc/nginx/nginx.conf

# # Copy authentication file
# COPY .htpasswd /etc/nginx/.htpasswd

# # Copy the web application frontend files
# COPY index.html /usr/share/nginx/html
FROM nginx:stable-alpine

# Ensure correct permissions
RUN chmod 644 /etc/nginx/nginx.conf

# Copy files with explicit permissions
COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf
COPY --chown=nginx:nginx .htpasswd /etc/nginx/.htpasswd
COPY --chown=nginx:nginx index.html /usr/share/nginx/html/index.html