#!/bin/bash

# Cleanup
echo removing older protogen...
rm -rf ./audio_archiver/logic/protogen
mkdir ./audio_archiver/logic/protogen

# Protogen
echo generating protogen...
python -m grpc_tools.protoc -I./proto --python_out=./audio_archiver/logic/protogen --grpc_python_out=./audio_archiver/logic/protogen ./proto/audio.proto
python -m grpc_tools.protoc -I./proto --python_out=./audio_archiver/logic/protogen --grpc_python_out=./audio_archiver/logic/protogen ./proto/channel.proto

echo changing some imports...
sed -i 's/import audio_pb2 as audio__pb2/import logic.protogen.audio_pb2 as audio__pb2/g' ./audio_archiver/logic/protogen/audio_pb2_grpc.py
sed -i 's/import channel_pb2 as channel__pb2/import logic.protogen.channel_pb2 as channel__pb2/g' ./audio_archiver/logic/protogen/channel_pb2_grpc.py


echo Ok