import asyncio
import os
import sys

from browser_use.llm.openai.chat import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import os

from dotenv import load_dotenv
from gologin import GoLogin
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv(".env")

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_URL = os.getenv("LLM_API_URL", "")
LLM_MODEL: str = os.getenv("LLM_MODEL", "")

cdp_url = "wss://test-crowlogin-browser.crowlingo.com/browsers/crowlogin-browser-profile-ep3uy2cvwbvgp5tqsxprde/RFGc3F4PkpUppAhfcE6Uy3/ws/devtools/browser/e4d40661-52db-4b8b-bd95-3ad79c6078a4"

user_info: dict[str, str] = {
	"username": "LewisRayna37782",
	"password": "6uOKXTkgrBB8",
	"url": "https://www.linkedin.com/in/evelyn-jackson-554623356/",
}

gl_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjA2Njk0MDRlZjRhOTVjY2IyN2IwMjgiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NmZkODZlYjhkOWIxNzkyYjQwZTdiYzQifQ.bMDgzBdjvqQ_tYRMuXq4sd0dI62gYlBLpw1EM2EJADw"
gl_profile: str = "67e44200cc5fc417e4551867"


async def run_search():
	gl = GoLogin(
		options={
			"token": gl_token,
			"profile_id": gl_profile,
		},
	)
	folder: str = "Twitter"
	profile = gl.getProfile()
	debugger_address = gl.start()
	config = BrowserConfig(
		cdp_url="http://" + debugger_address,
	)
	browser = Browser(config=config)
	agent = Agent(
		task=(
			"I have an automatic captcha solver, so just wait when there is one. If captcha is not getting solved, try solve it by yourself."
			"Try to sign in to "
			+ folder
			+ " if browser is not logged. If browser is logged through another username, it is still a success, only if you see contents such as tweets."
			"My information are the following: " + json.dumps(profile["notes"])
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
	gl.stop()


if __name__ == "__main__":
	asyncio.run(run_search())
