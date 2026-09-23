"""Simulated external API call with random latency and failures."""


async def call_external_api(title: str, description: str | None) -> dict:
    # TODO: sleep a random amount, fail with settings.external_api_failure_rate
    raise NotImplementedError
