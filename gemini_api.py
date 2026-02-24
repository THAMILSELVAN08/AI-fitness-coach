import requests
import json

def call_gemini(prompt, profile):
    # 1. USE ENVIRONMENT VARIABLES IN REAL APP
    # For now, put your NEW key here
    api_key = "AIzaSyCZQ-EC8uii0rl9DqmDah_YsroRbPwfsjg" 
    
    # 2. UPDATED MODEL NAME (gemini-2.5-flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048,
        }
        # Safety settings omitted for brevity, add back if needed
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            # This will now print the actual error if the new model fails
            raise Exception(f"Gemini API Error {response.status_code}: {response.text}")
        
        response_data = response.json()
        
        if 'candidates' in response_data and response_data['candidates']:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception("No content generated")
            
    except Exception as e:
        raise Exception(f"Gemini API call failed: {str(e)}")