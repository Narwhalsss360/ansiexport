from pathlib import Path
from shutil import copy
from typing import TextIO

import export_base
from export_base import ANSISequenceData

SEQUENCES: tuple[ANSISequenceData, ...] = tuple(sorted(export_base.sequences(), key=lambda seq: seq.set))


__by_set: dict[str, list[ANSISequenceData]] = {}


def by_set() -> dict[str, list[ANSISequenceData]]:
    if not __by_set:
        for sequence in SEQUENCES:
            if sequence.set not in __by_set:
                __by_set[sequence.set] = []
            __by_set[sequence.set].append(sequence)
    return __by_set


def sequence_identifier(sequence: ANSISequenceData) -> str:
    return sequence.abbreviation


def sequence_type(sequence: ANSISequenceData) -> str:
    if sequence.set == "C0":
        return "C0ControlFunction"

    if sequence.set == "C1":
        return "C1ControlFunction"

    if sequence.set == "Fs":
        return "IndependentControlFunction"

    if sequence.set == "control_sequences":
        return "ControlSequence"

    assert False, "Unreachable"


def escaped(text: str, with_quotes: bool = True) -> str:
    representation = repr(text)
    if with_quotes:
        return representation
    else:
        return representation[1:-1]


def bool_literal(value: bool) -> str:
    return "True" if value else "False"


def default_arguments_literal(default_arguments: list[int | None] | None) -> str:
    if default_arguments is None:
        return "None"

    if len(default_arguments) == 1:
        return f"({default_arguments[0]},)"

    return f"({' ,'.join(str(x) for x in default_arguments)})"


def init_token_const(sequence: ANSISequenceData) -> str:
    if sequence.set == "C0":
        return f"ControlByteToken(bit_combination=BitCombination({
            sequence.ansi_repr.column}, {
            sequence.ansi_repr.row})) "

    if sequence.set == "C1":
        return f"EscapeSequenceToken(intermediate_bit_combinations=EMPTY_SEQUENCE, final_bit_combination=BitCombination({sequence.ansi_repr.column}, {sequence.ansi_repr.row}))"

    if sequence.set == "Fs":
        return f"EscapeSequenceToken(intermediate_bit_combinations=EMPTY_SEQUENCE, final_bit_combination=BitCombination({sequence.ansi_repr.column}, {sequence.ansi_repr.row}))"

    if sequence.set == "control_sequences":
        return f"ControlSequenceToken(ControlSequenceToken.SEVEN_BIT_MODE_INTRODUCER, private_marker={f"ControlByteToken(bit_combination=BitCombination({sequence.private_marker.column}, {sequence.private_marker.row}))" if sequence.private_marker is not None else None}, intermediate_bit_combinations_sequence={"(BitCombination(2, 0),)" if sequence.has_intermediate_byte else "EMPTY_SEQUENCE"}, arguments=EMPTY_PARAMETERS, final_bit_combination=BitCombination({sequence.ansi_repr.column}, {sequence.ansi_repr.row}))"

    assert False, "Unreachable"


def sequence_const(sequence: ANSISequenceData) -> str:
    return (
        f"{sequence_identifier(sequence)} = {sequence_type(sequence)}(\n"
        f"    abbreviation={escaped(sequence.abbreviation)},\n"
        f"    name={escaped(sequence.name)},\n"
        f"    argument_count={sequence.argument_count},\n"
        f"    default_arguments={default_arguments_literal(sequence.default_arguments)},\n"
        f"    description={escaped(sequence.description)},\n"
        f"    init_token={init_token_const(sequence)}\n"
        f")"
    )


def sequences(file: TextIO) -> None:
    file.write(
        "from .sequence_types import (\n"
        "    EMPTY_PARAMETERS,\n"
        "    EMPTY_SEQUENCE,\n"
        "    BitCombination,\n"
        "    C0ControlFunction,\n"
        "    C1ControlFunction,\n"
        "    ControlByteToken,\n"
        "    ControlSequence,\n"
        "    ControlSequenceToken,\n"
        "    EscapeSequenceToken,\n"
        "    IndependentControlFunction,\n"
        ")\n\n"
    )

    for sequence in SEQUENCES:
        file.write(sequence_const(sequence))
        file.write('\n\n')

    for set, sequences in by_set().items():
        file.write(
            f"{set.upper()} = frozenset({{\n" +
            ",\n".join([f"    {sequence_identifier(seq)}" for seq in sequences]) + "\n" +
            "})\n\n"
        )

    file.write(
        "SETS = frozenset({\n" +
        ",\n".join([f"    {set.upper()}" for set in by_set()]) + "\n" +
        "})\n\n"
    )

    file.write("__all__ = [\n")
    file.write(",\n".join(f"    {sequence_identifier(sequence)!r}" for sequence in SEQUENCES))
    file.write(',\n')
    file.write(",\n".join(f"    {set.upper()!r}" for set in by_set()))
    file.write(",\n    'SETS'")
    file.write("\n]")


def name_to_identifier(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_").replace(",", "_")


def constants(dir: Path) -> None:
    if not dir.exists():
        dir.mkdir()

    if not dir.is_dir():
        raise NotADirectoryError()

    with open(dir.joinpath("all.py"), "w", encoding='utf-8') as all_file:
        for sequence in SEQUENCES:
            if not sequence.constants:
                continue

            as_identifier = {name_to_identifier(name): value for name, value in sequence.constants.items()}
            with open(dir.joinpath(f"{sequence.abbreviation.lower()}.py"), "w", encoding='utf-8') as sequence_file:
                sequence_file.write("\n".join(f"{name} = {value}" for name, value in as_identifier.items()))
                sequence_file.write("\n\n__all__ = [\n")
                sequence_file.write(",\n".join(f"    {name!r}" for name in as_identifier))
                sequence_file.write("\n]")

            all_file.write(f"from .{sequence.abbreviation.lower()} import (\n")
            all_file.write(",\n".join(f"    {name}" for name in as_identifier))
            all_file.write("\n)\n")

        all_file.write("\n__all__ = [\n")
        all_file.write(
            ",\n".join(
                f"    {name_to_identifier(name) !r} "for sequence in SEQUENCES for name in sequence.constants
                if sequence.constants))
        all_file.write("\n]")


def main() -> None:
    copy("sequence_types.py", "generated/src/ansiexport")
    with open("generated/src/ansiexport/sequences.py", "w", encoding='utf-8') as sequences_file:
        sequences(sequences_file)
    constants(Path("generated/src/ansiexport/const/"))


if __name__ == "__main__":
    main()
