"""A tiny local stub for GoogleSearch used only for offline testing.

This file is intentionally simple and is not imported by the production
`agent.py`. Use it from `scripts/check_tools.py` by setting
`EDUSCRIBE_USE_LOCAL_GOOGLESEARCH=1` in your environment.

The stub provides a minimal `GoogleSearch` class so the rest of the
tooling can detect the presence of a search tool without making network
calls.
"""

class GoogleSearch:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def search(self, query: str, max_results: int = 3):
        """Return a small deterministic, fake search result list.

        Keeps output consistent for offline CI or reviewer demos.
        """
        # Very small deterministic results to exercise tool-detection only
        return [
            {
                "title": "Local Stub Result for: %s" % query,
                "snippet": "This is a deterministic stub response. Replace with ADK GoogleSearch for real results.",
                "url": "http://example.local/%s" % query.replace(' ', '_')
            }
        ][:max_results]
