#!/usr/bin/env python

from ..exc import *
from collections import OrderedDict

class RPCRequest(object):
    unique_id = None
    """A unique ID to remember the request by. Protocol specific, may or
    may not be set. This value should only be set by
    :py:func:`~tinyrpc.RPCProtocol.create_request`.

    The ID allows client to receive responses out-of-order and still allocate
    them to the correct request.

    Only supported if the parent protocol has
    :py:attr:`~tinyrpc.RPCProtocol.supports_out_of_order` set to ``True``.
    """

    method = None
    """The name of the method to be called."""

    client = None
    nonce = None
    timestamp = None
    sig = None

    args = []
    """The positional arguments of the method call."""

    kwargs = OrderedDict()
    """The keyword arguments of the method call."""

    def error_respond(self, error):
        """Creates an error response.

        Create a response indicating that the request was parsed correctly,
        but an error has occured trying to fulfill it.

        :param error: An exception or a string describing the error.

        :return: A response or ``None`` to indicate that no error should be sent
                 out.
        """
        raise NotImplementedError()

    def respond(self, result):
        """Create a response.

        Call this to return the result of a successful method invocation.

        This creates and returns an instance of a protocol-specific subclass of
        :py:class:`~tinyrpc.RPCResponse`.

        :param result: Passed on to new response instance.

        :return: A response or ``None`` to indicate this request does not expect a
                 response.
        """
        raise NotImplementedError()

    def serialize(self):
        """Returns a serialization of the request.

        :return: A string to be passed on to a transport.
        """
        raise NotImplementedError()


class RPCResponse(object):
    """RPC call response class.

    Base class for all deriving responses.

    Has an attribute ``result`` containing the result of the RPC call, unless
    an error occured, in which case an attribute ``error`` will contain the
    error message."""

    unique_id = None

    def serialize(self):
        """Returns a serialization of the response.

        :return: A reply to be passed on to a transport.
        """
        raise NotImplementedError()


class RPCErrorResponse(RPCResponse):
    pass


class RPCProtocol(object):
    """Base class for all protocol implementations."""

    def create_request(self, method, args=None, kwargs=None, one_way=False):
        """Creates a new RPCRequest object.

        It is up to the implementing protocol whether or not ``args``,
        ``kwargs``, one of these, both at once or none of them are supported.

        :param method: The method name to invoke.
        :param args: The positional arguments to call the method with.
        :param kwargs: The keyword arguments to call the method with.
        :param one_way: The request is an update, i.e. it does not expect a
                        reply.
        :return: A new :py:class:`~tinyrpc.RPCRequest` instance.
        """
        raise NotImplementedError()

    def parse_request(self, data):
        """Parses a request given as a string and returns an
        :py:class:`RPCRequest` instance.

        :return: An instanced request.
        """
        raise NotImplementedError()

    def parse_reply(self, data):
        """Parses a reply and returns an :py:class:`RPCResponse` instance.

        :return: An instanced response.
        """
        raise NotImplementedError()


