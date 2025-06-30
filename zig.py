from main import build


def main() -> None:
    control_sequence_introducer, constants, controls = build()
    with open("ansi.zig", "w", encoding="utf-8") as out:
        with open("ansi.include.zig", "r", encoding="utf-8") as include:
            out.write(include.read())
        out.write(f"pub const CSI = \"{control_sequence_introducer}\";\n\n")
        for control in controls:
            out.write(f"pub const {control['name']} = ANSI {{\n")
            out.write(f"\t.sequence = \"{control['sequence']}\",\n")
            out.write(f"\t.no_of_arguments = {control['no_of_arguments']},\n")
            out.write(f"\t.no_of_default_arguments = {control['no_of_default_arguments']},\n")
            out.write("};\n\n")

        for i, (constant, value) in enumerate(constants.items()):
            out.write(f"pub const {constant} = {int(value)};\n")
            if i != len(constants) - 1:
                out.write("\n")
        print(out.name)


if __name__ == "__main__":
    main()
