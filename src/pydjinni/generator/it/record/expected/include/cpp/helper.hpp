// AUTOGENERATED FILE - DO NOT MODIFY!
// This file was generated by PyDjinni from 'record.djinni'
#pragma once
#include <memory>
#include "primitive_types.hpp"
#include "collection_types.hpp"
#include "optional_types.hpp"
#include "binary_types.hpp"
#include "base_record.hpp"

namespace test::record {
class Helper {
public:
    static ::test::record::PrimitiveTypes get_primitive_types(const ::test::record::PrimitiveTypes & record_type);
    static ::test::record::CollectionTypes get_collection_types(const ::test::record::CollectionTypes & record_type);
    static ::test::record::OptionalTypes get_optional_types(const ::test::record::OptionalTypes & record_type);
    static ::test::record::BinaryTypes get_binary_types(const ::test::record::BinaryTypes & record_type);
    static ::test::record::BaseRecord get_cpp_base_record();
    static ::test::record::BaseRecord get_host_base_record(const ::test::record::BaseRecord & record_type);
};
}  // namespace test::record
