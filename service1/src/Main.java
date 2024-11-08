
import java.io.*;
import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.net.*;
import java.util.Date;
import java.util.stream.*;

public class Main {
    public static void main(String[] args) {
        ServerSocket serverSocket = null;
        try {
            // Create an HTTP server to listen on port 8199
            serverSocket = new ServerSocket(8199);
            System.err.println("Service1 is running on port 8199");

            while (true) {
                try {
                    Socket clientSocket = serverSocket.accept();
                    // Handlint the the request 
                    new Thread(() -> {
                        try {
                            handleRequest(clientSocket);
                        } catch (Exception e) {
                            System.err.println(" - Error handling request: " + e.getMessage());
                        }
                    }).start();
                } catch (IOException e) {
                    System.err.println("Error accepting connection: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Could not start server: " + e.getMessage());
        } finally {
          
            if (serverSocket != null && !serverSocket.isClosed()) {
                try {
                    serverSocket.close();
                    System.err.println("Server socket closed.");
                } catch (IOException e) {
                    System.err.println("Error closing server socket: " + e.getMessage());
                }
            }
        }
    }


    private static void handleRequest(Socket clientSocket) throws Exception {
        try (OutputStream output = clientSocket.getOutputStream();
             PrintWriter writer = new PrintWriter(output, true);
             BufferedReader reader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()))) {
    
            String requestLine = reader.readLine();
    
            if (requestLine.startsWith("POST /api/stop")) {
                // Stop Docker Compose and exit the application
                stopDockerCompose() ;
                
                writer.println("HTTP/1.1 200 OK");
                writer.println("Content-Type: application/json");
                writer.println("Connection: close");
                writer.println();
                writer.println("{\"message\":\"System is shutting down...\"}");
            } else {
                // Regular request handling
                String service1 = getService1Info();
                String service2 = getService2Info();
                writer.println("HTTP/1.1 200 OK");
                writer.println("Content-Type: application/json");
                writer.println("Connection: close");
                writer.println();
                String jsonResponse = "{\"service1\":" + service1 + ",\"service2\":" + service2 + "}";
                writer.println(jsonResponse);

               // Sleep for 2 seconds to si delay in  next request
            Thread.sleep(2000);
            }
        } catch (IOException e) {
            System.err.println("Error handling request: " + e.getMessage());
        } finally {
            clientSocket.close();
        }
    }
    

    private static void stopDockerCompose() {
        try {
            ProcessBuilder processBuilder = new ProcessBuilder("/bin/sh", "-c", "docker-compose -f /app/docker-compose.yml down");
            processBuilder.inheritIO(); 
            Process process = processBuilder.start();
            int exitCode = process.waitFor(); 
    
            if (exitCode == 0) {
                
                System.out.println("{\"message\":\"Services stopped successfully.\"}");
            } else {
               
                System.out.println("{\"message\":\"Failed to stop services.\"}");
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            System.out.println("{\"message\":\"Error stopping services: " + e.getMessage() + "\"}");
        } finally {
          
            System.exit(0);
        }
    }
    


    private static String getService1Info() throws Exception {
        StringBuilder info = new StringBuilder();
        info.append("{");

        // IP address
        InetAddress ip = InetAddress.getLocalHost();
        info.append("\"IpAddress\":\"").append(ip.getHostAddress()).append("\",");

        // Running processes
        ProcessBuilder processBuilder = new ProcessBuilder("ps", "ax");
        Process process = processBuilder.start();
        info.append("\"Processes\":[").append(outputFromProcess(process)).append("],");

        // Available disk space
        File root = new File("/");
        long free = root.getFreeSpace();
        double freeGB = free / (1024 * 1024 * 1024);
        info.append("\"FreeSpaceGB\":\"").append(String.format("%.2f", freeGB)).append("\",");

        // Last boot time
        RuntimeMXBean runtimeMX = ManagementFactory.getRuntimeMXBean();
        Date startTime = new Date(runtimeMX.getStartTime());
        info.append("\"LastBootTime\":\"").append(startTime.toString()).append("\"");

        info.append("}");
        return info.toString();
    }

    private static String getService2Info() throws Exception {
        URI service2Uri = new URI("http://service2:5000");
        URL service2Url = service2Uri.toURL();

        BufferedReader input = new BufferedReader(new InputStreamReader(service2Url.openStream()));
        String inputLine;
        StringBuilder response = new StringBuilder();

        while ((inputLine = input.readLine()) != null) {
            response.append(inputLine);
        }
        input.close();
        return response.toString();
    }

    private static String outputFromProcess(Process pro) throws Exception {
        BufferedReader reader = new BufferedReader(new InputStreamReader(pro.getInputStream()));
        return reader.lines()
                     .map(line -> "\"" + line.replace("\"", "\\\"") + "\"")
                     .collect(Collectors.joining(","));
    }
}
