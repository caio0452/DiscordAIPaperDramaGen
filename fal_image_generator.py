
import httpx
import logging
from parameters import Parameters

class FalAIImageGenerator:
    def __init__(self, parameters: Parameters):
        self.http_client = httpx.AsyncClient()
        if (parameters.fal_api_key is None) or (parameters.fal_model_slug is None):
            raise RuntimeError("Missing fal API key or model slug")
        self.api_key = parameters.fal_api_key
        self.model_slug = parameters.fal_model_slug
        
    async def generate_image(self, text_prompt: str) -> str | None:
        headers = {
            "Authorization": f"Key {self.api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }
        data = {
            "prompt": text_prompt,
            "negative_prompt": "Ugly, distorted, low-quality",
            "enable_safety_checker": False,
            "num_images": 1
        }
        url = f"https://fal.run/{self.model_slug}"

        try:
            response = await self.http_client.post(url, headers=headers, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()

            first_image = result["images"][0]
            image_url = first_image["url"]
            return image_url
        except Exception:
            logging.exception(f"Failed to generate image with prompt '{text_prompt}' at {url}")
            return None