from dataclasses import dataclass
from pathlib import Path

import pydantic
import yaml

from pydjinni.exceptions import InputParsingException, FileNotFoundException
from pydjinni.parser.ast import TypeReference, BaseType
from pydjinni.parser.base_models import BaseExternalType


class Resolver:
    @dataclass
    class TypeResolvingException(Exception):
        """Exception raised when the required pydjinni type cannot be found"""
        type_reference: TypeReference
        position: int

    @dataclass
    class DuplicateTypeException(Exception):
        """Exception raised when the given pydjinni type is already defined"""
        datatype: BaseType
        position: int

    def __init__(self, external_types_model: type[BaseExternalType]):
        self.registry = dict()
        self._external_types_model = external_types_model

    def load_external(self, path: Path):
        try:
            types_dict = yaml.safe_load_all(path.read_text())
            for type_dict in types_dict:
                if type_dict is not None:
                    types_type = self._external_types_model.model_validate(type_dict)
                    self.register_external(types_type)
        except (pydantic.ValidationError, yaml.YAMLError) as e:
            raise InputParsingException(f"invalid external type {e}", file=path)
        except FileNotFoundError:
            raise FileNotFoundException(path)

    def register(self, datatype: BaseType):
        registry_name = ".".join(datatype.namespace + [datatype.name])
        if registry_name in self.registry:
            raise Resolver.DuplicateTypeException(
                datatype=datatype,
                position=datatype.position
            )
        else:
            self.registry[registry_name] = datatype

    def register_external(self, type_definition: BaseExternalType):
        registry_name = f"{type_definition.namespace}.{type_definition.name}" if type_definition.namespace else type_definition.name
        self.registry[registry_name] = type_definition

    def resolve(self, type_reference: TypeReference):
        type_reference.type_def = self.registry.get(type_reference.name)
        if type_reference.type_def is None:
            raise Resolver.TypeResolvingException(type_reference=type_reference, position=type_reference.position)
