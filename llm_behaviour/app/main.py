from fastapi import FastAPI
from pydantic import BaseModel,Field

from llm_behaviour.app.services.gemini import generate_response


app = FastAPI(
    title="LLM Behavior Lab",
    description=(
        "A hands-on FastAPI lab for understanding "
        "LLM generation behavior and limitations."
    ),
    version="1.0.0",
)

class PromptRequest(BaseModel):
    prompt:str=Field(..., 
                     min_length=1,
                     max_length=5000,
                     descripton="Prompt to send to the LLM")

class TemperatureRequest(BaseModel):
    prompt:str=Field(...,
                     min_length=1,
                     max_length=5000)
    temperature:float=Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description='Controls  variation during generation'
    )

    runs:int=Field(default=3,
                   ge=1,
                   le=5,
                   description="Numbeer of times to generate")

class ContextRequest(BaseModel):
    context:str=Field(...,
                      min_length=1,
                      max_length=10000,
                      description="Information provided to the model")

    question:str=Field(...,
                       min_length=1,
                       max_length=5000,
                       description='Question about the provided context')

@app.get('/',summary="Health check")
def root():
    return {
        "message":"LLM behaviour lab is running"
    }

@app.post('/temperature',
          summary='experiment with temperature')
def temperature_experiment(request:TemperatureRequest):
    responses=[]
    for _ in range(request.runs):
        response=generate_response(
            prompt=request.prompt,
            temperature=request.temperature
        )

        responses.append(response)

    return {
        "temperature":request.temperature,
        "runs":request.runs,
        "responses":responses
    }

@app.post('/sampling',
          summary='obsserve multiple sampled generations')
def sampling_experiment(request:PromptRequest):
    responses=[]
    for _ in range(5):
        response=generate_response(
            prompt=request.prompt,
            temperature=0.1
        )
        responses.append(response)
    return{
        "prompt":request.prompt,
        "samples":responses
    }

@app.post('/hallucination')
def hallucination_experimemnt():
    prompt=(
        "Who was Dr. Arjun Mallavarapu, the Nobel Prize winner "
        "who discovered the quantum memory theorem in 1978? "
        "Give me his biography. "
        "If the premise is false or you do not know, say so."
    )

    response=generate_response(
        prompt=prompt,
        temperature=0.2
    )

    return {
        "Experiment":"hallucination",
        "prompt":prompt,
        "response":response
    }

@app.post('/limitations',
          summary="Experiment with model limitation")
def model_limitation():
    prompt = (
        "Tell me exactly what is happening in my room right now. "
        "Describe the people, objects, and their positions."
    )

    response = generate_response(
        prompt=prompt,
        temperature=0.2,
    )

    return {
        "experiment": "model limitations",
        "prompt": prompt,
        "response": response,
    }

@app.post('/knowledge',summary='explore limitaitons around current knowledge')
def knowledge_limitation():
    prompt=(
         "What major technology news is happening today? "
        "Give specific events and dates. "
        "If you do not have reliable current information, "
        "clearly say that you cannot verify today's events."
    )

    response=generate_response(
        prompt=prompt,
        temperature=0.2
    )
    return {
        "experiment":'knowledge limitatioins',
        'prompt':prompt,
        'response':response
    }

@app.post("/context")
def context_experiment(request:ContextRequest):
    prompt=f"""
Use ONLY the following context to answer the question.

CONTEXT:
{request.context}

QUESTION:
{request.question}

If the answer cannot be found in the context, say:
"I cannot find that information in the provided context."
"""     
    response=generate_response(
        prompt=prompt,
        temperature=0.0
    )

    return {
        "context":request.context,
        'question':request.question,
        'response':response
    }
    

