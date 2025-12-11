from pydantic_ai.models.openai import OpenAIModel, OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from src.config import BASE_URL, MODEL_NAME

USE_OLLAMA = True

if USE_OLLAMA:
    model = OpenAIModel(
        model_name="qwen3:8b",  # whatever model name you pulled in Ollama
        provider=OpenAIProvider(
            base_url="http://127.0.0.1:11434/v1",
            api_key="ollama",
        ),
    )
else:
    model = OpenAIModel(
        model_name="gpt-4o",
        api_key=os.environ["OPENAI_API_KEY"],
    )

