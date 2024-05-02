from loguru import logger
from typing_extensions import override
import openai
from openai import OpenAI
from openai import AssistantEventHandler
import time
from openai.types.beta.assistant_stream_event import ThreadMessageDelta

from openai.types.beta import Thread

def get_assistant_instruction() -> str:
    recipe_name = '''
    Here's a delicious recipe for Zesty Herb-Stuffed Mushrooms that you can try at home:
    '''
    ingredients = '''
    - 24 large mushrooms, stems removed
    - 1 tablespoon olive oil
    - 1/2 cup onion, finely chopped
    - 2 cloves garlic, minced
    - 1/2 cup breadcrumbs
    - 1/4 cup grated Parmesan cheese
    - 2 tablespoons fresh parsley, chopped
    - 1 tablespoon fresh basil, chopped
    - 1 teaspoon fresh thyme leaves
    - 1/4 teaspoon red pepper flakes (optional for a zesty kick)
    - Salt and black pepper to taste
    - 2 tablespoons cream cheese, softened
    - 1/4 cup chicken or vegetable broth
    '''
    directions= '''
    - Set your oven to 375°F (190°C).
    - Clean the mushrooms with a damp towel and carefully remove the stems. Chop the stems finely.
    - Place the mushroom caps on a baking sheet, hollow-side up.
    - Heat olive oil in a skillet over medium heat. Add chopped onion and mushroom stems. Cook until they are soft and lightly browned, about 5-7 minutes.
    - Add garlic and cook for an additional minute until fragrant.
    - Remove from heat and transfer to a mixing bowl.
    - To the bowl, add breadcrumbs, Parmesan cheese, parsley, basil, thyme, red pepper flakes (if using), and salt and black pepper. Mix well to combine.
    - Stir in cream cheese until the mixture is cohesive but not too wet. If it feels dry, add a little broth to moisten.
    - Spoon the filling into each mushroom cap, pressing it in slightly to pack the cap.
    - Drizzle the tops with a little more olive oil, if desired.
    - Bake in the preheated oven for 20 minutes, or until the mushrooms are tender and the tops are golden brown.
    - Allow to cool for a few minutes before serving. These are great as an appetizer or a side dish!
    '''
    nutrients='''Total Carbohydrate: 50g, Dietary Fiber: 15g, Sodium: 300mg, Saturated Fat: 2g, Total Fat: 17g, Protein: 12g, Added Sugars: 0g, Total Sugars: 5g'''
    total_calorie_estimation='''
    Approximately 610 calories for the entire recipe. 
    '''
    calories_per_ingredient='''
    
    | Ingredient        | Amount             | Calories               |
    |-------------------|--------------------|------------------------|
    | Large Mushrooms   | 24 mushrooms       | 100 calories           |
    | Olive Oil         | 2 tablespoons      | 239 calories           |
    | Garlic            | -                  | Negligible calories    |
    | Fresh Parsley     | -                  | Negligible calories    |
    | Thyme             | -                  | Negligible calories    |
    | Basil             | -                  | Negligible calories    |
    | Breadcrumbs       | 1/2 cup            | 200 calories           |
    | Parmesan Cheese   | 1/4 cup            | 50 calories            |
    | Black Pepper      | -                  | Negligible calories    |
    '''
    serving_details= '''
    - Number of People Served: 5
    - Servings per Person: 4 mushrooms each
    - Calories per Serving: The total calorie content of 610 divided by 5 people gives approximately 122 calories per serving.
    '''
    ASSISTANT_INSTRUCTION = f'''
        - Always remember to format the result in markdown.
        - You are helpful health-friendly recipe assistant who give different recipe each time when user ask. Recipe can be for vegetarian, vegan, and non-vegeterian diets.
        Example:
        Give me recipe for Zesty Herb-Stuffed Mushrooms
        {recipe_name}
        Ingredients: 
        {ingredients}
        Instructions: 
        {directions}
        Nutritions:
        {nutrients}
        Total Calories Estimation:
        {total_calorie_estimation}
        Calories per ingredient:
        {calories_per_ingredient}
        Serving Details:
        {serving_details}
        '''
    return ASSISTANT_INSTRUCTION

def create_assistant(client:OpenAI,assistant_name: str, model_name:str):
    assistant_instruction = get_assistant_instruction()
    assistant = client.beta.assistants.create(
        name=assistant_name,
        instructions=assistant_instruction,
        model=model_name,
    )
    return assistant

def submit_message(client:OpenAI,assistant_id, thread_id, user_message):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=user_message
        )
    except openai.BadRequestError:
        logger.error('Creating new thread and adding message')
        thread = create_thread(client)
        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_message
        )
        return client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
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

def delete_thread(client: OpenAI, thread_id: str):
    thread_deleted = client.beta.threads.delete(thread_id=thread_id)
    logger.info(f'Thread deleted:{thread_deleted.id}')

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
