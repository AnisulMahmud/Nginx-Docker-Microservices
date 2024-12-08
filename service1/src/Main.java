import java.io.*;
import java.net.*;
import java.util.Date;
import java.util.stream.*;

public class Main {
    private static final String SERVICE2_REQUEST_URL = "http://service2:5000/request";


    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(8199)) {
            System.err.println("Service1 is running on port 8199");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                new Thread(() -> {
                    try {
                        handleRequest(clientSocket);
                    } catch (Exception e) {
                        System.err.println("Error handling request: " + e.getMessage());
                    }
                }).start();
            }
        } catch (IOException e) {
            System.err.println("Could not start server: " + e.getMessage());
        }
    }

    // Handles incoming client requests and routes them based on the request 
    private static void handleRequest(Socket clientSocket) throws Exception {
        try (OutputStream output = clientSocket.getOutputStream();
             PrintWriter writer = new PrintWriter(output, true);
             BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))) {

            String requestLine = reader.readLine();
            if (requestLine != null && requestLine.contains("GET /api/")) {
                String service1Info = getService1Info();
                String service2Info = getService2Info();

                writer.println("HTTP/1.1 200 OK");
                writer.println("Content-Type: application/json");
                writer.println("Connection: close");
                writer.println();
                writer.println("{\"service1\":" + service1Info + ",\"service2\":" + service2Info + "}");
            } else if (requestLine != null && requestLine.contains("POST /api/stop")) {
                stopDockerCompose();
                writer.println("HTTP/1.1 200 OK");
                writer.println("Content-Type: application/json");
                writer.println("Connection: close");
                writer.println();
                writer.println("{\"message\":\"System is shutting down...\"}");
            } else {
                writer.println("HTTP/1.1 404 Not Found");
                writer.println("Connection: close");
                writer.println();
            }
        } finally {
            clientSocket.close();
        }
    }


    // Stops the Docker Compose services and shuts down the application
    private static void stopDockerCompose() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("/bin/sh", "-c", "docker-compose down");
            processBuilder.inheritIO();
            Process process = processBuilder.start();
            process.waitFor();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        } finally {
            System.exit(0);
        }
    }


    // Retrieves information about Service 1
    private static String getService1Info() throws Exception {
        // First, check the state of Service 2
        try {
            URL stateUrl = new URL("http://service2:5000/state");
            HttpURLConnection stateConnection = (HttpURLConnection) stateUrl.openConnection();
            stateConnection.setRequestMethod("GET");
    
            // Service 2 is not in RUNNING state, return an error
            if (stateConnection.getResponseCode() != 200) {
                return "{\"message\":\"Service2 state is unavailable in info\"}";
            }
    
            BufferedReader stateReader = new BufferedReader(new InputStreamReader(stateConnection.getInputStream()));
            String stateResponse = stateReader.readLine();
            stateReader.close();
    
            // Check if the state is not RUNNING
            if (!stateResponse.contains("\"RUNNING\"")) {
                return "{\"message\":\"Service is not in RUNNING state\"}";
            }
    
            // If state is RUNNING, get Service 1 info
            StringBuilder info = new StringBuilder("{");
            InetAddress ip = InetAddress.getLocalHost();
            info.append("\"IpAddress\":\"").append(ip.getHostAddress()).append("\",");
    
            ProcessBuilder processBuilder = new ProcessBuilder("ps", "ax");
            Process process = processBuilder.start();
            info.append("\"Processes\":[").append(outputFromProcess(process)).append("],");
    
            File root = new File("/");
            double freeGB = root.getFreeSpace() / (1024.0 * 1024.0 * 1024.0);
            info.append("\"FreeSpaceGB\":\"").append(String.format("%.2f", freeGB)).append("\",");
            info.append("\"LastBootTime\":\"").append(new Date().toString()).append("\"");
            info.append("}");
            return info.toString();
    
        } catch (Exception e) {
            // Handle any unexpected errors
            return "{\"message\":\"Error checking service state: " + 
                   e.getMessage().replace("\"", "'") + "\"}";
        }
    }

    // Retrieves information about Service 2
    private static String getService2Info() throws Exception {
        // First, check the state of Service 2
        URL stateUrl = new URL(SERVICE2_REQUEST_URL);
        HttpURLConnection stateConnection = (HttpURLConnection) stateUrl.openConnection();
        stateConnection.setRequestMethod("GET");
    
        // If state check fails, return an error message
        if (stateConnection.getResponseCode() != 200) {
            return "{\"message\":\"Service is not in RUNNING state\"}";
        }
    
        // Read the state response
        BufferedReader stateReader = new BufferedReader(new InputStreamReader(stateConnection.getInputStream()));
        String stateResponse = stateReader.readLine();
        stateReader.close();
    
        // Check if the state is not RUNNING
        if (!stateResponse.contains("\"RUNNING\"")) {
            return "{\"message\":\"Service2 is not in RUNNING state\"}";
        }
    
        // If state is RUNNING, proceed to get Service 2 info
        URL service2Url = new URL(SERVICE2_REQUEST_URL);
        HttpURLConnection connection = (HttpURLConnection) service2Url.openConnection();
        connection.setRequestMethod("GET");
    
        if (connection.getResponseCode() != 200) {
            return "{\"message\":\"Service2 is not accessible\"}";
        }
    
        BufferedReader input = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuilder response = new StringBuilder();
        String inputLine;
        while ((inputLine = input.readLine()) != null) {
            response.append(inputLine);
        }
        input.close();
    
        return response.toString();
    }

 

    //Collects and formats the output
    private static String outputFromProcess(Process process) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
        return reader.lines()
                     .map(line -> "\"" + line.replace("\"", "\\\"") + "\"")
                     .collect(Collectors.joining(","));
    }
}
