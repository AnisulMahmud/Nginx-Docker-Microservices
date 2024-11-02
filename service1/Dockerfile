FROM openjdk:17-jdk-alpine


# Set the working directory
WORKDIR /app

# Copy the current directory contents intot the container at /app
COPY src/ /app/src/

# Compile the java program
RUN javac src/Main.java


# Expose the port
EXPOSE 8199

# Specify the entry point to run the compiled java class
ENTRYPOINT [ "java", "-cp", "src", "Main" ]
