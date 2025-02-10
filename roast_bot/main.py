from mira_sdk import MiraClient, CompoundFlow
from mira_sdk.exceptions import FlowError

def generate_roast(target_name, style="cry hard roast", topics=None, intensity="10"):
    client = MiraClient(config={"API_KEY":"sb-ed41b1c035007b9a13da6d3b81c82600"})
    flow = CompoundFlow(source="workflow.yaml")

    roast_input = {
        "target_name": target_name,
        "roast_style": style,
        "topics": topics or "general",
        "intensity": intensity,
    }

    try:
        response = client.flow.test(flow, roast_input)
        roast = response['roast_generator']  # Get main roast
        delivery = response['delivery_formatter']  # Get formatted delivery
        return roast, delivery
    except FlowError as e:
        return f"Roast generation failed: {str(e)}", None

if __name__ == "__main__":
    target = input("Enter target name: ")
    style = input("Enter roast style (default: cry hard roast): ") or "cry hard roast"
    topics = input("Enter topics (comma separated, default: general): ") or "general"
    intensity = input("Enter intensity (1-10, default: 10): ") or "10"

    roast, delivery = generate_roast(
        target_name=target,
        style=style,
        topics=topics,
        intensity=intensity
    )

    print("Delivery Guide:", delivery)
    print("Generated Roast:", roast)
    print("Delivery Guide:", delivery)
