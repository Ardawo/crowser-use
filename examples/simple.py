import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use import Agent, Browser, BrowserConfig

load_dotenv(".env.example")

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_URL = os.getenv("LLM_API_URL", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")

cdp_url = "wss://test-crowlogin-browser.crowlingo.com/browsers/crowlogin-browser-profile-ep3uy2cvwbvgp5tqsxprde/RFGc3F4PkpUppAhfcE6Uy3/ws/devtools/browser/e4d40661-52db-4b8b-bd95-3ad79c6078a4"

user_info: dict[str, str] = {"username": "LewisRayna37782","password":"6uOKXTkgrBB8","url":"https://www.linkedin.com/in/evelyn-jackson-554623356/"}

async def run_search():
	config = BrowserConfig(
		cdp_url=cdp_url,
	)
	browser = Browser(config=config)
	agent = Agent(
		task=(
			"I have an automatic captcha solver, so just wait when there is one."
			"Create hotmail mail with the following information: " + json.dumps(user_info)
		),
		llm=ChatOpenAI(
			base_url=LLM_API_URL,
			model=LLM_MODEL,
			api_key=SecretStr(LLM_API_KEY),
		),
		browser=browser,
			use_vision=False,
	)
	await agent.run()


if __name__ == "__main__":

	asyncio.run(run_search())
