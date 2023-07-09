from django.utils.deconstruct import deconstructible


@deconstructible
class EnumType(object):
    @classmethod
    def choices(cls):
        attrs = [i for i in cls.__dict__.keys() if i[:1] != "_" and i.isupper()]
        return tuple((cls.__dict__[attr], cls.__dict__[attr]) for attr in sorted(attrs))

    @classmethod
    def choices_flat(cls):
        attrs = [i for i in cls.__dict__.keys() if i[:1] != "_" and i.isupper()]
        return tuple(cls.__dict__[attr] for attr in sorted(attrs))

    def __eq__(self, other):
        return set(self.choices()) == set(other.choices())
