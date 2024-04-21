from GPTModels.ModelClass import AnthropicModel, OpenAIChatModel


class LLMFactory:
    def __init__(self):
        self.models = {
            'openai': OpenAIChatModel,
            'anthropic': AnthropicModel,
        }

    def get_model(self, model_type, model_name=None):
        model_class = self.models.get(model_type)
        if not model_class:
            raise ValueError(f"Unsupported model type: {model_type}")
  
        if model_name:
            return model_class(model_name)
           
        return model_class()  
