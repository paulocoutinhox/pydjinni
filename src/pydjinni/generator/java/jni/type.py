from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field


class NativeType(str, Enum):
    object = 'jobject'
    string = 'jstring'
    boolean = 'jboolean'
    byte = 'jbyte'
    char = 'jchar'
    short = 'jshort'
    int = 'jint'
    long = 'jlong'
    float = 'jfloat'
    double = 'jdouble'


class JniExternalType(BaseModel):
    translator: str = Field(
        pattern=r"^(::)?([a-zA-Z][a-zA-Z0-9_]*(::))*[a-zA-Z][a-zA-Z0-9_]*$"
    )
    header: Path
    typename: NativeType = Field(
        default=NativeType.object,
        description="The Java native [`jvalue` union type](https://docs.oracle.com/en/java/javase/17/docs/specs/jni/types.html#the-value-type) as represented in JNI."
    )
    type_signature: str = Field(
        examples=["(ILjava/lang/String;[I)J"],
        description="[Java VM Type Signatures](https://docs.oracle.com/en/java/javase/17/docs/specs/jni/types.html#type-signatures)"
    )


class JniType(JniExternalType):
    name: str
    jni_prefix: str = None
    source: Path
    namespace: str


class JniField(BaseModel):
    name: str
    jni_name: str = None
    type_signature: str = None
    routine_name: str = None
    field_accessor: str = None
