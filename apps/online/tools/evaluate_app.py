from pathlib import Path
from typing import List

import click

from online.application.evaluation import evaluate_agent

EVALUATION_PROMPTS: List[str] = [
    """
Write me a paragraph on the creative process in music production following the next structure:

- introduction
- what are its main components
- why it's powerful

Retrieve the sources when compiling the answer. Also, return the sources you used as context.
""",
    "What is the creative process in music production?",
    "What is the Ableton Live Digital Audio Workstation?",
    """How does deliberate practice in music skill development work?

Explain to me:
- what is deliberate practice
- how it works
- why it's important
- what are the main components
- what are the main challenges
""",
    "List 3 digital audio workstations for creating electronic music and why they are important.",
    "Explain how does sound synthesis work. Focus on what architecture it uses, how it's different from other sound creation methods and how synthesizers are programmed.",
    "List 5 ways or tools to incorporate AI into music composition and production",
    """How can I optimize my music production workflow?

Provide a list of top 3 best practices, while providing a short explanation for each, which contains why it's important.
""",
    "Explain to me in more detail how does musical memory work and why do we need it when developing improvisation skills.",
    "What is the difference between a sample library and a virtual instrument?",
    "Recommend me a course on music production and sound design",
    "How does arrangement structure affect a musical composition and its emotional impact?",
    """What is the importance of mastering in music production?
Explain to me:
- what is mastering
- how it works
- why it's important
- what are the main components
- what are the main trade-offs
""",
    "List the most popular advanced production techniques to optimize sonic quality and why they are important.",
    "List what are the main ways of evaluating a musical composition and why they are important.",
]

@click.command()
@click.option(
    "--retriever-config-path",
    type=click.Path(exists=True, path_type=Path),
    help="path to the retriever configuration file",
)
def main(retriever_config_path: Path) -> None:
    """Evaluate agent with custom retriever configuration"""
    evaluate_agent(EVALUATION_PROMPTS, retriever_config_path=retriever_config_path)

if __name__ == "__main__":
    main()