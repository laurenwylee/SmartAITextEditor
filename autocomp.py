import json
import requests

API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer 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"}
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))
data = query(input())
retVal = data[0].get("generated_text")
print(retVal)
