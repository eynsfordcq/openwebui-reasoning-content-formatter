"""
title: Reasoning Content Formatter
author: eynsfordcq
github_url: https://github.com/eynsfordcq/openwebui-reasoning-content-formatter
version: 0.2
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
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
        self.valves = self.Valves()
        self.thinking_open = False

    def stream(self, event: dict) -> dict:
        reasoning_tag = self.valves.reasoning_tag
        content_tag = self.valves.content_tag
        
        if not event.get("choices"):
            return event
        
        delta = event["choices"][0].get("delta", {})
        if not delta.get(content_tag) and delta.get(reasoning_tag):
            reasoning_text = delta[reasoning_tag]
            if not self.thinking_open:
                delta[content_tag] = f"<thinking>{reasoning_text}"
                self.thinking_open = True
            else:
                delta[content_tag] = reasoning_text

            # clear the reasoning field.
            delta[reasoning_tag] = ""

        elif delta.get(content_tag) and self.thinking_open:
            delta[content_tag] = (
                f"</thinking>\n{delta[content_tag]}"
            )
            self.thinking_open = False

        return event
