# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service_file.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12service_file.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x15\n\x04Uuid\x12\r\n\x05value\x18\x01 \x01(\t\"\"\n\x0bStatRequest\x12\x13\n\x04uuid\x18\x01 \x01(\x0b\x32\x05.Uuid\"\x95\x01\n\tStatReply\x12\x1d\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x0f.StatReply.Data\x1ai\n\x04\x44\x61ta\x12\x33\n\x0f\x63reate_datetime\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04size\x18\x02 \x01(\x04\x12\x10\n\x08mimetype\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\"0\n\x0bReadRequest\x12\x13\n\x04uuid\x18\x01 \x01(\x0b\x32\x05.Uuid\x12\x0c\n\x04size\x18\x02 \x01(\x04\"@\n\tReadReply\x12\x1d\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x0f.ReadReply.Data\x1a\x14\n\x04\x44\x61ta\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32P\n\x04\x46ile\x12\"\n\x04stat\x12\x0c.StatRequest\x1a\n.StatReply\"\x00\x12$\n\x04read\x12\x0c.ReadRequest\x1a\n.ReadReply\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_file_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_UUID']._serialized_start=55
  _globals['_UUID']._serialized_end=76
  _globals['_STATREQUEST']._serialized_start=78
  _globals['_STATREQUEST']._serialized_end=112
  _globals['_STATREPLY']._serialized_start=115
  _globals['_STATREPLY']._serialized_end=264
  _globals['_STATREPLY_DATA']._serialized_start=159
  _globals['_STATREPLY_DATA']._serialized_end=264
  _globals['_READREQUEST']._serialized_start=266
  _globals['_READREQUEST']._serialized_end=314
  _globals['_READREPLY']._serialized_start=316
  _globals['_READREPLY']._serialized_end=380
  _globals['_READREPLY_DATA']._serialized_start=360
  _globals['_READREPLY_DATA']._serialized_end=380
  _globals['_FILE']._serialized_start=382
  _globals['_FILE']._serialized_end=462
# @@protoc_insertion_point(module_scope)
