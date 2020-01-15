class BaseException(Exception):
    pass


class RequestFailedError(BaseException):
    def __init__(self, status: int = None):
        self.reason = \
            ("Request cainiao API was failed,"
             " response status code is {}").format(status)
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class NoMobileOrPhone(BaseException):
    def __init__(self):
        self.reason = "At least one Phone or Mobile"
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class TradeOrderListError(BaseException):
    def __init__(self):
        self.reason = \
            ("The list length must greater than 0 "
             "and less than or equal 100")
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class ItemSetError(BaseException):
    def __init__(self):
        self.reason = ("The item count must greater than 0,"
                       "and name is not set None or ''")
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class ItemsNoneError(BaseException):
    def __init__(self):
        self.reason = "The items is not set None or []"
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class ItemsLimitError(BaseException):
    def __init__(self):
        self.reason = "The items length must less than or equal 100"
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class TradeOrderInfoError(BaseException):
    def __init__(self):
        self.reason = "The recipients length must less than or equal 10"
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason


class CloudPrintConnectError(BaseException):
    def __init__(self, e):
        self.reason = "The websocket connect failed, {}".format(e)
        super(BaseException, self).__init__(self, self.reason)

    def __str__(self):
        return self.reason
