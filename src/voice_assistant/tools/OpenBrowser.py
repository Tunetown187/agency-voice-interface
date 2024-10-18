import asyncio
import json
import logging
import os
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

from agency_swarm.tools import BaseTool
from pydantic import Field

from voice_assistant.models import WebUrl
from voice_assistant.utils.decorators import timeit_decorator

logger = logging.getLogger(__name__)

with open(os.getenv("PERSONALIZATION_FILE")) as f:
    personalization = json.load(f)
browser_urls = personalization["browser_urls"]
browser = personalization["browser"]

class OpenBrowser(BaseTool):
    """A tool to open a browser with a URL based on the user's prompt."""
    chain_of_thought: str = Field(
        ..., description="Step-by-step thought process to determine the URL to open."
    )
    url: str = Field(
        ..., description="The URL to open. Available options: " + ", ".join(browser_urls)
    )

    @timeit_decorator
    async def run(self):
        """
        Open a browser with the best-fitting URL based on the user's prompt.
        """
        if self.url:
            logger.info(f"📖 open_browser() Opening URL: {self.url}")
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(
                    pool, webbrowser.get(browser).open, self.url
                )
            return {"status": "Browser opened", "url": self.url}
        return {"status": "No URL found"}


if __name__ == "__main__":
    tool = OpenBrowser(chain_of_thought="I want to open my favorite website", url="https://www.linkedin.com")
    asyncio.run(tool.run())
