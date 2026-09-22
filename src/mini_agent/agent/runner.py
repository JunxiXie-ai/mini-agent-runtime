from mini_agent.agent.loop import AgentLoop


def run_agent(goal: str) -> str:
    agent = AgentLoop()

    return agent.run(goal)