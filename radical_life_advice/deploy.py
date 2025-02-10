from mira_sdk import MiraClient, CompoundFlow
from mira_sdk.exceptions import FlowError

client = MiraClient(config={"API_KEY":"sb-ed41b1c035007b9a13da6d3b81c82600"})  # Initialize client
flow = CompoundFlow(source="workflow.yaml")           # Load flow configuration

try:
    client.flow.deploy(flow)                               # Deploy to platform
    print("Compound flow deployed successfully!")          # Success message
except FlowError as e:
    print(f"Deployment error: {str(e)}")                   # Handle deployment error
