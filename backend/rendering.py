from html import escape


def render_agent_message(agent: dict[str, str], message: str, elapsed: str) -> str:
    name = escape(str(agent.get("name", "Agent")))
    icon = escape(str(agent.get("icon", "")))
    safe_message = escape(message)
    safe_elapsed = escape(elapsed)
    return (
        f'<article class="agent-message"><header>{icon} {name}</header>'
        f'<div>{safe_message}</div><small>{safe_elapsed}</small></article>'
    )
