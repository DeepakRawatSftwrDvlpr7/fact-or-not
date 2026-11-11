import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from tavily import TavilyClient
from PIL import Image
import io
import json

app = FastAPI(title="TruthLens Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

class FactCheckResponse(BaseModel):
    claim: str
    verdict: str
    explanation: str
    correction: str
    references: list[str]

@app.post("/api/verify", response_model=FactCheckResponse)
async def verify_claim(
    text: str = Form(None),
    image: UploadFile = File(None)
):
    if not text and not image:
        raise HTTPException(status_code=400, detail="Provide either text or an image.")

    image_bytes = None
    extracted_text = text or ""

    if image:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        vision_prompt = "Extract any news claims, headlines, or statements visible in this image verbatim."
        vision_response = ai_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[pil_image, vision_prompt]
        )
        extracted_text = vision_response.text

    try:
        search_result = tavily_client.search(query=extracted_text, max_results=4)
        search_contexts = []
        reference_urls = []
        
        for res in search_result.get("results", []):
            search_contexts.append(f"Title: {res.get('title')}\nSnippet: {res.get('content')}")
            reference_urls.append(res.get('url'))

        context_string = "\n\n".join(search_contexts)

        analysis_prompt = f"""
        You are an objective, professional fact-checking engine. Analyze the claim below based on the web evidence provided.
        
        Claim / Statement: "{extracted_text}"
        
        Web Evidence Context:
        {context_string}
        
        Return your answer strictly in the following JSON format without any markdown code block wrappers around the JSON:
        {{
            "claim": "Summary of the core claim checked",
            "verdict": "True / False / Misleading / Unverified",
            "explanation": "Clear, objective breakdown of why based on the evidence",
            "correction": "The actual truth or accurate context",
            "references": {reference_urls}
        }}
        """

        contents_payload = [analysis_prompt]
        if image_bytes:
            contents_payload.insert(0, Image.open(io.BytesIO(image_bytes)))

        gemini_response = ai_client.models.generate_content(
            model="gemini-3.8-flash",
            contents=contents_payload
        )

        raw_text = gemini_response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        parsed_data = json.loads(raw_text.strip())
        return parsed_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))