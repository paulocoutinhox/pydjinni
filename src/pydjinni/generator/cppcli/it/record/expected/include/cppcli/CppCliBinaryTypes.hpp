// AUTOGENERATED FILE - DO NOT MODIFY!
// This file was generated by PyDjinni from 'record.djinni'
#pragma once
#include "binary_types.hpp"

namespace Test::Record::CppCli {
[System::Serializable]
public ref class BinaryTypes sealed  {
public:
    BinaryTypes(array<System::Byte>^ binaryT, array<System::Byte>^ binaryOptional);

    property array<System::Byte>^ BinaryT
    {
        array<System::Byte>^ get();
    }
    property array<System::Byte>^ BinaryOptional
    {
        array<System::Byte>^ get();
    }
internal:
    using CppType = ::test::record::BinaryTypes;
    using CsType = BinaryTypes^;

    static CppType ToCpp(CsType cs);
    static CsType FromCpp(const CppType& cpp);
private:
    array<System::Byte>^ _binaryT;
    array<System::Byte>^ _binaryOptional;
};
}  // namespace Test::Record::CppCli
