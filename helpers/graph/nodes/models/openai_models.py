import asyncio
import os
import openai
from openai import AsyncOpenAI

# call_openai_model_code = """
# import asyncio
# import os
# import openai
# from openai import AsyncOpenAI

# async def call_openai_model(model: str, prompt: str, api_key: str):
#     client = AsyncOpenAI(api_key=api_key)
#     response = await client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#     )
#     return response.choices[0].message.content

# result = asyncio.run(call_openai_model("gpt-4o-mini", "Hello, world!", ""))
# """
# call_openai_model_code = call_openai_model_code.format(api_key="")

# openai_result = {}
# exec(call_openai_model_code, openai_result)


async def call_openai_model(model: str, prompt: str, api_key: str):
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
