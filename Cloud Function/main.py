import os
import json
import functions_framework
import vertexai

from google.cloud import logging
from vertexai.preview.generative_models import GenerativeModel, Part

PROJECT_ID = "poc-chatbot-edf"
LOCATION = "europe-west1"

client = logging.Client(project=PROJECT_ID)
client.setup_logging()

LOG_NAME = "run_inference-cloudfunction-log"
logger = client.logger(LOG_NAME)

@functions_framework.http
def run_inference(request):
    """HTTP Cloud Function.
    Args:
        a GET HTTP request with 'prompt' query parameter 
    Returns:
        a HTTP response with the response from gemini 1.5
    """

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'prompt' in request_json:
        prompt = request_json['prompt']
    elif request_args and 'prompt' in request_args:
        prompt = request_args['prompt']
    else:
        return json.dumps({"response_text": "No prompt provided"})

    logger.log(f"Received request for prompt: {prompt}")
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-1.5-pro")

    responses = model.generate_content(
        contents=prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
        stream=True,
    )

    response_list = []
    for response in responses:
        try:
            response_list.append(response.text)
        except IndexError:
            response_list.append("")
            continue
    prompt_response = " ".join(response_list)

    return json.dumps({"response_text": prompt_response})
