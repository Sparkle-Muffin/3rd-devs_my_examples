from openai import OpenAI
from typing import Union, AsyncIterable
from dotenv import load_dotenv
import os

class OpenAIService:
    def __init__(self):
        load_dotenv()
        self.openai = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY')
        )
    
    def completion(
        self,
        messages: list[dict],
        model: str = "gpt-4",
        stream: bool = False
    ) -> Union[dict, AsyncIterable]:
        try:
            chat_completion = self.openai.chat.completions.create(
                messages=messages,
                model=model,
                stream=stream
            )
            
            return chat_completion
            
        except Exception as error:
            print("Error in OpenAI completion:", error)
            raise error