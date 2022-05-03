# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: audio.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61udio.proto\x12\x05\x61udio\"\x93\x01\n\x0b\x41udioObject\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nchannel_id\x18\x02 \x01(\x05\x12\r\n\x05title\x18\x03 \x01(\t\x12\x0e\n\x06status\x18\x04 \x01(\t\x12\x10\n\x08\x64uration\x18\x05 \x01(\t\x12\x0b\n\x03url\x18\x06 \x01(\t\x12\x12\n\nupdated_at\x18\x07 \x01(\t\x12\x12\n\ncreated_at\x18\x08 \x01(\t\"b\n\x0eNewAudioObject\x12\r\n\x05title\x18\x01 \x01(\t\x12\x12\n\nchannel_id\x18\x02 \x01(\x05\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x10\n\x08\x64uration\x18\x04 \x01(\t\x12\x0b\n\x03url\x18\x05 \x01(\t\"E\n\x12\x43reateAudioRequest\x12/\n\x10new_audio_object\x18\x01 \x01(\x0b\x32\x15.audio.NewAudioObject\"\x1e\n\x10ReadAudioRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"(\n\x17ReadAudioByTitleRequest\x12\r\n\x05title\x18\x01 \x01(\t\"Q\n\x12UpdateAudioRequest\x12\n\n\x02id\x18\x01 \x01(\x05\x12/\n\x10new_audio_object\x18\x02 \x01(\x0b\x32\x15.audio.NewAudioObject\" \n\x12\x44\x65leteAudioRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x16\n\x14ReadAudioListRequest\"\"\n\x13\x43reateAudioResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t\"J\n\x11ReadAudioResponse\x12(\n\x0c\x61udio_object\x18\x01 \x01(\x0b\x32\x12.audio.AudioObject\x12\x0b\n\x03msg\x18\x02 \x01(\t\"\"\n\x13UpdateAudioResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\"\n\x13\x44\x65leteAudioResponse\x12\x0b\n\x03msg\x18\x01 \x01(\t\"O\n\x15ReadAudioListResponse\x12)\n\raudio_objects\x18\x01 \x03(\x0b\x32\x12.audio.AudioObject\x12\x0b\n\x03msg\x18\x02 \x01(\t2\xef\x02\n\x05\x41udio\x12\x46\n\x0b\x43reateAudio\x12\x19.audio.CreateAudioRequest\x1a\x1a.audio.CreateAudioResponse\"\x00\x12@\n\tReadAudio\x12\x17.audio.ReadAudioRequest\x1a\x18.audio.ReadAudioResponse\"\x00\x12\x46\n\x0bUpdateAudio\x12\x19.audio.UpdateAudioRequest\x1a\x1a.audio.UpdateAudioResponse\"\x00\x12\x46\n\x0b\x44\x65leteAudio\x12\x19.audio.DeleteAudioRequest\x1a\x1a.audio.DeleteAudioResponse\"\x00\x12L\n\rReadAudioList\x12\x1b.audio.ReadAudioListRequest\x1a\x1c.audio.ReadAudioListResponse\"\x00\x62\x06proto3')



_AUDIOOBJECT = DESCRIPTOR.message_types_by_name['AudioObject']
_NEWAUDIOOBJECT = DESCRIPTOR.message_types_by_name['NewAudioObject']
_CREATEAUDIOREQUEST = DESCRIPTOR.message_types_by_name['CreateAudioRequest']
_READAUDIOREQUEST = DESCRIPTOR.message_types_by_name['ReadAudioRequest']
_READAUDIOBYTITLEREQUEST = DESCRIPTOR.message_types_by_name['ReadAudioByTitleRequest']
_UPDATEAUDIOREQUEST = DESCRIPTOR.message_types_by_name['UpdateAudioRequest']
_DELETEAUDIOREQUEST = DESCRIPTOR.message_types_by_name['DeleteAudioRequest']
_READAUDIOLISTREQUEST = DESCRIPTOR.message_types_by_name['ReadAudioListRequest']
_CREATEAUDIORESPONSE = DESCRIPTOR.message_types_by_name['CreateAudioResponse']
_READAUDIORESPONSE = DESCRIPTOR.message_types_by_name['ReadAudioResponse']
_UPDATEAUDIORESPONSE = DESCRIPTOR.message_types_by_name['UpdateAudioResponse']
_DELETEAUDIORESPONSE = DESCRIPTOR.message_types_by_name['DeleteAudioResponse']
_READAUDIOLISTRESPONSE = DESCRIPTOR.message_types_by_name['ReadAudioListResponse']
AudioObject = _reflection.GeneratedProtocolMessageType('AudioObject', (_message.Message,), {
  'DESCRIPTOR' : _AUDIOOBJECT,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.AudioObject)
  })
_sym_db.RegisterMessage(AudioObject)

NewAudioObject = _reflection.GeneratedProtocolMessageType('NewAudioObject', (_message.Message,), {
  'DESCRIPTOR' : _NEWAUDIOOBJECT,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.NewAudioObject)
  })
_sym_db.RegisterMessage(NewAudioObject)

CreateAudioRequest = _reflection.GeneratedProtocolMessageType('CreateAudioRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEAUDIOREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.CreateAudioRequest)
  })
_sym_db.RegisterMessage(CreateAudioRequest)

ReadAudioRequest = _reflection.GeneratedProtocolMessageType('ReadAudioRequest', (_message.Message,), {
  'DESCRIPTOR' : _READAUDIOREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.ReadAudioRequest)
  })
_sym_db.RegisterMessage(ReadAudioRequest)

ReadAudioByTitleRequest = _reflection.GeneratedProtocolMessageType('ReadAudioByTitleRequest', (_message.Message,), {
  'DESCRIPTOR' : _READAUDIOBYTITLEREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.ReadAudioByTitleRequest)
  })
_sym_db.RegisterMessage(ReadAudioByTitleRequest)

UpdateAudioRequest = _reflection.GeneratedProtocolMessageType('UpdateAudioRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUDIOREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.UpdateAudioRequest)
  })
_sym_db.RegisterMessage(UpdateAudioRequest)

DeleteAudioRequest = _reflection.GeneratedProtocolMessageType('DeleteAudioRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEAUDIOREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.DeleteAudioRequest)
  })
_sym_db.RegisterMessage(DeleteAudioRequest)

ReadAudioListRequest = _reflection.GeneratedProtocolMessageType('ReadAudioListRequest', (_message.Message,), {
  'DESCRIPTOR' : _READAUDIOLISTREQUEST,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.ReadAudioListRequest)
  })
_sym_db.RegisterMessage(ReadAudioListRequest)

CreateAudioResponse = _reflection.GeneratedProtocolMessageType('CreateAudioResponse', (_message.Message,), {
  'DESCRIPTOR' : _CREATEAUDIORESPONSE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.CreateAudioResponse)
  })
_sym_db.RegisterMessage(CreateAudioResponse)

ReadAudioResponse = _reflection.GeneratedProtocolMessageType('ReadAudioResponse', (_message.Message,), {
  'DESCRIPTOR' : _READAUDIORESPONSE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.ReadAudioResponse)
  })
_sym_db.RegisterMessage(ReadAudioResponse)

UpdateAudioResponse = _reflection.GeneratedProtocolMessageType('UpdateAudioResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEAUDIORESPONSE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.UpdateAudioResponse)
  })
_sym_db.RegisterMessage(UpdateAudioResponse)

DeleteAudioResponse = _reflection.GeneratedProtocolMessageType('DeleteAudioResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEAUDIORESPONSE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.DeleteAudioResponse)
  })
_sym_db.RegisterMessage(DeleteAudioResponse)

ReadAudioListResponse = _reflection.GeneratedProtocolMessageType('ReadAudioListResponse', (_message.Message,), {
  'DESCRIPTOR' : _READAUDIOLISTRESPONSE,
  '__module__' : 'audio_pb2'
  # @@protoc_insertion_point(class_scope:audio.ReadAudioListResponse)
  })
_sym_db.RegisterMessage(ReadAudioListResponse)

_AUDIO = DESCRIPTOR.services_by_name['Audio']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AUDIOOBJECT._serialized_start=23
  _AUDIOOBJECT._serialized_end=170
  _NEWAUDIOOBJECT._serialized_start=172
  _NEWAUDIOOBJECT._serialized_end=270
  _CREATEAUDIOREQUEST._serialized_start=272
  _CREATEAUDIOREQUEST._serialized_end=341
  _READAUDIOREQUEST._serialized_start=343
  _READAUDIOREQUEST._serialized_end=373
  _READAUDIOBYTITLEREQUEST._serialized_start=375
  _READAUDIOBYTITLEREQUEST._serialized_end=415
  _UPDATEAUDIOREQUEST._serialized_start=417
  _UPDATEAUDIOREQUEST._serialized_end=498
  _DELETEAUDIOREQUEST._serialized_start=500
  _DELETEAUDIOREQUEST._serialized_end=532
  _READAUDIOLISTREQUEST._serialized_start=534
  _READAUDIOLISTREQUEST._serialized_end=556
  _CREATEAUDIORESPONSE._serialized_start=558
  _CREATEAUDIORESPONSE._serialized_end=592
  _READAUDIORESPONSE._serialized_start=594
  _READAUDIORESPONSE._serialized_end=668
  _UPDATEAUDIORESPONSE._serialized_start=670
  _UPDATEAUDIORESPONSE._serialized_end=704
  _DELETEAUDIORESPONSE._serialized_start=706
  _DELETEAUDIORESPONSE._serialized_end=740
  _READAUDIOLISTRESPONSE._serialized_start=742
  _READAUDIOLISTRESPONSE._serialized_end=821
  _AUDIO._serialized_start=824
  _AUDIO._serialized_end=1191
# @@protoc_insertion_point(module_scope)
