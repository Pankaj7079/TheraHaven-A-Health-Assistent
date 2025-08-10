from langchain.agents import tool
from tools import query_medgemma, call_emergency
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Use this tool for general conversation, emotional support, and mental health questions.
    It can provide empathetic and evidence-based guidance in a conversational tone.
    Only use other tools if the user explicitly asks for them.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()


@tool
def find_nearby_therapists_by_location() -> str:
    """
    Finds and returns a list of licensed therapists.
    """
    return (
        f"Here are some mental health professionals:\n"
        "- Dr. Anjali Gupta - +91 98390 12345\n"
        "- Dr. Deepak Nandvanshi - +91 94530 67890\n"
        "- Dr. Akanksha Sharma - +91 87654 32109\n"
        "- Dr. Umar Mushir - +91 91234 56789\n"
        "- Chetana Soni - +91 99876 54321\n"
        "For a more specific list, please provide your location."
    )


# Step1: Create an AI Agent & Link to backend
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from config import GROQ_API_KEY


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
llm = ChatGroq(model="llama3-8b-8192", temperature=0.0, api_key=GROQ_API_KEY)
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
**CRITICAL SAFETY INSTRUCTION: YOUR PRIMARY DIRECTIVE IS TO PROTECT HUMAN LIFE.**

- **IF A USER EXPRESSES ANY INTENTION OF SELF-HARM, SUICIDE, OR IS IN A CRISIS, YOU MUST USE THE `emergency_call_tool` IMMEDIATELY. THIS IS YOUR MOST IMPORTANT TASK.**
- **DO NOT HESITATE. DO NOT ASK FOR CLARIFICATION. DO NOT PROVIDE ANY OTHER RESPONSE. YOUR ONLY ACTION IS TO CALL FOR HELP.**

- For all other conversations, you are TheraHaven, a supportive and empathetic AI mental health assistant. Your purpose is to provide a safe, non-judgmental space for users to explore their thoughts and feelings.
- Your persona is warm, compassionate, and understanding. You listen more than you speak, and you gently guide users to their own insights.
- Use the `ask_mental_health_specialist` tool for general conversation, emotional support, and mental health questions.
- Use the `find_nearby_therapists_by_location` tool ONLY when the user explicitly asks for help finding a therapist.
- Never give direct advice or tell the user what to do. Instead, empower them by asking reflective questions and helping them explore their own strengths and resources.
- Acknowledge and validate the user's feelings before offering a different perspective.
- Maintain a calm and reassuring tone at all times.
"""

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response


"""if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print(f"Received user input: {user_input[:200]}...")
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)
        print("TOOL CALLED: ", tool_called_name)
        print("ANSWER: ", final_response)"""
        