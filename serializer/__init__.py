#-*- coding:utf-8 -*-

import re
import datetime
import decimal
import base64
try:
    import ujson as json
except:
    import json

class Serializer:
    def __init__(self):
        self.__data__ = {}
        for k, v in self.__class__.__dict__.items():
            if not k.startswith('_'):
                self.__data__[k] = v

    def is_valid(self, data):
        self.error = ""
        self.data = {}
        for k, v in self.__data__.items():
            res, value = v.validate(k, data)
            if not res:
                self.error = value
                return False
            else:
                self.data[k] = value
        return True

class Field:
    reg = None
    def __init__(self, label="", required=False, 
                default=None, error_message="",
                min_length=0, max_length=0,
                min_value=0, max_value=0,
                choices=[], regexp=None,
                pattern="", max_digits = 0,
                decimal_places = 0):

        self.required = required
        self.default = default
        self.max_length = max_length
        self.min_length = min_length
        self.min_value = min_value
        self.max_value = max_value
        self.choices = choices
        self.error_message = error_message
        self.pattern = pattern
        self.max_digits = max_digits
        self.decimal_places = decimal_places

        if regexp:
            self.reg = re.compile(regexp)

    def validate(self, k, data):
        if self.required and k not in data:
            return False, "parameter %s is required" % k
        elif not self.required and data.get(k) is None:
            return True, self.default
        return self.run_validate(k, data.get(k))

class EmailFiled(Field):
    reg = re.compile("^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$")
    def run_validate(self, k, value):
        if self.reg.match(value):
            return True, value
        return False, self.error_message or "parameter %s not valid" % k

class IntegerField(Field):
    def run_validate(self, k, value):
        try:
            value = int(value)
            if self.min_value and value <= self.min_value or self.max_value and value >= self.max_value:
                raise
            return True, value
        except:
            return False, self.error_message or "parameter %s not valid" % k

class CharField(Field):
    def run_validate(self, k, value):
        if self.reg:
            if self.reg.match(value):
                return True, value
        else:
            l = len(value)
            if self.min_length and l >= self.min_length or self.max_length and l <= self.max_length:
                return True, value
        return False, self.error_message or "parameter %s not valid" % k

class ChoiceField(Field):
    def run_validate(self, k, value):
        if value in self.choices:
            return True, value
        return False, self.error_message or "parameter %s not valid" % k

class DateField(Field):
    pattern = "%Y-%m-%d"
    def run_validate(self, k, value):
        try:
            dt = datetime.datetime.strptime(value, self.pattern)
            return True, dt
        except:
            return False, self.error_message or "parameter %s not valid" % k

class DateTimeField(Field):
    pattern = "%Y-%m-%d %H:%M:%S"
    def run_validate(self, k, value):
        try:
            dt = datetime.datetime.strptime(value, self.pattern)
            return True, dt
        except:
            return False, self.error_message or "parameter %s not valid" % k

class DecimalField(Field):
    def run_validate(self, k, value):
        try:
            if len(value) > (self.max_digits + 1):
                raise
            if "." in value and len(value.split(".")[-1]) > self.decimal_places:
                raise
            return True, decimal.Decimal(value)
        except:
            return False, self.error_message or "parameter %s not valid" % k

class URLField(Field):
    reg = re.compile("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]")
    def run_validate(self, k, value):
        if self.reg.match(value):
            return True, value
        return False, self.error_message or "parameter %s not valid" % k

class Base64Field(Field):
    def run_validate(self, k, value):
        try:
            value = base64.b64decode(balue)
            return True, value
        except:
            return False, self.error_message or "parameter %s not valid" % k

class BooleanField(Field):
    def run_validate(self, k, value):
        if value in ("0", "false", "null"):
            return True, False
        return True, True

class JSONField(Field):
    def run_validate(self, k, value):
        try:
            value = json.loads(value)
            return True, value
        except:
            return False, self.error_message or "parameter %s not valid" % k
