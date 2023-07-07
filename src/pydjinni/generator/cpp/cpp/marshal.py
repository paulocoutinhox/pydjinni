from pathlib import Path

import mistletoe

from pydjinni.generator.marshal import Marshal
from pydjinni.parser.ast import Interface, Record, Enum, Flags, Parameter, Function
from pydjinni.parser.base_models import BaseType, BaseField, Constant, BaseExternalType, TypeReference
from .comment_renderer import DoxygenCommentRenderer
from .config import CppConfig
from .external_types import external_types
from .type import CppExternalType, CppType, CppField


class CppMarshal(Marshal[CppConfig, CppExternalType], types=external_types):

    def _type_specifier(self, type_ref: TypeReference):
        output = type_ref.type_def.cpp.typename if type_ref else "void"
        if type_ref:
            if type_ref.parameters:
                parameter_output = ""
                for parameter in type_ref.parameters:
                    if parameter_output:
                        parameter_output += ", "
                    parameter_output += self._type_specifier(parameter)
                output += f"<{parameter_output}>"
            if (isinstance(type_ref.type_def, BaseExternalType) and type_ref.type_def.primitive == BaseExternalType.Primitive.interface) or \
                    isinstance(type_ref.type_def, Interface):
                output = f"std::shared_ptr<{output}>"
            elif type_ref.optional:
                output = f"std::optional<{output}>"
        return output

    def _parameter_type_specifier(self, type_ref: TypeReference):
        type_spec = self._type_specifier(type_ref)
        return type_spec if type_ref.type_def.cpp.by_value else f"const {type_spec} &"

    def marshal_base_type(self, type_def: BaseType):
        namespace = self.config.namespace + [identifier.convert(self.config.identifier.namespace) for identifier in type_def.namespace]
        name = type_def.name.convert(self.config.identifier.type)

        type_def.cpp = CppType(
            name=name,
            typename=f"::{'::'.join(namespace + [name])}",
            comment=mistletoe.markdown(type_def.comment, DoxygenCommentRenderer) if type_def.comment else '',
            header=Path(f"{type_def.name.convert(self.config.identifier.file)}.{self.config.header_extension}"),
            source=Path(f"{type_def.name.convert(self.config.identifier.file)}.{self.config.source_extension}"),
            namespace="::".join(namespace),
            proxy=isinstance(type_def, Interface) and self.key in type_def.targets,
            by_value=type(type_def) not in [Interface, Record]
        )

    def marshal_function(self, type_def: Function):
        pass

    def second_function(self, type_def: Function):
        type_def.cpp = CppType(
            typename=f"std::function<{self._type_specifier(type_def.return_type_ref)}"
                     f"({','.join([self._type_specifier(parameter.type_ref) for parameter in type_def.parameters])})>",
            comment=mistletoe.markdown(type_def.comment, DoxygenCommentRenderer) if type_def.comment else '',
        )

    def marshal_base_field(self, field_def: BaseField):
        comment = mistletoe.markdown(field_def.comment, DoxygenCommentRenderer) if field_def.comment else ''
        match field_def:
            case Enum.Item() | Flags.Flag():
                style = self.config.identifier.enum
                type_spec = None
            case Record.Field():
                style = self.config.identifier.field
                type_spec = self._type_specifier(field_def.type_ref)
            case Parameter():
                style = self.config.identifier.field
                type_spec = self._parameter_type_specifier(field_def.type_ref)
            case Constant():
                style = self.config.identifier.const
                type_spec = None
            case Interface.Method():
                style = self.config.identifier.method
                type_spec = self._type_specifier(field_def.return_type_ref)
            case _:
                AssertionError("unsupported")

        field_def.cpp = CppField(
            name=field_def.name.convert(style),
            comment=comment,
            type_spec=type_spec
        )
