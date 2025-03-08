def define_type(basename, class_name, fields):
    fields.insert(0, "token")
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
    
EXPR_TYPES = [
    "Binary : left, operator, right",
    "Call : callee, paren, arguments",
    "Grouping : expression",
    "Literal : value",
    "Logical : left, operator, right",
    "Unary : operator, right",
    "Identifier : name",
    "Assign: name, value",
]

STMT_TYPES = [
    "Expression : expression",
    "Print : expression",
    "If : condition, if_branch, else_branch",
    "While : condition, body",
    "Block : statements",
    "Switch : expr, cases",
]
if __name__ == "__main__":
    define_ast("SNEK2", "Expression", EXPR_TYPES)
    define_ast("SNEK2", "Statement", STMT_TYPES)