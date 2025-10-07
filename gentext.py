from google import genai
from google.genai import types
import settings

client = genai.Client(api_key=settings.google_ai_token)

async def gen_text(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        # turn off "thinking" feature for testing
        # TODO enable thinking, consider budget https://ai.google.dev/gemini-api/docs/thinking
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0), # dynamic thinking: thinking_budget=-1
            # global prompt
            # TODO allow users to choose individual system prompts?
            system_instruction="""
            You are a discord user. You format messages as if they are discord messages. You are appropriately brief with your responses,
            but you still make a good-faith effort to be helpful. However, you do not know everything. You will format your responses as
            though they are discord messages, infrequently making use of emojis, and occassionally reference internet culture.
            """
        )
    )
    return response.text