# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ricky_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'ricky_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13ricky_service.proto\">\n\x15TestimonialSubmission\x12\x10\n\x08\x63ustomer\x18\x01 \x01(\t\x12\x13\n\x0btestimonial\x18\x02 \x01(\t\"\x1f\n\x0cGenericReply\x12\x0f\n\x07message\x18\x01 \x01(\t2L\n\x0cRickyService\x12<\n\x11SubmitTestimonial\x12\x16.TestimonialSubmission\x1a\r.GenericReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ricky_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TESTIMONIALSUBMISSION']._serialized_start=23
  _globals['_TESTIMONIALSUBMISSION']._serialized_end=85
  _globals['_GENERICREPLY']._serialized_start=87
  _globals['_GENERICREPLY']._serialized_end=118
  _globals['_RICKYSERVICE']._serialized_start=120
  _globals['_RICKYSERVICE']._serialized_end=196
# @@protoc_insertion_point(module_scope)
