import boto3
from typing import Optional, List
from app.config.env_config import settings

class BedrockService:

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        self.model_id = settings.AWS_MODEL

    def generate(
        self,
        prompt: str,
        image_paths: Optional[List[str]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        top_p: float = 0.9,
    ) -> str:

        content = []

        if image_paths:
            for image_path in image_paths:

                with open(image_path, "rb") as img:
                    image_bytes = img.read()

                image_format = (
                    image_path.split(".")[-1]
                    .lower()
                    .replace("jpg", "jpeg")
                )

                content.append(
                    {
                        "image": {
                            "format": image_format,
                            "source": {
                                "bytes": image_bytes
                            }
                        }
                    }
                )

        content.append(
            {
                "text": prompt
            }
        )

        response = self.client.converse(
            modelId=self.model_id,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            inferenceConfig={
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": top_p
            }
        )

        return response["output"]["message"]["content"][0]["text"]

bedrock_service = BedrockService()