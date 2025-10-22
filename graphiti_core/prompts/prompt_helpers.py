"""
Copyright 2024, Zep Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
from datetime import date, datetime, time
from typing import Any

DO_NOT_ESCAPE_UNICODE = "\nDo not escape unicode characters.\n"


class PromptJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for serializing data to prompts.

    Handles special types that are not natively JSON serializable:
    - datetime objects (including Neo4j DateTime)
    - date objects
    - time objects
    """

    def default(self, obj):
        # Handle standard datetime objects
        if isinstance(obj, datetime):
            return obj.isoformat()
        # Handle date objects
        if isinstance(obj, date):
            return obj.isoformat()
        # Handle time objects
        if isinstance(obj, time):
            return obj.isoformat()
        # Handle Neo4j temporal types (DateTime, Date, Time, etc.)
        # These have an iso_format() method
        if hasattr(obj, "iso_format") and callable(obj.iso_format):
            return obj.iso_format()
        # Fallback to default behavior
        return super().default(obj)


def to_prompt_json(
    data: Any, ensure_ascii: bool = False, indent: int | None = None
) -> str:
    """
    Serialize data to JSON for use in prompts.

    Args:
        data: The data to serialize
        ensure_ascii: If True, escape non-ASCII characters. If False (default), preserve them.
        indent: Number of spaces for indentation. Defaults to None (minified).

    Returns:
        JSON string representation of the data

    Notes:
        By default (ensure_ascii=False), non-ASCII characters (e.g., Korean, Japanese, Chinese)
        are preserved in their original form in the prompt, making them readable
        in LLM logs and improving model understanding.

        Handles Neo4j temporal types (DateTime, Date, Time) and standard Python datetime objects.
    """
    return json.dumps(
        data, ensure_ascii=ensure_ascii, indent=indent, cls=PromptJSONEncoder
    )
