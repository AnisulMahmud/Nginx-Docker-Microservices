# Nginx-Docker-Microservices

This project demonstrates a Dockerized microservices architecture with NGINX serving as a reverse proxy and load balancer. The system comprises multiple instances of service containers (service1 and service2), with NGINX managing authentication, load balancing, and routing. A CI/CD pipeline is also integrated to automate the build, test, and deployment processes.

---

## Features
- **Load Balancing:** NGINX balances requests across three service1 instances (`service1-1`, `service1-2`, `service1-3`) running on port 8199.
- **Basic Authentication:** Protects the app with a username and password, configured in the `.htpasswd` file.
- **Stop Button:** Allows stopping `service1-2` gracefully via the browser interface. Future updates will include the functionality to stop all services.
- **Request Button:** Accessible at [http://localhost:8198](http://localhost:8198), the Request button sends a request to the backend services after a 2-second delay.
- **Monitoring and Metrics:** Provides real-time metrics such as service start time, number of requests, and current system state through the `/metrics` endpoint.
- **State Management:** Includes system states like INIT, RUNNING, PAUSED, and SHUTDOWN, with transitions managed through the browser or API.
- **CI/CD Integration:** Automates building, testing, and deploying the system.

---

## How to Use
After cloing follow this steps...

### Build and Start the System
Run the following command in the root directory to build and start all services:
```bash
docker-compose up --build

### Access the Application
1. Visit [http://localhost:8198](http://localhost:8198).  
2. You’ll be prompted for login. Use the credentials provided in the `login.txt` file.  
3. Interact with the following features:
   - **Request Button:** Sends a request to backend services with a 2-second delay.  
   - **Stop Button:** Stops the `service1-2` instance. Full shutdown functionality will be added in future updates.  

---

### Stop All Services
To stop all containers, use:
```bash
docker-compose down


###  Metrics Access
#### Metrics can be accessed via:
Browser: http://localhost:8197/metrics

#### Curl Command:
curl http://localhost:8197/metrics

####  API Testing
#### Test the /state endpoint using the following curl command:
curl -X PUT localhost:8197/state \
-d "PAUSED" \
-H "Content-Type: text/plain" \
-H "Accept: text/plain"


#### Troubleshooting Login
If the login popup does not appear:

Clear your browser cache.
Restart the system using docker-compose down followed by docker-compose up --build


