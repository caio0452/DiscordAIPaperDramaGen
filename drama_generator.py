import re
import json
import random
import prompts
from openai import AsyncOpenAI
from parameters import Parameters
from drama_data import Drama, DramaTemplate
from fal_image_generator import FalAIImageGenerator

class AIDramaGenerator:
    def __init__(self, parameters: Parameters):
        self.openai_client = AsyncOpenAI(
            api_key=parameters.openai_api_key.get_secret_value(),
            base_url=parameters.openai_base_url
        )
        self.llm_name = parameters.llm_name
        self.image_generator: FalAIImageGenerator | None = None
        self._drama_data = DramaTemplate.from_file("data.json")
        self.image_gen_chance = parameters.image_generation_chance
        if parameters.is_all_fal_data_present():
            self.image_generator = FalAIImageGenerator(parameters)
        else:
            print("No valid fal.ai API key or model slug found in environment variables, image generation is disabled")

    def _get_random_drama_sentence(self):
        generated = random.choice(self._drama_data.sentences)
        for key, values in self._drama_data.combinations.items():
            placeholder = f"[{key}]"
            while (placeholder in generated):
                # Replace one placeholder at a time. We don't want all of the same placeholder to be the same random choice
                generated = generated.replace(placeholder, random.choice(values), 1)
            
        return generated
    
    async def generate_ai_drama(self) -> Drama:
        TEMPERATURE = 0.5
        base_sentence = self._get_random_drama_sentence()
        image_url: str | None = None

        context = ""
        for word in re.findall(r'[a-zA-Z]', base_sentence):
            if word in self._drama_data.descriptions:
                context += self._drama_data.descriptions[word] + ". "
        if context == "":
            context = "(no additional context)"

        result = await self.openai_client.chat.completions.create(
            messages=prompts.DRAMA_PROMPT
                .replace("[base_sentence]", base_sentence)
                .replace("[context]", context)
                .messages,
            model=self.llm_name,
            temperature=TEMPERATURE
        )

        result_text = result.choices[0].message.content        
        if (result_text in ("", None)):
            raise RuntimeError("LLM provider returned empty response")
        
        try:
            response_json = json.loads(result_text)
            headline = response_json["headline"]
            content = response_json["content"]
            image_caption = response_json["image_caption"]
        except Exception as ex:
            raise RuntimeError(f"Failed to parse LLM response: {result_text}") from ex

        if self.image_generator is not None:
            if random.random() < self.image_gen_chance:
                image_url = await self.image_generator.generate_image(image_caption)

        return Drama(content, headline, image_url)