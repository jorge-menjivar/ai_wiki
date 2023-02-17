from pipeline import PipelineCloud
from settings import getSettings

settings = getSettings()


def infer(api: PipelineCloud, text: str):
    # Downloading data for title

    run = api.run_pipeline(
        settings.mystic_gpt3_j_id,
        [
            text,
            {
                "response_length": 128,
                "temperature": 0.10,
                "top_k": 50,
                "repetition_penalty": 1.25
            },
        ],
    )

    if run.error_info:
        quit()

    if run.result_preview is not None:
        return run.result_preview[0][0]

    return ""
