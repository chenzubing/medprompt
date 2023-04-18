from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, meta


class Medprompt:
    def __init__(
        self, template_path: str,
        template_name: str,
        allowed_missing_variables: Optional[List[str]] = None,
        default_variable_values: Optional[Dict[str, Any]] = None,
        ):
        self.template_path = template_path
        self.template_name = template_name
        self.env = Environment(loader=FileSystemLoader(self.template_path))
        self.template = self.env.get_template(self.template_name)
        self.ast = self.env.parse(self.template.render())
        self.variables = meta.find_undeclared_variables(self.ast)
        self.allowed_missing_variables = allowed_missing_variables or [
            "examples",
            "description",
            "output_format",
        ]
        self.default_variable_values = default_variable_values or {}

    def list_templates(self) -> List[str]:
        return self.env.list_templates()

    def update_template_variables(self, variables: Dict[str, Any]) -> None:
        self.default_variable_values.update(variables)

    def generate_prompt(self, variables: Dict[str, Any]) -> str:
        self.update_template_variables(variables)
        return self.template.render(variables)

    def get_template_variables(self) -> List[str]:
        return self.variables

    def get_template_ast(self) -> Dict[str, Any]:
        return self.ast

    def get_template_ast_as_json(self) -> str:
        return self.env.dump(self.ast)



    # def get_template_ast_as_yaml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=yaml.Dumper)

    # def get_template_ast_as_toml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=toml.Dumper)

    # def get_template_ast_as_xml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_html(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_csv(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_tsv(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_jsonl(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_yaml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_toml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_xml(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_html(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

    # def get_template_ast_as_csv(self) -> str:
    #     return self.env.dump(self.ast, Dumper=xmltodict.unparse)

