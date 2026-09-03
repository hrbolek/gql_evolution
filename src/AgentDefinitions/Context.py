from dataclasses import dataclass


@dataclass
class AgentContext:
    """
    Runtime dependencies available to agent tools.

    Later this context can contain:
    - GraphQL client
    - delegated authentication token
    - effective user information
    - federation/subgraph endpoint
    - audit/correlation identifiers
    """

    subgraph_name: str = "demo"