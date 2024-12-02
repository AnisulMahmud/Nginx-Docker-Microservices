# Use the official Nginx image as a base
FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

# COPY index.html /usr/share/nginx/html/

# RUN apk add --no-cache apache2-utils


# Copy the .htpasswd file for basic authentication
COPY .htpasswd /etc/nginx/.htpasswd

# Copy the index.html file directly into Nginx's html folder
COPY index.html /usr/share/nginx/html/

# Expose the port Nginx will run on
EXPOSE 8198

# Command to run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
