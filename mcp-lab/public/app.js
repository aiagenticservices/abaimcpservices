const MCP_ENDPOINT = "/api/mcp";

const btnListTools = document.getElementById("btn-list-tools");
const toolsOutput = document.getElementById("tools-output");

const toolSelect = document.getElementById("tool-select");
const toolInputs = document.querySelectorAll(".tool-input");
const btnCallTool = document.getElementById("btn-call-tool");
const requestOutput = document.getElementById("request-output");
const responseOutput = document.getElementById("response-output");

toolSelect.addEventListener("change", () => {
  const selected = toolSelect.value;
  toolInputs.forEach((el) => {
    if (el.getAttribute("data-tool") === selected) {
      el.classList.add("active");
    } else {
      el.classList.remove("active");
    }
  });
});

btnListTools.addEventListener("click", async () => {
  const payload = {
    jsonrpc: "2.0",
    id: "1",
    method: "tools/list",
    params: {}
  };

  const res = await fetch(MCP_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  toolsOutput.textContent = JSON.stringify(data, null, 2);
});

btnCallTool.addEventListener("click", async () => {
  const toolName = toolSelect.value;

  let args = {};
  if (toolName === "google_search") {
    const query = document.getElementById("input-query").value || "";
    args = { query };
  } else if (toolName === "google_calendar_list") {
    const calendarId = document.getElementById("input-calendar-id").value || "primary";
    args = { calendar_id: calendarId };
  }

  const payload = {
    jsonrpc: "2.0",
    id: "2",
    method: "tools/call",
    params: {
      name: toolName,
      arguments: args
    }
  };

  requestOutput.textContent = JSON.stringify(payload, null, 2);

  const res = await fetch(MCP_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  responseOutput.textContent = JSON.stringify(data, null, 2);
});
