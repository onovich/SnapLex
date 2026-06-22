from snaplex.providers import TranslationRequest, TranslationResponse
from snaplex.services import InMemoryTranslationCache, TranslationCacheKey


def test_cache_key_uses_request_values_and_provider_name() -> None:
    request = TranslationRequest(text="hello", source_lang="en", target_lang="es")

    key = TranslationCacheKey.from_request(request, provider_name="fake")

    assert key.text == "hello"
    assert key.source_lang == "en"
    assert key.target_lang == "es"
    assert key.provider_name == "fake"


def test_in_memory_cache_returns_stored_response() -> None:
    cache = InMemoryTranslationCache()
    key = TranslationCacheKey("hello", "en", "es", "fake")
    response = TranslationResponse("hola", "fake", "en", "es")

    cache.set(key, response)

    assert cache.get(key) == response
    assert len(cache) == 1
