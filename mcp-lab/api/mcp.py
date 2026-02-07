import json
def google_search(query: str):
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
    return {
        "tools": [
            {
                "name": "google_search",
                "description": "Search the web using Google (demo).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"}
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
                        "calendar_id": {"type": "string"}
                    },
                    "required": ["calendar_id"]
                }
            }
        ]
    }

def call_tool(name: str, args: dict):
    if name == "google_search":
        return google_search(args.get("query", ""))
    if name == "google_calendar_list":
        return google_calendar_list(args.get("calendar_id", "primary"))
    raise ValueError(f"Unknown tool: {name}")

def handler(request):
    try:
        body = request.body
        if isinstance(body, (bytes, bytearray)):
            body = body.decode("utf-8")
        data = json.loads(body or "{}")
    except Exception as e:
        return _json_response({"error": f"Parse error: {e}"}, 400)

    method = data.get("method")
    params = data.get("params", {})
    id_value = data.get("id")

    try:
        if method == "tools/list":
            return _json_response({"jsonrpc": "2.0", "id": id_value, "result": list_tools()})
        if method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            return _json_response({"jsonrpc": "2.0", "id": id_value, "result": call_tool(name, args)})
        return _json_response({"error": f"Unknown method: {method}"}, 404)
    except Exception as e:
        return _json_response({"error": str(e)}, 500)

def _json_response(payload, status=200):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(payload)
    }
