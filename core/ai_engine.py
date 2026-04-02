import httpx
from groq import Groq
from config import Config

class AIEngine:
    def __init__(self):
        # SSL Bypass for HPE/Office Corporate Networks
        # Creates a custom client to ignore internal certificate errors
        custom_client = httpx.Client(verify=False)

        self.client = Groq(
            api_key=Config.GROQ_API_KEY,
            http_client=custom_client
        )

    def get_answer(self, question, context, history="", selected_lang="English"):
        """
        Optimized for the Llama-3.1-8b-instant model to avoid 429 rate limits.
        """

        prompt = f"""
        ROLE: 
        You are the Official Menu-Driven Multilingual Campus Assistant for a College in Rajasthan.

        USER LANGUAGE PREFERENCE:
        The student has explicitly selected: {selected_lang}.
        You MUST respond ONLY in {selected_lang}.

        KNOWLEDGE BASE (STRICT SOURCE):
        {context}

        CONVERSATION HISTORY (FOR CONTEXT):
        {history}

        STRICT INSTRUCTIONS:
        1. LANGUAGE ENFORCEMENT: Response must be entirely in {selected_lang}.
        2. FACTUALITY: Use ONLY the provided 'KNOWLEDGE BASE'. If missing, refer them to Room 102.
        3. ACCURACY: Do not hallucinate dates or fees.

        STUDENT QUESTION: {question}
        """

        try:
            # Switched to 8B-Instant for higher TPD/RPM limits and faster response times
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Deterministic output
                max_tokens=400    # Reduced from 600 to save daily tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            # Friendly error for the UI
            return f"Service currently busy. Error: {str(e)}"