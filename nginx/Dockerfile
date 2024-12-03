# # FROM nginx:stable-alpine

# # # Copy NGINX configuration file
# # COPY nginx.conf /etc/nginx/nginx.conf

# # # Copy authentication file
# # COPY .htpasswd /etc/nginx/.htpasswd

# # # Copy the web application frontend files
# # COPY index.html /usr/share/nginx/html
# FROM nginx:stable-alpine

# # Ensure correct permissions
# RUN chmod 644 /etc/nginx/nginx.conf

# # Copy files with explicit permissions
# COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf
# COPY --chown=nginx:nginx .htpasswd /etc/nginx/.htpasswd
# COPY --chown=nginx:nginx index.html /usr/share/nginx/html/index.html


FROM nginx:alpine

# Remove existing files
RUN rm -f /etc/nginx/nginx.conf /etc/nginx/.htpasswd /usr/share/nginx/html/index.html

# Create necessary directories
RUN mkdir -p /etc/nginx /usr/share/nginx/html

# Copy files with explicit permissions
COPY nginx.conf /etc/nginx/nginx.conf
COPY .htpasswd /etc/nginx/.htpasswd
COPY index.html /usr/share/nginx/html/index.html

# Set correct permissions
RUN chmod 644 /etc/nginx/nginx.conf /etc/nginx/.htpasswd /usr/share/nginx/html/index.html