# Step1: Setup FastAPI backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from ai_agent import graph, SYSTEM_PROMPT, parse_response
from tools import call_emergency

app = FastAPI()

# Step2: Receive and validate request from Frontend
class Query(BaseModel):
    message: str

EMERGENCY_KEYWORDS = ["kill myself", "suicide", "end my life", "want to die"]

@app.post("/ask")
async def ask(query: Query):
    # Check for emergency keywords
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in query.message.lower():
            response = call_emergency()
            return {"response": response, "tool_called": "emergency_call_tool"}

    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
    #inputs = {"messages": [("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    # Step3: Send response to the frontend
    return {"response": final_response,
            "tool_called": tool_called_name}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)






