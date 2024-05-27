import datetime
from typing import Optional, Union

import grpc

import clients.service_file_pb2 as service_file_pb2
import clients.service_file_pb2_grpc as service_file_pb2_grpc


def _get_dict_from_stat_response(response: service_file_pb2.StatReply) -> dict[str, Union[str, int]]:
    """Transforms 'create_datetime' response attribute into an ISO format string and returns it with other response data as a dict.

    Args:
        response: gRPC response

    Returns:
        human-readable StatReply data as a dict
    """
    data = response.data
    return {'create_datetime': datetime.datetime.fromtimestamp(data.create_datetime.seconds + data.create_datetime.nanos * 1e-9).isoformat(),
            'size': data.size,
            'mimetype': data.mimetype,
            'name': data.name}


class GrpcClient:
    STAT_TIMEOUT = 5
    READ_TIMEOUT = 10

    def __init__(self, grpc_server_address: str, cert_file_path: Optional[str] = None):
        self.server_address = grpc_server_address
        if cert_file_path:
            with open(cert_file_path, 'rb') as f:
                certificates = f.read()
            self.channel_credentials = grpc.ssl_channel_credentials(root_certificates=certificates)
        else:
            self.channel_credentials = None

    def _get_channel(self) -> grpc.Channel:
        if self.channel_credentials:
            return grpc.secure_channel(self.server_address, self.channel_credentials)
        else:
            return grpc.insecure_channel(self.server_address)

    def stat(self, uuid: str) -> dict[str, Union[str, int]]:
        """Requests file metadata.

        Args:
            uuid: unique file identifier

        Returns:
            file metadata as dict

        Raises:
            grpc.RpcError
        """
        with self._get_channel() as channel:
            stub = service_file_pb2_grpc.FileStub(channel)
            request = service_file_pb2.StatRequest(uuid=service_file_pb2.Uuid(value=uuid))
            response = stub.stat(request, timeout=self.STAT_TIMEOUT)
            return _get_dict_from_stat_response(response)

    def read(self, uuid: str) -> bytes:
        """Requests file content.

        Args:
            uuid: unique file identifier

        Returns:
            file content

        Raises:
            grpc.RpcError
        """
        with self._get_channel() as channel:
            stub = service_file_pb2_grpc.FileStub(channel)
            request = service_file_pb2.ReadRequest(uuid=service_file_pb2.Uuid(value=uuid))
            response = stub.read(request, timeout=self.READ_TIMEOUT)
            messages = list(response)
            return b''.join(msg.data.data for msg in messages)
