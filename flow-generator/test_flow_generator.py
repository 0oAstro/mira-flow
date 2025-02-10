from mira_sdk import MiraClient, CompoundFlow

config = {
    "idea": "Real-time collaboration tool",
    "details": "Supports multi-user editing, conflict resolution, and integration with third-party APIs"
}

client = MiraClient(config={"API_KEY": "sb-ed41b1c035007b9a13da6d3b81c82600"})
flow = CompoundFlow(source="workflow.yaml")

result = client.flow.test(flow, config)
print(result.keys())
print(result.values())
