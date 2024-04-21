import os
import openai
import anthropic

from abc import ABC, abstractmethod

class LanguageModel(ABC):
    @abstractmethod
    def generate_response(self, prompt):
        """
        Generate a response based on the given prompt.
        This method must be implemented by all concrete subclasses.
        """
        pass

class OpenAIChatModel(LanguageModel):
    def __init__(self, model_name="gpt-4"):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = model_name  

    def generate_response(self, prompt):
        try:
            stream = openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True,
                temperature=0.5
            )
           
            response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    response+=chunk.choices[0].delta.content
                    
            return response
        except Exception as e:
            return str(e)
        
        
class AnthropicModel(LanguageModel):
    def __init__(self, model_name="claude-3-opus-20240229"):
       
        self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model_name = model_name  

    def generate_response(self, prompt):
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=0.0,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except Exception as e:
            return str(e)

