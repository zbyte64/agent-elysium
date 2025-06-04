import logging

from pydantic_ai import Agent as BaseAgent


class Agent(BaseAgent):
    async def run(self, *args, **kwargs):
        result = await super().run(*args, **kwargs)
        logging.debug(result.output)
        return result
