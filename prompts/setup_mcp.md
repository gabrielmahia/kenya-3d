# Prompt: Setup MCP Connection

Paste into Claude Code after enabling the Blender MCP add-on.

---

Connect Claude Code to Blender MCP and verify:

1. Check registration: run `claude mcp get blender`
2. Verify Blender has the MCP add-on enabled (Edit → Preferences → Add-ons → MCP)
3. Ask Blender for the current scene name via MCP
4. Confirm host/port match (default localhost:9000)
5. If connection fails, confirm Blender's MCP panel shows "Running"

Report: "Blender MCP connected — ready for civic 3D visualization"

---

**Troubleshooting**

| Issue | Fix |
|---|---|
| Connection refused | `uvx blender-mcp-server` in terminal |
| Add-on missing | Edit → Preferences → Get Extensions → search "MCP" |
| Module not found | `pip install -r requirements.txt` |
