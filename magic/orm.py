# -*- coding: utf-8 -*-


class Field(object):

    def __init__(self, name, valume):
        self.name = name
        self.valume = valume

    def __str__(self, field):
        print(self.__class__.__name__, self.field)
        return '<%s:%s>' % (self.__class__.__name__, self.field)


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, "varchar(100)")


class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, "bigint")


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":
            return type.__new__(cls, name, bases, attrs)
        print("Found Model %s" % name)
        mapping = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                mapping[k] = v
        for k in mapping.keys():
            attrs.pop(k)
        attrs["__mapping__"] = mapping
        # 假设表名是类名
        attrs["__name__"] = name
        return type.__new__(cls, name, bases, attrs)


class Model(dict):
    __metaclass__ = ModelMetaClass

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Model object has no attribute %s", key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mapping__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = "insert into %s (%s) values (%s)" % (self.__table__, ','.join(fields), ','.join(params))
        print(sql)
        print(str(args))


class User(Model):
    __table__ = "user"

    id = IntegerField("id")
    name = StringField("name")


user = User(id=1, name="test12312313123123123123")
user.save()
