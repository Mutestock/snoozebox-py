#!/bin/bash

# Cleanup
echo removing older protogen...
rm -rf ./audio_archiver/protogen
mkdir ./audio_archiver/protogen

# Protogen
echo generating protogen...
python -m grpc_tools.protoc -I./proto --python_out=./audio_archiver/protogen --grpc_python_out=./audio_archiver/protogen ./proto/audio.proto
python -m grpc_tools.protoc -I./proto --python_out=./audio_archiver/protogen --grpc_python_out=./audio_archiver/protogen ./proto/channel.proto

echo changing some imports...
sed -i 's/import audio_pb2 as audio__pb2/import protogen.audio_pb2 as audio__pb2/g' ./audio_archiver/protogen/audio_pb2_grpc.py
sed -i 's/import channel_pb2 as channel__pb2/import protogen.channel_pb2 as channel__pb2/g' ./audio_archiver/protogen/channel_pb2_grpc.py


echo Ok