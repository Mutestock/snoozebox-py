#!/bin/bash

echo "cleaning up..."
rm -rf proto

echo "copying updated proto files..."
cp -r ../../proto proto

echo "generating gRPC..."
proto_dir=proto
for entry in "$proto_dir"/*
do
    proto_name="$(basename $entry)"
    proto_name="${proto_name%.*}"
    echo "found ${proto_name}..."
    python -m grpc_tools.protoc -I./proto --python_out=./test_grpc/protogen --grpc_python_out=./test_grpc/protogen $entry
    sed -i "s/import ${proto_name}_pb2 as ${proto_name}__pb2/import protogen.${proto_name}_pb2 as ${proto_name}__pb2/g" "./test_grpc/protogen/${proto_name}_pb2_grpc.py"
done

export AUDIO_ARCHIVER_TESTING=1

echo "running nose..."
nose2 -v
echo "done"