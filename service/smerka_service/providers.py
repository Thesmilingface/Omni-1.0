"""Provider adapters with bounded timeouts and secret-safe errors."""
from typing import Any
import httpx
from .config import Settings

class ProviderError(RuntimeError):
    pass

async def complete(settings: Settings, messages: list[dict[str, str]]) -> str:
    key = settings.api_key()
    if not key:
        raise ProviderError(f"No API key configured for provider '{settings.provider}'. Set its key in your local .env file.")
    timeout = httpx.Timeout(settings.timeout_seconds, connect=min(10.0, settings.timeout_seconds))
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            if settings.provider in {"groq", "openai"}:
                base = settings.api_base if settings.provider == "groq" else __import__("os").getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
                response = await client.post(f"{base}/chat/completions", headers={"Authorization": f"Bearer {key}"}, json={"model": settings.model, "messages": messages, "temperature": 0.7})
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            if settings.provider == "gemini":
                # Gemini REST API; key is placed in a header, never in a URL/log.
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.model}:generateContent"
                contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]} for m in messages]
                response = await client.post(url, headers={"x-goog-api-key": key}, json={"contents": contents, "generationConfig": {"temperature": 0.7}})
                response.raise_for_status()
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise ProviderError("The AI provider could not be reached. Check the network and retry.") from exc
        except httpx.HTTPStatusError as exc:
            code = exc.response.status_code
            if code == 401 or code == 403:
                raise ProviderError("The provider rejected the credentials or access. Check provider settings.") from exc
            if code == 429:
                raise ProviderError("The provider rate limit was reached. Wait before retrying.") from exc
            raise ProviderError(f"The provider returned HTTP {code}. Check provider/model configuration.") from exc
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise ProviderError("The provider returned an unexpected response format.") from exc
    raise ProviderError(f"Unsupported provider '{settings.provider}'. Choose groq, gemini, or openai.")
