import openai
from settings import get_settings

settings = get_settings()


async def aInfer(text: str):

    response = await openai.Completion.acreate(
        model="text-curie-001",
        prompt=text,
        temperature=0,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    content: str = response.choices[0].text  # type: ignore
    model: str = f'gpt3-{response.model}'  # type: ignore
    return content, model


def infer(text: str):

    response = openai.Completion.create(
        model="text-curie-001",
        prompt=text,
        temperature=0,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    content: str = response.choices[0].text  # type: ignore
    model: str = f'gpt3-{response.model}'  # type: ignore
    return content, model
