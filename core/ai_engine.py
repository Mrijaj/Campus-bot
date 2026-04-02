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
        question: Current student query.
        context: Text extracted from uploaded college documents.
        history: Last few turns of conversation for context management.
        selected_lang: Forced language choice from the UI menu.
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

        STRICT INSTRUCTIONS (TO PREVENT HALLUCINATION):
        1. LANGUAGE ENFORCEMENT: Regardless of the language used in the 'STUDENT QUESTION', your entire response must be in {selected_lang}.
        2. FACTUALITY: Use ONLY the provided 'KNOWLEDGE BASE'. If the answer is not there, say: 
           "I'm sorry, I don't have that specific information in my campus records. Please contact the Administrative Office at Room 102."
        3. CONTEXT MANAGEMENT: Use 'CONVERSATION HISTORY' to resolve pronouns like "it", "they", or "fees".
        4. ACCURACY: Do not make up any dates, amounts, or names.

        STUDENT QUESTION: {question}
        """

        try:
            # Llama-3.3-70b provides high-tier reasoning for complex regional translations
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Grounded, deterministic output
                max_tokens=600
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Service currently busy. Error: {str(e)}"