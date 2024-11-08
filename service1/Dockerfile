FROM openjdk:17-jdk-alpine

# Install Docker CLI and Docker Compose
RUN apk add --no-cache docker-cli docker-compose

# Set the working directory
WORKDIR /app

# Copy the source code and the shutdown script into the container
COPY src/ /app/src/


# Compile the Java program
RUN javac src/Main.java

# Expose the port used by service1
EXPOSE 8199

# Specify the entry point to run the Java application
ENTRYPOINT ["java", "-cp", "src", "Main"]


