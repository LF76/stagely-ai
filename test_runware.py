import urllib.request
import json
import time
import uuid
import sys
import os

# Read from environment or local .env
API_KEY = os.environ.get("RUNWARE_API_KEY")

if not API_KEY and os.path.exists(".env"):
    with open(".env") as f:
        for line in f:
            if line.startswith("RUNWARE_API_KEY="):
                API_KEY = line.strip().split("=", 1)[1].strip("\"'")

if not API_KEY:
    print("Error: RUNWARE_API_KEY not found in environment or .env file.")
    print("Please set RUNWARE_API_KEY in your .env or environment variables.")
    sys.exit(1)
URL = "https://api.runware.ai/v1"

prompt = sys.argv[1] if len(sys.argv) > 1 else "luxury cosmetic serum bottle on a black wet volcanic stone with water droplets, dramatic commercial studio lighting, 8k"

print(f"Generating image via Runware Edge for prompt:\n'{prompt}'...\n")

t0 = time.time()
req_body = [
    {
        "taskType": "imageInference",
        "taskUUID": str(uuid.uuid4()),
        "positivePrompt": f"{prompt}, commercial product photography, sharp focus, 8k",
        "model": "runware:100@1",
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "CFGScale": 1.5,
        "numberResults": 1
    }
]

req = urllib.request.Request(
    URL,
    data=json.dumps(req_body).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        elapsed = time.time() - t0
        image_url = result["data"][0]["imageURL"]
        print(f"Success in {elapsed:.2f} seconds!")
        print(f"Generated Image URL: {image_url}")
except Exception as e:
    print(f"Error: {e}")
