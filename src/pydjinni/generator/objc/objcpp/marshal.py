from pathlib import Path

from pydjinni.config.types import IdentifierStyle
from pydjinni.generator.marshal import Marshal
from pydjinni.parser.ast import Enum, Flags, Record, Interface, Parameter
from pydjinni.parser.base_models import BaseField, BaseType
from .config import ObjcppConfig
from .external_types import external_types
from .type import ObjcppExternalType, ObjcppType, ObjcppField


class ObjcppMarshal(Marshal[ObjcppConfig, ObjcppExternalType], types=external_types):
    def marshal_base_type(self, type_def: BaseType):
        namespace = self.config.namespace + [identifier.convert(IdentifierStyle.Case.pascal) for identifier in type_def.namespace]
        name = type_def.name.convert(IdentifierStyle.Case.pascal)
        translator = "::" + "::".join(namespace + [name])
        type_def.objcpp = ObjcppType(
            name=name,
            namespace="::".join(namespace),
            header=Path(f"{name}+Private.{self.config.header_extension}"),
            source=Path(f"{name}+Private.{self.config.source_extension}"),
            translator=translator
        )

    def marshal_base_field(self, field_def: BaseField):
        match field_def:
            case Enum.Item() | Flags.Flag():
                field_def.objcpp = ObjcppField(
                    name=field_def.name.convert(IdentifierStyle.Case.pascal)
                )
            case Record.Field() | Parameter():
                field_def.objcpp = ObjcppField(
                    name=field_def.name.convert(IdentifierStyle.Case.camel)
                )
            case Interface.Method():
                field_def.objcpp = ObjcppField(
                    name=field_def.name.convert(IdentifierStyle.Case.camel),
                )
