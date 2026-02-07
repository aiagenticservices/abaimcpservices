import json
import sys

# Vercel Python serverless entrypoint: handler(request)
# We’ll implement a minimal JSON-RPC-like MCP server.

def google_search(query: str):
    """
    MCP Tool: google_search
    In a real implementation, this would call Google Custom Search API.
    Here we just return a fake result so the flow is crystal clear.
    """
    return {
        "tool": "google_search",
        "query": query,
        "results": [
            {
                "title": "Example result 1",
                "url": "https://www.google.com/search?q=" + query,
                "snippet": f"Fake search result for '{query}'."
            }
        ]
    }


def google_calendar_list(calendar_id: str):
    """
    MCP Tool: google_calendar_list
    In a real implementation, this would call Google Calendar API.
    Here we return a fake list of events.
    """
    return {
        "tool": "google_calendar_list",
        "calendarId": calendar_id,
        "events": [
            {
                "id": "evt_1",
                "summary": "Fake Meeting",
                "start": "2026-02-06T10:00:00Z",
                "end": "2026-02-06T11:00:00Z"
            }
        ]
    }


def list_tools():
    """
    MCP Concept: tools/list
    Return metadata about available tools and their parameters.
    This is how a client discovers capabilities.
    """
    return {
        "tools": [
            {
                "name": "google_search",
                "description": "Search the web using Google (demo).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query text."
                        }
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "google_calendar_list",
                "description": "List events from a Google Calendar (demo).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Calendar identifier (email or ID)."
                        }
                    },
                    "required": ["calendar_id"]
                }
            }
        ]
    }


def call_tool(name: str, args: dict):
    """
    MCP Concept: tools/call
    Execute a tool by name with arguments.
    """
    if name == "google_search":
        query = args.get("query", "")
        return google_search(query)
    elif name == "google_calendar_list":
        calendar_id = args.get("calendar_id", "primary")
        return google_calendar_list(calendar_id)
    else:
        raise ValueError(f"Unknown tool: {name}")


def make_error_response(id_value, code, message):
    return {
        "jsonrpc": "2.0",
        "id": id_value,
        "error": {
            "code": code,
            "message": message
        }
    }


def make_success_response(id_value, result):
    return {
        "jsonrpc": "2.0",
        "id": id_value,
        "result": result
    }


def handler(request):
    """
    Vercel entrypoint.
    - Reads JSON body
    - Dispatches based on 'method'
    - Returns JSON-RPC-like response
    """
    try:
        body = request.body
        if isinstance(body, (bytes, bytearray)):
            body = body.decode("utf-8")

        data = json.loads(body or "{}")
    except Exception as e:
        return _json_response(
            make_error_response(None, -32700, f"Parse error: {e}"),
            status=400
        )

    jsonrpc = data.get("jsonrpc")
    method = data.get("method")
    params = data.get("params", {}) or {}
    id_value = data.get("id")

    if jsonrpc != "2.0":
        return _json_response(
            make_error_response(id_value, -32600, "Invalid Request: jsonrpc must be '2.0'"),
            status=400
        )

    try:
        if method == "tools/list":
            result = list_tools()
            return _json_response(make_success_response(id_value, result))
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            if not tool_name:
                raise ValueError("Missing 'name' in params for tools/call")
            result = call_tool(tool_name, args)
            return _json_response(make_success_response(id_value, result))
        else:
            return _json_response(
                make_error_response(id_value, -32601, f"Method not found: {method}"),
                status=404
            )
    except Exception as e:
        return _json_response(
            make_error_response(id_value, -32000, f"Server error: {e}"),
            status=500
        )


def _json_response(payload, status=200):
    """
    Helper to build a Vercel-compatible response.
    """
    from http.server import BaseHTTPRequestHandler

    class Response(BaseHTTPRequestHandler):
        pass

    # Vercel Python runtime expects a dict with 'statusCode', 'headers', 'body'
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(payload)
    }
