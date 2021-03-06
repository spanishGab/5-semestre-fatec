import zmq
from zmq import REP
from collections import namedtuple

from ..constants.constants import TYPE_ERROR_MESAGE, VALUE_ERROR_MESSAGE

ADDRESS_PATTERN = '{protocol}://{interface}:{port}'
DEFAULT_MESSAGE_SEPARATOR = ':'

SocketIteratorResult = namedtuple('SocketIteratorResult', ['name', 'content'])

SOCKET_NAME_RESTRICTION = ("'socket_name' must be equal to some of these " +
                           " values {}")

MESSAGE_STRUCTURE = (
    "{sender_name}" + DEFAULT_MESSAGE_SEPARATOR +
    "{message}" + DEFAULT_MESSAGE_SEPARATOR +
    "{recipient_name}" + DEFAULT_MESSAGE_SEPARATOR +
    "{recipient_protocol}" + DEFAULT_MESSAGE_SEPARATOR +
    "{recipient_interace}" + DEFAULT_MESSAGE_SEPARATOR +
    "{recipient_port}" + DEFAULT_MESSAGE_SEPARATOR
)


class BaseZeroMqSocketContextManager:

    def __init__(self, init_context: bool = True, **kwargs):
        self.create_sockets_context(kwargs.get('io_threads', 1))

        self.__sockets = {}
        self.__socket_names = []

    @property
    def sockets_context(self):
        return self.__sockets_context

    def create_sockets_context(self, io_threads: int = 1):
        self.__sockets_context = zmq.Context(io_threads)

    @property
    def sockets(self):
        return self.__sockets

    def add_socket_to_context(self, socket_name: str, socket_type: int = REP):
        if isinstance(socket_name, str):
            self.sockets[socket_name] = {
                    'socket': self.sockets_context.socket(socket_type)
                }
            self.__socket_names.append(socket_name)
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def remove_socket_from_context(self, socket_name: str):
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:
                self.sockets.pop(socket_name)
                self.__socket_names.remove(socket_name)
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def connect_socket_to_address(self,
                                  socket_name: str,
                                  address_protocol: str = 'tcp',
                                  address_interface: str = '127.0.0.1',
                                  address_port: int = 5555):
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:

                self.sockets[socket_name]['socket'].connect(
                    ADDRESS_PATTERN.format(protocol=address_protocol,
                                           interface=address_interface,
                                           port=address_port)
                )

                self.sockets[socket_name]['address'] = ADDRESS_PATTERN.format(
                    protocol=address_protocol,
                    interface=address_interface,
                    port=address_port
                )
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def disconnect_socket_from_address(self, socket_name: str):
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:
                self.sockets[socket_name]['socket'].disconnect(
                    self.sockets[socket_name]['address']
                )
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def bind_socket_to_address(self,
                               socket_name: str,
                               address_protocol: str = 'tcp',
                               address_interface: str = '127.0.0.1',
                               address_port: int = 5555):
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:

                self.sockets[socket_name]['socket'].bind(
                    ADDRESS_PATTERN.format(protocol=address_protocol,
                                           interface=address_interface,
                                           port=address_port)
                )

                self.sockets[socket_name]['address'] = ADDRESS_PATTERN.format(
                    protocol=address_protocol,
                    interface=address_interface,
                    port=address_port
                )

                self.__socket_names.append(socket_name)
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def unbind_socket_from_address(self, socket_name: str):
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:
                self.sockets[socket_name]['socket'].unbind(
                    self.sockets[socket_name]['address']
                )
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def receive_message(self, socket_name: str) -> list:
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:
                message = self.sockets[socket_name]['socket'].recv_string()
                message = message.split(DEFAULT_MESSAGE_SEPARATOR)

                return message
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def send_message(self,
                     socket_name: str,
                     message: str,
                     **kwargs) -> object:
        if isinstance(socket_name, str):
            if socket_name in self.__socket_names:
                result = self.sockets[socket_name]['socket'].send_string(
                    u=(
                        MESSAGE_STRUCTURE.format(
                            sender_name=kwargs.get('message_sender',
                                                   socket_name),
                            message=message,

                            recipient_name=(
                                kwargs.get('message_recipient_name',
                                           'contact')
                            ),

                            recipient_protocol=(
                                kwargs.get('message_recipient_protocol',
                                           'tcp')
                            ),

                            recipient_interace=(
                                kwargs.get('message_recipient_interace',
                                           '127.0.0.1')
                            ),
                            recipient_port=(
                                str(kwargs.get('message_recipient_port',
                                               5555))
                            )
                        )
                    )
                )

                return result
            else:
                raise ValueError(VALUE_ERROR_MESSAGE.format(
                    param='socket_name',
                    restr=(SOCKET_NAME_RESTRICTION
                           .format(self.__socket_names)))
                )
        else:
            raise TypeError(TYPE_ERROR_MESAGE.format(param='socket_name',
                                                     tp=str,
                                                     inst=type(socket_name)))

    def __iter__(self):
        self.__iter_counter = 0
        return self

    def __next__(self):
        if self.__iter_counter == len(self.__socket_names):
            raise StopIteration

        result = self.sockets[self.__socket_names[self.__iter_counter]]
        self.__iter_counter += 1

        return SocketIteratorResult(
            name=self.__socket_names[self.__iter_counter],
            content=result
        )
