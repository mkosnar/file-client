import datetime
import os
import unittest
from concurrent.futures import ThreadPoolExecutor

import grpc
from google.protobuf.timestamp_pb2 import Timestamp
from google.rpc import code_pb2, status_pb2
from grpc_status import rpc_status

from clients import service_file_pb2, service_file_pb2_grpc
from clients.grpc_client import GrpcClient


class NotFoundTestFileServicer(service_file_pb2_grpc.FileServicer):
    def stat(self, request, context):
        status = status_pb2.Status(code=code_pb2.NOT_FOUND, message='File not found.')
        context.abort_with_status(rpc_status.to_status(status))

    def read(self, request, context):
        status = status_pb2.Status(code=code_pb2.NOT_FOUND, message='File not found.')
        context.abort_with_status(rpc_status.to_status(status))


class FoundTestFileServicer(service_file_pb2_grpc.FileServicer):
    _test_stat_data = {'create_datetime': Timestamp(seconds=1000000, nanos=1000), 'size': 1, 'mimetype': 'mimetype', 'name': 'file'}
    result_stat_data = {**_test_stat_data,
                        'create_datetime': datetime.datetime.fromtimestamp(_test_stat_data['create_datetime'].seconds + _test_stat_data['create_datetime'].nanos * 1e-9).isoformat()}

    def __init__(self):
        super().__init__()
        self.result_read_data = list()

    def stat(self, request, context):
        return service_file_pb2.StatReply(data=service_file_pb2.StatReply.Data(**self._test_stat_data))

    def read(self, request, context):
        for _ in range(5):
            read_data = os.urandom(1024)
            self.result_read_data.append(read_data)
            yield service_file_pb2.ReadReply(data=service_file_pb2.ReadReply.Data(data=read_data))


class TestGrpcClientStat(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port('localhost:50051')
        self.server.start()

    def tearDown(self):
        self.server.stop(grace=None)

    def test_found(self):
        service_file_pb2_grpc.add_FileServicer_to_server(FoundTestFileServicer(), self.server)

        client = GrpcClient('localhost:50051')
        res = client.stat('uuid')
        self.assertDictEqual(res, FoundTestFileServicer.result_stat_data)

    def test_not_found(self):
        service_file_pb2_grpc.add_FileServicer_to_server(NotFoundTestFileServicer(), self.server)

        client = GrpcClient('localhost:50051')
        with self.assertRaises(grpc.RpcError) as rpce:
            client.stat('uuid')
        status = rpc_status.from_call(rpce.exception)
        self.assertEqual(status.code, code_pb2.NOT_FOUND)


class TestGrpcClientRead(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port('localhost:50051')
        self.server.start()

    def tearDown(self):
        self.server.stop(grace=None)

    def test_found(self):
        file_servicer = FoundTestFileServicer()
        service_file_pb2_grpc.add_FileServicer_to_server(file_servicer, self.server)

        client = GrpcClient('localhost:50051')
        res = client.read('uuid')
        self.assertEqual(res, b''.join(file_servicer.result_read_data))

    def test_not_found(self):
        service_file_pb2_grpc.add_FileServicer_to_server(NotFoundTestFileServicer(), self.server)

        client = GrpcClient('localhost:50051')
        with self.assertRaises(grpc.RpcError) as rpce:
            client.read('uuid')
        status = rpc_status.from_call(rpce.exception)
        self.assertEqual(status.code, code_pb2.NOT_FOUND)
