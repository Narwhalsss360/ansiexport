from dataclasses import asdict
from copy import deepcopy
import npycli.ansi as ansi
import json
import yaml


def use_escape(s: str) -> str:
    return repr(s)[1:-1]


def build() -> tuple[str, dict[str, int], list[dict]]:
    constants: dict[str, int] = {}
    controls: list[dict] = []

    for attr_name in dir(ansi):
        if attr_name.startswith("__"):
            continue
        attr = getattr(ansi, attr_name)
        if isinstance(attr, ansi.ANSIControl):
            controls.append(asdict(deepcopy(attr)))
        elif isinstance(attr, int):
            constants[attr_name] = attr

    return use_escape(ansi.ANSIControl.CSI), constants, controls


def main() -> str | None:
    control_sequence_introducer, constants, controls = build()

    print(f"{len(constants)} constants and {len(controls)} controls")
    export = {
        "control_sequence_introducer": control_sequence_introducer,
        "constants": constants,
        "controls": controls
    }

    with open("ansi.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(export, indent=4))
    with open("ansi.yaml", "w", encoding="utf-8") as f:
        f.write(yaml.dump(export, indent=2))


if __name__ == "__main__":
    if (result := main()):
        print(result)
