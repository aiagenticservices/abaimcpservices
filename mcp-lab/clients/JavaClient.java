import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class JavaClient {
    private static final String MCP_ENDPOINT = "https://your-vercel-domain.vercel.app/api/mcp";

    public static void main(String[] args) throws Exception {
        // Example: call tools/list
        String listPayload = """
            {
              "jsonrpc": "2.0",
              "id": "java-1",
              "method": "tools/list",
              "params": {}
            }
            """;

        System.out.println("=== tools/list ===");
        System.out.println(sendRequest(listPayload));

        // Example: call google_search
        String callPayload = """
            {
              "jsonrpc": "2.0",
              "id": "java-2",
              "method": "tools/call",
              "params": {
                "name": "google_search",
                "arguments": {
                  "query": "Model Context Protocol"
                }
              }
            }
            """;

        System.out.println("=== tools/call google_search ===");
        System.out.println(sendRequest(callPayload));
    }

    private static String sendRequest(String json) throws Exception {
        URL url = new URL(MCP_ENDPOINT);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            byte[] input = json.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }

        StringBuilder response = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line.trim());
            }
        }

        return response.toString();
    }
}
