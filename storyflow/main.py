# Updated Python implementation
from mira_sdk import MiraClient, CompoundFlow
from pydantic import BaseModel
import json
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryConfig(BaseModel):
    genres_list: str
    weights_list: str
    min_age: str
    max_age: str
    platforms_list: str
    max_branches: str
    user_prompt: str = ""

    def validate_inputs(self):
        """Validate and normalize inputs"""
        # Validate genres
        genres = [g.strip() for g in self.genres_list.split(',')]
        valid_genres = [
            'scifi', 'fantasy', 'mystery', 'romance', 'thriller', 'horror',
            'slice_of_life', 'historical', 'western', 'comedy', 'drama',
            'action', 'adventure', 'cyberpunk', 'dystopian', 'steampunk'
        ]
        if not all(genre in valid_genres for genre in genres):
            raise ValueError(f"Invalid genres. Valid options are: {', '.join(valid_genres)}")

        # Validate weights
        weights = [float(w.strip()) for w in self.weights_list.split(',')]
        if len(weights) != len(genres):
            raise ValueError("Number of weights must match number of genres")
        if not all(0 <= w <= 1 for w in weights):
            raise ValueError("Weights must be between 0 and 1")
        
        # Normalize weights to sum to 1
        total = sum(weights)
        if total == 0:
            raise ValueError("Weights cannot all be 0")
        normalized_weights = [w/total for w in weights]
        self.weights_list = ','.join(str(w) for w in normalized_weights)

        # Validate age range
        min_age = int(self.min_age)
        max_age = int(self.max_age)
        if not (0 <= min_age <= max_age):
            raise ValueError("Invalid age range")

        # Validate max branches
        max_branches = int(self.max_branches)
        if not (2 <= max_branches <= 7):
            raise ValueError("Max branches must be between 2 and 7")


def render_story(response: Dict[str, Any]):
    """Render story content from platform adaptor output"""
    try:
        print("\n" + "="*50)
        print("Generated Story")
        print("="*50)
        
        # Extract CLI formatted story
        platform_output = json.loads(response.get('formatted_story', '{}'))
        cli_story = platform_output.get('cli', {})
        
        # Print story structure
        print(f"\nTitle: {cli_story.get('Title', 'Untitled Story')}\n")
        
        # Print chapters and scenes
        for key, value in cli_story.items():
            if key.startswith("Chapter"):
                print(f"\n{key}: {value[0]}")
                for scene in value[1:]:
                    print(f"- {scene}")
        
        # Extract and display choices from narrative
        full_story = response.get('full_story', '')
        if "Choices:" in full_story:
            choices_section = full_story.split("Choices:")[1]
            print("\nBranching Choices:")
            for choice in choices_section.split('\n'):
                if choice.strip():
                    print(f"• {choice.strip()}")
                    
    except json.JSONDecodeError:
        logger.error("Invalid platform adaptor output format")
        print("\nRaw Story Output:\n")
        print(response.get('full_story', 'No story generated'))

def generate_story_core(config: StoryConfig) -> Dict[str, Any]:
    """Execute the story generation flow"""
    client = MiraClient(config={"API_KEY": "sb-ed41b1c035007b9a13da6d3b81c82600"})
    
    try:
        flow = CompoundFlow(source="workflow.yaml")
        result = client.flow.test(flow, config.model_dump(mode="json"))
        return {
            'formatted_story': result.output.get('platform_adaptor', ''),
            'full_story': result.output.get('story_generator', ''),
            'world_details': result.output.get('world_builder', '')
        }
    except Exception as e:
        logger.error(f"Flow execution failed: {str(e)}")
        return {}

def main():
    print("\nWelcome to the Interactive Story Generator!\n")
    
    try:
        # Test configuration
        user_config = {
            "genres_list": "fantasy,scifi",
            "weights_list": "0.6,0.4",
            "min_age": "12",
            "max_age": "16",
            "platforms_list": "cli",
            "max_branches": "3",
            "user_prompt": "A story about space wizards"
        }
        
        config = StoryConfig(**user_config)
        config.validate_inputs()
        
        print("\nGenerating your story...")
        response = generate_story_core(config)
        
        if response:
            render_story(response)
            print("\nStory generation complete!")
        else:
            print("Failed to generate story")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())