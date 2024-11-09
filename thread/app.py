from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from OpenAIService import OpenAIService
from typing import Optional, List, Dict, Any

app = FastAPI()
openai_service = OpenAIService()
previous_summarization = ""

class Message(BaseModel):
    message: dict

async def generate_summarization(user_message: dict, assistant_response: dict) -> str:
    summarization_prompt = {
        "role": "system",
        "content": f"""Please summarize the following conversation in a concise manner, incorporating the previous summary if available:
<previous_summary>{previous_summarization or "No previous summary"}</previous_summary>
<current_turn> User: {user_message['content']}\nAssistant: {assistant_response.content} </current_turn>
"""
    }
    
    response = openai_service.completion(
        messages=[
            summarization_prompt,
            {"role": "user", "content": "Please create/update our conversation summary."}
        ],
        model="gpt-4",
        stream=False
    )
    
    return response.choices[0].message.content

def create_system_prompt(summarization: str) -> dict:
    base_prompt = "You are Alice, a helpful assistant who speaks using as few words as possible.\n\n"
    
    if summarization:
        summary_section = (
            "Here is a summary of the conversation so far:\n"
            "<conversation_summary>\n"
            f"  {summarization}\n"
            "</conversation_summary>\n\n"
        )
        base_prompt += summary_section
    
    base_prompt += "Let's chat!"
    
    return {
        "role": "system",
        "content": base_prompt
    }

@app.post("/api/chat")
async def chat(message: Message):
    global previous_summarization
    
    try:
        system_prompt = create_system_prompt(previous_summarization)
        
        assistant_response = openai_service.completion(
            messages=[system_prompt, message.message],
            model="gpt-4",
            stream=False
        )
        
        # Generate new summarization
        previous_summarization = await generate_summarization(
            message.message,
            assistant_response.choices[0].message
        )
        
        return assistant_response
        
    except Exception as error:
        print('Error in OpenAI completion:', str(error))
        raise HTTPException(status_code=500, detail="An error occurred while processing your request")

@app.post("/api/demo")
async def demo():
    global previous_summarization
    
    demo_messages = [
        {"content": "Hi! I'm Adam", "role": "user"},
        {"content": "How are you?", "role": "user"},
        {"content": "Do you know my name?", "role": "user"}
    ]
    
    assistant_response = None
    
    for message in demo_messages:
        print('--- NEXT TURN ---')
        print('Adam:', message['content'])
        
        try:
            system_prompt = create_system_prompt(previous_summarization)
            
            assistant_response = openai_service.completion(
                messages=[system_prompt, message],
                model="gpt-4",
                stream=False
            )
            
            print('Alice:', assistant_response.choices[0].message.content)
            
            # Generate new summarization
            previous_summarization = await generate_summarization(
                message,
                assistant_response.choices[0].message
            )
            
        except Exception as error:
            print('Error in OpenAI completion:', str(error))
            raise HTTPException(status_code=500, detail="An error occurred while processing your request")
    
    return assistant_response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000) 