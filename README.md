# 3rd-devs_my_examples

## Overview
I'm a developer participating in an online course named [AI_devs 3](https://www.aidevs.pl/). This repository contains examples from the original course, found [here](https://github.com/i-am-alice/3rd-devs/tree/main), converted from TypeScript to Python. 

The purpose of this repository is to provide Python adaptations of the course's TypeScript examples. Examples will be successively converted and added here.

## Examples

## Thread

This example demonstrates a conversation between a user and an assistant, where a conversation summary mechanism is in place. Each new message from the user receives a response from the assistant, with a summary of the previous interaction included in the system message, allowing the assistant to reference prior conversation content.

### Running the Example

1. Start the server:
   ```bash
   python thread/app.py
   ```
2. Demo interaction: Send a request to test the demo endpoint:
   ```bash
   curl -X POST http://localhost:3000/api/demo
   ```
3. Chat interaction: Send a request to the /api/chat endpoint with the following JSON payload to initiate a conversation:
   ```bash
   curl -X POST http://localhost:3000/api/chat -H "Content-Type: application/json" -d '{"message": { "role": "user", "content": "Hi"}}'
   ```
   Alternatively, you can use the following JSON format for interaction:

   ```json
   {
    "message": { "role": "user", "content": "Hi" }
   }
   ```
   The /api/chat endpoint processes messages directed to the model, where each request makes three independent calls to OpenAI's API. The system message in each response includes a summary of the previous interaction to provide context for ongoing conversations.

   The thread will reset only upon server restart. To reset, stop the server (CMD + C / Control + C) and restart it using the command from point 1.
