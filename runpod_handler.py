import runpod
import io
import time
import concurrent
import uuid
import json
from transformers import InstructBlipProcessor, InstructBlipForConditionalGeneration
import torch
from PIL import Image
import requests

model = InstructBlipForConditionalGeneration.from_pretrained("Salesforce/instructblip-vicuna-7b")
processor = InstructBlipProcessor.from_pretrained("Salesforce/instructblip-vicuna-7b")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)



#runpod handler
def handler(event):
    total_it=time.time()
    input_data=event['input']
    #handle input data -> input: text_list, duration, document_id
    url=input_data['url']
    prompt=input_data['prompt']

    image = Image.open(requests.get(url, stream=True).raw).convert("RGB")
    inputs = processor(images=image, text=prompt, return_tensors="pt").to(device)

    outputs = model.generate(
            **inputs,
            do_sample=False,
            num_beams=5,
            max_length=256,
            min_length=1,
            top_p=0.9,
            repetition_penalty=1.5,
            length_penalty=1.0,
            temperature=1,
    )
    generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0].strip()
    print(generated_text)


    #return: list of audio ids
    response={
        'generated_text': generated_text,
    }
    return json.dumps(response)


#runpod config.
runpod.serverless.start({
    "handler": handler
})