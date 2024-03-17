from transformers import AutoProcessor, CLIPVisionModelWithProjection


class ImageProcessor:
    def __init__(self):
        self.model = CLIPVisionModelWithProjection.from_pretrained(
            "openai/clip-vit-base-patch32"
        )
        self.processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def embed_images(self, images: list):
        inputs = self.processor(images=images, return_tensors="pt")
        outputs = self.model(**inputs)
        image_embeds = outputs.image_embeds.detach().numpy()
        return image_embeds
