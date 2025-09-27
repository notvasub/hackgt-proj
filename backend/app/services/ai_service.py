"""AI service for claim analysis and optimization."""

import json
import base64
from typing import List, Dict, Any, Optional
import httpx
from app.config import settings
from app.models.claim import Claim, ClaimFile


class AIService:
    """Service for AI-related operations."""
    
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.base_url = "https://api.openai.com/v1"
    
    async def _make_openai_request(self, messages: List[Dict[str, Any]]) -> str:
        """Make a request to OpenAI API."""
        if not self.openai_api_key:
            # Return mock response when OpenAI is not configured
            return """{
                "optimized_description": "AI analysis is not available. Please review the original incident description and add any additional details you feel are important for your claim.",
                "damage_assessment": "Please provide a detailed assessment of all damages incurred. Include specific areas affected, extent of damage, and any visible issues.",
                "claim_justification": "This claim is based on the incident details provided. Please ensure all relevant information is included to support your claim.",
                "requested_amount": 0.0,
                "strength_score": 50
            }"""
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def _encode_image_to_base64(self, image_url: str) -> str:
        """Encode image from URL to base64."""
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, timeout=30.0)
            response.raise_for_status()
            
            image_data = response.content
            base64_image = base64.b64encode(image_data).decode('utf-8')
            return f"data:image/jpeg;base64,{base64_image}"
    
    async def analyze_claim(
        self, 
        claim: Claim, 
        files: List[ClaimFile]
    ) -> Dict[str, Any]:
        """Analyze a claim and generate optimized content."""
        
        # Prepare the prompt
        system_prompt = """You are an expert insurance claim analyst. Your job is to analyze incident details and images to create an optimized insurance claim that maximizes reimbursement potential.

Analyze the provided information and generate:
1. An optimized incident description that highlights key details
2. A comprehensive damage assessment
3. A strong claim justification
4. A realistic requested amount
5. A strength score (0-100) for the claim

Focus on:
- Clear, detailed descriptions
- Professional language
- Highlighting all claimable damages
- Supporting evidence from images
- Legal and policy compliance
- Maximizing claim value while being realistic

Return your response as a JSON object with these fields:
{
    "optimized_description": "...",
    "damage_assessment": "...", 
    "claim_justification": "...",
    "requested_amount": 12345.67,
    "strength_score": 85
}"""

        # Build user message with claim details
        user_message = f"""
Claim Type: {claim.claim_type.value}
Insurance Provider: {claim.insurance_provider}
Policy Number: {claim.policy_number}
Incident Date: {claim.incident_date}
Incident Location: {claim.incident_location}

Original Incident Description:
{claim.incident_description}

Please analyze this claim and the attached images to create an optimized version.
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Add images to the message if available
        if files:
            image_content = []
            for file in files:
                if file.content_type and file.content_type.startswith('image/'):
                    try:
                        base64_image = await self._encode_image_to_base64(file.s3_url)
                        image_content.append({
                            "type": "image_url",
                            "image_url": {"url": base64_image}
                        })
                    except Exception as e:
                        print(f"Failed to process image {file.filename}: {e}")
                        continue
            
            if image_content:
                messages[-1]["content"] = [
                    {"type": "text", "text": user_message},
                    *image_content
                ]
        
        try:
            # Make API request
            response = await self._make_openai_request(messages)
            
            # Parse JSON response
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # If response is not valid JSON, create a structured response
                result = {
                    "optimized_description": response,
                    "damage_assessment": "AI analysis completed. Please review the optimized description above.",
                    "claim_justification": "This claim has been optimized using AI analysis of the provided incident details and images.",
                    "requested_amount": 0.0,
                    "strength_score": 75
                }
            
            return result
            
        except Exception as e:
            # Fallback response in case of API failure
            return {
                "optimized_description": f"AI analysis temporarily unavailable. Original description: {claim.incident_description}",
                "damage_assessment": "Damage assessment pending AI analysis.",
                "claim_justification": "Claim justification pending AI analysis.",
                "requested_amount": 0.0,
                "strength_score": 50,
                "error": str(e)
            }
    
    async def generate_claim_summary(self, claim: Claim) -> str:
        """Generate a brief summary of the claim."""
        summary_prompt = f"""
        Generate a brief 2-3 sentence summary of this insurance claim:
        
        Type: {claim.claim_type.value}
        Provider: {claim.insurance_provider}
        Description: {claim.incident_description}
        
        Focus on the key incident details and claim type.
        """
        
        messages = [
            {"role": "user", "content": summary_prompt}
        ]
        
        try:
            response = await self._make_openai_request(messages)
            return response.strip()
        except Exception:
            return f"{claim.claim_type.value} claim with {claim.insurance_provider}"
