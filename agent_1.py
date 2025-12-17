root_agent = Agent(
    name=agent_name,
    model=Gemini(
        model=agent_model,
        retry_options=retry_config
    ),
    description=agent_description,
    instruction=agent_instruction,
    tools=agent_tools,
)
print("✅ Root Agent defined.")

runner = InMemoryRunner(agent=root_agent)
print("✅ Runner created.")
