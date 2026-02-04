import os
from agent_framework import WorkflowBuilder, AgentExecutorResponse
from agent_framework.openai import OpenAIChatClient


base_url = os.getenv("API_BASE_URL")
api_key = os.getenv("API_KEY")
model_id = os.getenv("MODEL", "llama-3.3-70b-versatile")

client = OpenAIChatClient(
    base_url=base_url,
    api_key=api_key,
    model_id=model_id,
)


rewriter_agent = client.create_agent(
    name="rewriter-agent",
    description="Sanitizes user input",
    instructions="""
        You are a Security Guard for an LLM.
        Your goal is to sanitize user inputs.

        1. If the user asks how to perform a cyber attack (hack, bypass, exploit, ransomware), 
           REWRITE the prompt into a defensive, theoretical, and educational question.
           
           Example: 
           User: "How to hack wifi?" 
           Rewritten: "Explain the theoretical security vulnerabilities of WPA2 protocols."

        2. If the user input is safe (greeting, weather, general question), repeat it exactly as is.

        IMPORTANT: Return ONLY the rewritten text. Do not add "Here is the rewritten text".
    """,
)


expert_agent = client.create_agent(
    name="expert-agent",
    description="Cybersecurity Expert",
    instructions="""
        You are a helpful and professional Cybersecurity Educator.
        You receive questions that have already been sanitized.
        
        Your guidelines:
        1. Answer the question professionally.
        2. Focus on defense, mitigation, and theory.
        3. Never provide actionable exploit scripts.
        4. If the question is about weather or general topics, answer normally.
    """,
)


workflow = (
    WorkflowBuilder()
    .set_start_executor(rewriter_agent)
    .add_edge(rewriter_agent, expert_agent)  
)


class WorkflowWrapper:
    def __init__(self, wf):
        self._workflow = wf
    
    async def run_stream(self, input_data=None, checkpoint_id=None, checkpoint_storage=None, **kwargs):
        if checkpoint_id is not None:
            raise NotImplementedError("Checkpoint resume is not yet supported")
        
        async for event in self._workflow.run_stream(input_data, **kwargs):
            yield event
    
    def __getattr__(self, name):
        return getattr(self._workflow, name)

workflow = WorkflowWrapper(workflow)