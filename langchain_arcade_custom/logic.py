from dotenv import load_dotenv
import os
from arcadepy import Arcade

# Check if LangGraph is enabled
LANGGRAPH_ENABLED = True
try:
    from langgraph.errors import NodeInterrupt
except ImportError:
    LANGGRAPH_ENABLED = False

load_dotenv()

def handle_tool_authorization(
    client: Arcade,
    tool_name: str,
    user_id: str | None,
    langgraph: bool = False,
) -> dict[str, str] | None:
    """Handle tool authorization for a given user.
    """
    if user_id is None:
        error_message = f"user_id is required to run {tool_name}"
        if langgraph:
            raise NodeInterrupt(error_message)
        return {"error": error_message}

    # Authorize the user for the tool
    auth_response = client.tools.authorize(tool_name=tool_name, user_id=user_id)
    if auth_response.status != "completed":
        auth_message = (
            "Please use the following link to authorize: "
            f"{auth_response.authorization_url}"
        )
        if langgraph:
            raise NodeInterrupt(auth_message)
        return {"error": auth_message}
    
    return None

def get_default_attendees(sender_id: str) -> list[str]:
    """Get default attendees for a given sender_id.
    """
    mock_attendees = {"1234":[]}
    return mock_attendees.get(sender_id)

def get_user_id(sender_id: str) -> str:
    """Get user_id for a given sender_id.
    """
    mock_user_id = {"1234":os.environ['ARCADE_USER_ID']}
    return mock_user_id.get(sender_id)
