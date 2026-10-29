from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, NamedTuple

import yaml


class ANSIRepresentation(NamedTuple):
    column: int
    row: int


MAX_ANSI_REPRESENTATION_ROW = 15
MAX_ANSI_REPRESENTATION_COLUMN = 8
SETS: tuple[str, ...] = (
    "C0",
    "C1",
    "Fs",
    "control_sequences"
)

@dataclass(frozen=True)
class ANSISequenceData:
    set: str
    ansi_repr: ANSIRepresentation
    abbreviation: str
    name: str
    argument_count: int
    default_arguments: list[int | None] | None
    description: str
    has_intermediate_byte: bool | None
    private_marker: ANSIRepresentation | None
    constants: dict[str, int]

    _invalid_sentinel = None

    @staticmethod
    def invalid() -> ANSISequenceData:
        if ANSISequenceData._invalid_sentinel is None:
            ANSISequenceData._invalid_sentinel = ANSISequenceData(
                "",
                ANSIRepresentation(-1, -1),
                "",
                "",
                -1,
                None,
                "",
                None,
                None,
                {}
            )
        return ANSISequenceData._invalid_sentinel

    @staticmethod
    def from_dict(data: dict[str, Any]) -> ANSISequenceData:
        def get_required_key(key: str) -> Any:
            if (value := data.get(key, None)) is None:
                raise KeyError(f"'{key}' key required")
            return value

        unsafe_set: str = get_required_key("set")
        unsafe_ansi_repr: ANSIRepresentation = ANSIRepresentation(get_required_key("col"), get_required_key("row"))
        unsafe_abbreviation: str = get_required_key("abbreviation")
        unsafe_name: str = get_required_key("name")
        unsafe_argument_count: int = get_required_key("argument_count")
        unsafe_default_arguments: list[int | None] | None = data.get("default_arguments", None)
        unsafe_description: str = get_required_key("description")
        unsafe_has_intermediate_byte: bool | None = data.get("has_intermediate_byte")
        unsafe_private_marker: dict[str, int] | None = data.get("private_marker")
        unsafe_constants: dict[str, int] | None = data.get("constants")

        def require_type(name: str, obj: Any, t: type) -> None:
            if not isinstance(obj, t):
                raise TypeError(f"{name} must be of type {t}")

        def require_non_empty(name: str, value: str) -> None:
            if not value:
                raise ValueError(f"{name} must be not be empty")

        require_type("set", unsafe_set, str)
        require_non_empty("set", unsafe_set)
        if unsafe_set not in SETS:
            raise ValueError(f"The set '{unsafe_set}' is invalid.")

        if unsafe_set == "control_sequences":
            if unsafe_has_intermediate_byte is None:
                raise TypeError("For the control_sequences set, 'has_intermediate_byte is not None' is required")
        else:
            if unsafe_has_intermediate_byte is not None:
                raise TypeError("For any set which is not the control_sequences set, 'has_intermediate_byte is None' is required")

        if unsafe_ansi_repr.column < 0 or unsafe_ansi_repr.column > MAX_ANSI_REPRESENTATION_COLUMN:
            raise ValueError(f"Column must be between 0 and {MAX_ANSI_REPRESENTATION_COLUMN}")
        if unsafe_ansi_repr.row < 0 or unsafe_ansi_repr.row > MAX_ANSI_REPRESENTATION_ROW:
            raise ValueError(f"Row must be between 0 and {MAX_ANSI_REPRESENTATION_ROW}")

        require_type("abbreviation", unsafe_abbreviation, str)
        require_non_empty("abbreviation", unsafe_abbreviation)

        require_type("name", unsafe_name, str)
        require_non_empty("name", unsafe_name)

        require_type("argument_count", unsafe_argument_count, int)
        if unsafe_argument_count < -1:
            raise ValueError("argument count must be greater than or equal to -1")

        if unsafe_default_arguments is not None:
            require_type("default_arguments", unsafe_default_arguments, list)
            for i, arg in enumerate(unsafe_default_arguments):
                if arg is None:
                    continue
                require_type(f"default_argument[{i}]", arg, int)

        if unsafe_argument_count == 0 and unsafe_default_arguments is not None:
            raise ValueError("Must have 'default_arguments == None' if argument count is 0.")

        if unsafe_argument_count != 0:
            if unsafe_default_arguments is None:
                raise TypeError("Must have 'default_arguments != None', event if 'argument_count == 0'")

            if unsafe_argument_count != -1 and unsafe_argument_count != len(unsafe_default_arguments):
                raise TypeError("Must have 'len(default_arguments) == argument_count' if non-variadic")

        require_type("description", unsafe_description, str)
        require_non_empty("description", unsafe_description)

        private_marker: ANSIRepresentation | None = None
        if unsafe_private_marker is not None:
            require_type("private_marker", unsafe_constants, dict)
            for key in unsafe_private_marker:
                require_type(f"private_marker key '{key}'", key, str)
            if "row" not in unsafe_private_marker:
                raise KeyError("Required key 'row' for private_marker")
            if "col" not in unsafe_private_marker:
                raise KeyError("Required key 'col' for private_marker")
            for key, value in unsafe_private_marker.items():
                require_type(f"constants[{key}]", value, int)
            private_marker = ANSIRepresentation(unsafe_private_marker["col"], unsafe_private_marker["row"])

        if unsafe_constants is not None:
            require_type("constants", unsafe_constants, dict)
            for key in unsafe_constants:
                require_type(f"constants key '{key}'", key, str)
                normalized = key.replace(" ", "_").replace("-", "_").replace(",", "_")
                if not normalized.isidentifier():
                    raise ValueError(f"Constant's name '{key}' did not normalize ({normalized}) to an identifier")
            for key, value in unsafe_constants.items():
                require_type(f"constants[{key}]", value, int)

        return ANSISequenceData(
            unsafe_set,
            unsafe_ansi_repr,
            unsafe_abbreviation,
            unsafe_name,
            unsafe_argument_count,
            unsafe_default_arguments,
            unsafe_description,
            unsafe_has_intermediate_byte,
            private_marker,
            unsafe_constants or {},
        )


__sequence_cache: tuple[ANSISequenceData, ...] | None = None

def sequences() -> tuple[ANSISequenceData, ...]:
    global __sequence_cache

    if __sequence_cache is None:
        with open("ansi.json", "r") as f:
            __sequence_cache = tuple(sorted(
                [ANSISequenceData.from_dict(seq) for seq in json.loads(f.read())],
                key=lambda seq: seq.abbreviation
            ))
    return __sequence_cache


def main() -> None:
    seqs = sequences()
    print(f"There are {len(seqs)}:")

    for seq in seqs:
        print(seq.abbreviation)

    with open("ansi.json", "r") as json_file, open("ansi.yaml", "w", encoding="utf-8") as yaml_file:
        yaml_file.write(yaml.dump(json.loads(json_file.read()), indent=2))


if __name__ == "__main__":
    main()