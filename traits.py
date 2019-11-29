from typing import Dict, Callable

TraitName = str
trait_impls: Dict[TraitName, Dict["Serializable", Callable]] = {}


def add_trait_impl(trait_klass, klass, impl) -> None:
    if trait_klass not in trait_impls:
        trait_impls[trait_klass] = {}
    trait_impls[trait_klass][klass] = impl


def add_trait_impls(trait_klass, klasses_and_serializers: Dict) -> None:
    for klass, impl in klasses_and_serializers.items():
        add_trait_impl(trait_klass, klass, impl)


class Trait:
    def call_impl(self, trait_klass, value, *args, **kwargs):
        if type(value) not in trait_impls[trait_klass]:
            raise Exception(
                f"Missing serialization function for {value.__class__}."
                "\nFound these serializers:\n" +
                "\n".join(f"    * {serializable.__name__} ({serializable})"
                          for serializable in trait_impls[trait_klass].keys()))

        impl = trait_impls[trait_klass][type(value)]
        return impl(value, *args, **kwargs)

    @classmethod
    def implement(cls, trait_klass, impl) -> None:
        add_trait_impl(trait_klass, cls, impl)


class Serializable(Trait):
    def serialize(self, *args, **kwargs):
        return self.call_impl(Serializable, self, *args, **kwargs)


class Savable(Trait):
    def save(self, *args, **kwargs):
        return self.call_impl(Savable, self, *args, **kwargs)
