from abc import ABC
from typing import Any


class IntegerRange:
    def __init__(self,
                 min_amount: int,
                 max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: Any, name: str) -> Any:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, value: Any) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Grade should be integer")
        if self.min_amount > value or value > self.max_amount:
            raise ValueError("Grade should not be less than "
                             "2 and greater than 12")
        setattr(instance, self.protected_name, value)


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):

    def __init__(self,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(4, 14)
    height = IntegerRange(80, 120)
    weight = IntegerRange(20, 50)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    age = IntegerRange(14, 60)
    height = IntegerRange(120, 220)
    weight = IntegerRange(50, 120)

    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)


class Slide:
    def __init__(self,
                 name: str,
                 limitation_class:
                 ChildrenSlideLimitationValidator
                 or AdultSlideLimitationValidator) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except (TypeError, ValueError):
            return False
