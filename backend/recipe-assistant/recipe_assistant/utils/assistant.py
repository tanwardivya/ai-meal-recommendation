from typing_extensions import override
from openai import OpenAI
from openai import AssistantEventHandler
import time
from openai.types.beta.assistant_stream_event import ThreadMessageDelta

from openai.types.beta import Thread
def create_assistant(client:OpenAI,assistant_name: str, assistant_instruction:str, model_name:str):
    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=assistant_instruction,
        model=model_name,
    )
    return assistant

def submit_message(client:OpenAI,assistant_id, thread_id, user_message):
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )


def get_response(client:OpenAI,thread_id) -> str:
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for m in messages:
        if m.role == 'assistant':
            if m.content[0]:
                return m.content[0].text.value #type:ignore
    return ''

def create_thread(client: OpenAI):
    thread = client.beta.threads.create()
    return thread

def create_run(client:OpenAI,assistant_id: str,thread_id:str, user_input:str):
    run = submit_message(client,assistant_id, thread_id, user_input)
    return run

def create_thread_and_run(client:OpenAI,assistant_id: str, user_input:str):
    thread = client.beta.threads.create()
    run = submit_message(client,assistant_id, thread, user_input)
    return thread, run


def wait_on_run(client,run, thread_id):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter and delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter and delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 

def stream_assistant_run(client: OpenAI, thread_id: str,assistant_id: str, prompt: str):
    stream = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=prompt,
        stream=True,
        )
    for event in stream:
        if isinstance(event, ThreadMessageDelta) and event.data and event.data.delta and event.data.delta.content and event.data.delta.content[0] and event.data.delta.content[0].text: #type:ignore
            message_content = event.data.delta.content[0].text.value #type:ignore
            yield f"data: {{\"role\": \"assistant\", \"content\": \"{message_content}\"}}\n\n"
