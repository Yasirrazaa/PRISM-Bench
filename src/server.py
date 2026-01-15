"""
PRISM Server: A2A server for the PRISM Cultural Intelligence benchmark.
"""

import argparse
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from executor import Executor


def main():
    parser = argparse.ArgumentParser(description="Run the PRISM benchmark agent.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=9009, help="Port to bind the server")
    parser.add_argument("--card-url", type=str, help="URL to advertise in the agent card")
    args = parser.parse_args()

    # PRISM Agent Card
    skill = AgentSkill(
        id="prism_cultural_intelligence",
        name="Cultural Intelligence Evaluation",
        description="Evaluates AI systems on Normative Agility - the capacity to recognize "
                    "that 'right' and 'wrong' vary by cultural context. Tests for cultural "
                    "imperialism (Level 1) and stereotype resistance (Level 2).",
        tags=["cultural-intelligence", "benchmark", "PGAF", "ethics", "bias", "evaluation"],
        examples=[
            "Evaluate an AI's response to cross-cultural ethical dilemmas",
            "Test for Western-centric defaults in moral reasoning",
            "Assess stereotype resistance when handling individual-vs-group scenarios"
        ]
    )

    agent_card = AgentCard(
        name="PRISM",
        description="PRISM: Pluralistic Reasoning & Identity-Specific Modeling. "
                    "A Cultural Intelligence (CQ) benchmark that tests AI's capacity to swap "
                    "'Moral Operating Systems' based on context. Unlike ethics benchmarks "
                    "(right vs wrong) or bias benchmarks (harm detection), PRISM tests whether "
                    "the AI knows that 'right' changes depending on where you are standing.",
        url=args.card_url or f"http://{args.host}:{args.port}/",
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill]
    )

    request_handler = DefaultRequestHandler(
        agent_executor=Executor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=args.host, port=args.port)


if __name__ == '__main__':
    main()
