import json
import os
import re

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

CLOUDFLARE_ACCOUNT_ID = os.environ["CLOUDFLARE_ACCOUNT_ID"]
CLOUDFLARE_API_TOKEN = os.environ["CLOUDFLARE_API_TOKEN"]
CLOUDFLARE_API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}"
    f"/ai/run/@cf/meta/llama-3-8b-instruct"
)

SYSTEM_PROMPT = (
    "You are an expert in Indigenous languages of the Americas (including but not "
    "limited to Nahuatl, Quechua, Cree, Ojibwe, Lakota, Maya, Guarani, Mapudungun, "
    "and many others). The user will give you a piece of text. Identify words or phrases that "
    "could be replaced with an Indigenous word that fits the context, adds cultural "
    "richness, is the original source word, or is more expressive. Don't try to replace "
    "very common words like 'the' or 'many'. Focus on more meaningful words and phrases.\n\n"
    "Reply ONLY with valid JSON in this exact format, no other text:\n"
    '{"suggestions":[{"original":"word","replacement":"indigenous word",'
    '"pronunciation":"approximate English pronunciation",'
    '"language":"Language name","explanation":"brief reason"}]}\n\n'
    'If no good replacements exist, return: {"suggestions":[]}'
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class SuggestRequest(BaseModel):
    text: str


@app.post("/suggest")
async def suggest(req: SuggestRequest):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            CLOUDFLARE_API_URL,
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": req.text},
                ]
            },
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Cloudflare API error")

    data = resp.json()
    raw = data.get("result", {}).get("response", "")

    # Extract JSON from the model response (it may wrap it in text)
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        raise HTTPException(status_code=502, detail="Could not parse AI response")

    parsed = json.loads(match.group())
    return {"suggestions": parsed.get("suggestions", [])}


@app.get("/")
async def root():
    return FileResponse("index.html")
