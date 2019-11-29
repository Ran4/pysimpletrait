from typing import Dict
import random

from traits import Serializable, Savable, add_trait_impls

class Sub(Serializable, Savable):
    def __init__(self, value):
        self.id = random.randint(0, 1000)
        self.value = value

class Sub2(Serializable):
    def __init__(self, value):
        self.id = random.randint(0, 1000)
        self.value = value


def serialize_sub(x: Sub, squared: bool = False) -> Dict:
    return {
        "value": x.value ** 2 if squared else x.value,
    }


def save_sub(x: Sub):
    print(f"Saved sub {x.serialize()}")
    return x.id


Sub.implement(Savable, save_sub)
Sub.implement(Serializable, lambda sub: {"value": sub.value})

if __name__ == "__main__":
    print(Sub(43).serialize())

    print(Sub(44).save())
    print(Savable.save(Sub(45)))
