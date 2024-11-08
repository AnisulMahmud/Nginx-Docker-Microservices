# Nginx-Docker-Microservices
This project sets up a Dockerized microservices architecture using NGINX as a reverse proxy and load balancer. The system includes multiple instances of service containers (service1 and service2), with NGINX managing authentication, load balancing, and routing.

## Features
* Load Balancing: NGINX balances requests across three service1 instances (service1-1, service1-2, service1-3) running on port 8199.
* Basic Authentication: Protects the app with username and password from the .htpasswd file.
* Stop Button: Allows stopping service1-2 gracefully . This functionality will be updated soon to allow stopping all services.
* Request Button: When you visit http://localhost:8198, you can click on the Request button. This sends a request to the backend services after a 2-second delay.


## How to Use

a. Run the following command to build and start the services:
-> docker-compose up --build ( in the root)


b. Visit http://localhost:8198. You’ll be prompted for login. Enter the credentials given in login.txt.


c. Click the Request button to send a request to the backend. There will be a 2-second delay before the request is processed.


d. Click the Stop button to stop service1-2. The full shutdown of all services will be implemented soon.

### Troubleshooting Login
If the login popup does not appear, clear your browser cache.

### Stop All Services
Use docker-compose down to stop all containers.