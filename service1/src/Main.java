
import java.io.*;
import java.lang.management.ManagementFactory;
import java.lang.management.RuntimeMXBean;
import java.net.*;
import java.util.Date;
import java.util.stream.*;

public class Main {
  

    public static void main(String[] args) throws Exception {
        // for creating http server to listen on port 8199
        ServerSocket serverSocket = new ServerSocket(8199);
        System.err.println("Service1 is running on port 8199");

        while (true) {
           ;

            Socket clientSocket = serverSocket.accept();
            // Handle the request in a new thread
            new Thread(() -> {
                try {
                    handleRequest(clientSocket);
                } catch (Exception e) {
                    System.err.println(" - Error handling request: " + e.getMessage());
                }
            }).start();
        }
    }

    private static void handleRequest(Socket clientSocket) throws Exception{
        try (OutputStream output = clientSocket.getOutputStream();
             PrintWriter writer = new PrintWriter(output, true)) {

    
            // Getting service information
            String service1 = getService1Info();
            String service2 = getService2Info();

            // HTTP response
            writer.println("HTTP/1.1 200 OK");
            writer.println("Content-Type: application/json");
            writer.println("Connection: close");
            writer.println();

            // Combine service information into JSON
            String jsonResponse = "{\"service1\":" + service1 + ",\"service2\":" + service2 + "}";
            writer.println(jsonResponse);

   
            // Sleep for 2 seconds to simulate delay in handling next request
            Thread.sleep(2000);
            

        } catch (IOException | InterruptedException e) {
            System.err.println("Error handling request: " + e.getMessage());
        } finally {
            try {
                clientSocket.close();
            } catch (IOException e) {
                System.err.println("Error closing client socket: " + e.getMessage());
            }
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
