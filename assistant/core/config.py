from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no pragma cover
    from typing import Any


math_symbols_mapping: dict[str, str] = {
    "equal": "=",
    "plus": "+",
    "minus": "-",
    "asterisk": "*",
    "divide": "/",
    "modulo": "mod",
    "power": "**",
    "square root": "**(1/2)",
}

math_tags: str = ",".join(list(math_symbols_mapping.keys()))

analyzer_config: dict[str, "Any"] = {
    "args": {
        "stop_words": None,
        "lowercase": True,
        "norm": "l1",
        "use_idf": False,
    },
    "sensitivity": 0.2,
}

assistant_name: str = "jean-michel"  # to replace
