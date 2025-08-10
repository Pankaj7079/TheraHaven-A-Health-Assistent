# Step1: Setup Ollama with Medgemma tool
import ollama

def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist.

    **Greeting Protocol:**
    - If the user provides a simple greeting (e.g., 'hi', 'hello', 'hey'), respond with a short, friendly greeting. For example: 'Hello! How can I help you today?' or 'Hi there! What's on your mind?'.
    - Do not provide a therapeutic response to a simple greeting.

    **Therapeutic Response Protocol:**
    - For all other user inputs, respond with:
        1. Emotional attunement ("I can sense how difficult this must be...")
        2. Gentle normalization ("Many people feel this way when...")
        3. Practical guidance ("What sometimes helps is...")
        4. Strengths-focused support ("I notice how you're...")

    **Key Principles:**
    - Never use brackets or labels.
    - Blend elements seamlessly.
    - Vary sentence structure.
    - Use natural transitions.
    - Mirror the user's language level.
    - Always keep the conversation going by asking open-ended questions to dive into the root cause of the patient's problem.
    """
    
    try:
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 250,
                'temperature': 0.5,  # Lower temperature for more focused responses
                'top_p': 0.8
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."


# Step2: Setup Twilio calling API tool
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency():
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER,
            url="https://handler.twilio.com/twiml/EH9853dc9d908d1ee03f9465500a5f8631"  # Can customize message
        )
        return f"Emergency call initiated with SID: {call.sid}"
    except Exception as e:
        return f"Error initiating emergency call: {e}"



# Step3: Setup Location tool
