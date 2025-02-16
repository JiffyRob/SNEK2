def define_type(basename, class_name, fields):
    string = f"class {class_name}({basename}):"
    string += f"\n    def __init__(self, {', '.join(fields)}):"
    for field in fields:
        string += f"\n        self.{field} = {field}"

    string += "\n\n    def accept(self, visitor):"
    string += f"\n        return visitor.visit_{class_name.lower()}(self)"

    return string + "\n\n"


def define_ast(output_dir, basename, types):
    path = f"{output_dir}/{basename.lower()}.py"
    with open(path, "w") as f:
        f.write("# AUTO GENERATED FILE\n\n")
        f.write(f"class {basename}:\n")
        f.write("    pass\n\n")
        for type in types:
            class_name, fields = type.split(":")
            class_name = class_name.strip()
            fields = [field.strip() for field in fields.split(",")]
            f.write(define_type(basename, class_name, fields))
    
TYPES = [
    "Binary : left, operator, right",
    "Grouping : expression",
    "Literal : value",
    "Unary : operator, right"
]
if __name__ == "__main__":
    define_ast(".", "Expression", TYPES)