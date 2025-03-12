"""
title: Reasoning Content Formatter
author: eynsfordcq
github_url: https://github.com/eynsfordcq/openwebui-reasoning-content-formatter
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    # Valves: Configuration options for the filter
    class Valves(BaseModel):
        content_tag: str = Field(
            default="content",
            description="The content tag of the api response. Defaults to 'content'.",
        )
        reasoning_tag: str = Field(
            default="reasoning",
            description="The reasoning tag of the api response. Defaults to 'reasoning', some provider uses 'reasoning_content'.",
        )

    def __init__(self):
        # Initialize valves (optional configuration for the Filter)
        self.valves = self.Valves()
        self.thinking_open = False

    def stream(self, event: dict) -> dict:
        choices = event.get("choices", [])
        if not choices:
            return event
        delta = choices[0].get("delta", {})

        if delta.get(self.valves.content_tag, "") == "" and delta.get(
            self.valves.reasoning_tag
        ) not in (None, ""):
            reasoning_text = delta[self.valves.reasoning_tag]
            if not self.thinking_open:
                delta[self.valves.content_tag] = f"<thinking>{reasoning_text}"
                self.thinking_open = True
            else:
                delta[self.valves.content_tag] = reasoning_text

            # clear the reasoning field.
            delta[self.valves.reasoning_tag] = ""

        elif delta.get(self.valves.content_tag, "") != "" and self.thinking_open:
            delta[self.valves.content_tag] = (
                f"</thinking>\n{delta[self.valves.content_tag]}"
            )
            self.thinking_open = False

        return event
