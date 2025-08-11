import json
import os
import logging
import requests
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BEARER_TOKEN = "ABSKQmVkcm9ja0FQSUtleS05ZTI1LWF0LTA4OTk5NDMxMjgxNTpJbnpGSHZ1c2RaYWg5bHJHNUk5bzlKVXdHcmNpcWJIaTRCbDBKeFlYMlVpM0FRRDhnMWJSSkFjbFdIST0="

class BedrockClient:
    def __init__(self, region: str = "us-east-1"):
        self.endpoint = f"https://bedrock-runtime.{region}.amazonaws.com"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }

    def converse(self, model_id: str, messages: List[Dict[str, Any]]) -> str:
        url = f"{self.endpoint}/model/{model_id}/converse"
        payload = {"messages": messages}
        try:
            resp = requests.post(url, headers=self.headers, json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return data.get("output", {}).get("message", {}).get("content", [{}])[0].get("text", "")
        except Exception as e:
            logger.error("Bedrock call failed: %s", e)
            return "Oops, something went wrong."

if __name__ == "__main__":
    user_msg = input("You: ").strip()
    client = BedrockClient(region="us-east-1")
    msgs = [{
        "role": "user",
        "content": [{"text": user_msg}]
    }]
    reply = client.converse("meta.llama3-8b-instruct-v1:0", msgs)
    print("Assistant:", reply)
