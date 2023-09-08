from pathlib import Path

from pydjinni.generator.generator import Generator
from pydjinni.parser.ast import Enum, Flags, Record, Interface, Function
from pydjinni.parser.base_models import (
    BaseType,
    BaseField,
    SymbolicConstantField
)
from .config import JavaConfig
from .type import (
    JavaExternalType,
    JavaBaseType,
    JavaRecord,
    JavaFlags,
    JavaFunction,
    JavaBaseField,
    JavaSymbolicConstantField,
    JavaInterface
)
from .external_types import external_types


class JavaGenerator(Generator):
    key = "java"
    config_model = JavaConfig
    external_type_model = JavaExternalType
    external_types = external_types
    marshal_models = {
        BaseType: JavaBaseType,
        Record: JavaRecord,
        Record.Field: JavaRecord.JavaField,
        Flags: JavaFlags,
        Function: JavaFunction,
        BaseField: JavaBaseField,
        SymbolicConstantField: JavaSymbolicConstantField,
        Interface: JavaInterface,
        Interface.Method: JavaInterface.JavaMethod,
        Interface.Property: JavaInterface.JavaProperty
    }
    writes_source = True

    def generate_enum(self, type_def: Enum):
        self.write_source("enum.java.jinja2", type_def=type_def)

    def generate_flags(self, type_def: Flags):
        self.write_source("flags.java.jinja2", type_def=type_def)

    def generate_record(self, type_def: Record):
        self.write_source("record.java.jinja2", type_def=type_def)

    def generate_interface(self, type_def: Interface):
        self.write_source("interface.java.jinja2", type_def=type_def)

    def generate_function(self, type_def: Function):
        self.write_source("function.java.jinja2", type_def=type_def)

    def generate_loader(self):
        if self.config.native_lib:
            loader = f"{self.config.native_lib}Loader"
            package = '.'.join(self.config.package + ["native_lib"])
            package_path = Path("/".join(package.split(".")))
            self.write_source(
                template="loader.java.jinja2",
                filename=package_path / f"{loader}.java",
                loader=loader,
                package=package
            )

    def generate(self, ast: list[BaseType], copy_support_lib_sources: bool = True):
        super().generate(ast, copy_support_lib_sources)
        self.generate_loader()
