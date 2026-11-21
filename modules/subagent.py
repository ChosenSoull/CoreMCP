import os
from typing import Any, Dict, List, Optional
from openai import OpenAI

class OpenAIModel:
    """
    Base input structure for OpenAI-compatible LLM models.
    Encapsulates common parameters for making API calls to various LLMs.
    """

    def __init__(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        api_key: Optional[str] = None,
        base_url: str = "http://localhost:8080/v1/",
        temperature: float = 0.7,
        max_tokens: int = 65535,
        top_p: float = 1.0,
        seed: Optional[int] = None,
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.seed = seed

    def to_dict(self) -> dict:
        """Converts the input object to a dictionary suitable for API calls."""
        payload = {
            "model": self.model,
            "messages": self.messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "seed": self.seed,
        }
        return {k: v for k, v in payload.items() if v is not None}

    def send_message(self):
        key = self.api_key if self.api_key is not None else "not-needed"

        client = OpenAI(
            base_url=self.base_url,
            api_key=key,
        )

        response = client.chat.completions.create(**self.to_dict())

        return response

def run_subagent(
    prompt: str,
    system_prompt: Optional[str] = None,
) -> str:
    """Run the subagent to get a response from the LLM.
    This function initializes and runs the OpenAI model
    Parameters
    ----------
    prompt : str
        The main query (prompt) to be sent to the LLM.
    system_prompt : Optional[str]
        The system prompt that defines the model's role and context.
    Returns
    -------
    str - The text content of the response received from the LLM.
    """

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    mcp_api_key = os.getenv("OPENAI_API_KEY")
    mcp_base_url = os.getenv("OPENAI_BASE_URL", "http://localhost:8080/v1/")
    mcp_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    env_temp = os.getenv("OPENAI_TEMPERATURE")
    mcp_temperature = float(env_temp) if env_temp is not None else 0.7

    env_max_tokens = os.getenv("OPENAI_MAX_TOKENS")
    mcp_max_tokens = int(env_max_tokens) if env_max_tokens is not None else 65535

    env_top_p = os.getenv("OPENAI_TOP_P")
    mcp_top_p = float(env_top_p) if env_top_p is not None else 1.0

    env_seed = os.getenv("OPENAI_SEED")
    mcp_seed = int(env_seed) if env_seed is not None else None

    agent = OpenAIModel(
        model=mcp_model,
        messages=messages,
        api_key=mcp_api_key,
        base_url=mcp_base_url,
        temperature=mcp_temperature,
        max_tokens=mcp_max_tokens,
        top_p=mcp_top_p,
        seed=mcp_seed,
    )

    response = agent.send_message()
    return response.choices[0].message.content