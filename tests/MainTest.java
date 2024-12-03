import org.junit.Test;
import java.net.Socket;
import static org.junit.Assert.assertTrue;

public class MainTest {

    @Test
    public void testServerIsRunning() {
        try {
            // Attempt to connect to the server at localhost:8199
            Socket socket = new Socket("localhost", 8199);
            assertTrue(socket.isConnected()); // Test will pass if the connection is established
            socket.close();
        } catch (Exception e) {
            // If an exception occurs, the test fails
            assertTrue("Server is not running: " + e.getMessage(), false);
        }
    }
}
