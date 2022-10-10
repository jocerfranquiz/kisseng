# definition of an infix operator class
# this recipe also works in jython
# calling sequence for the infix is either:
#  x |op| y
# or:
# x <<op>> y
# where op is the operator
# This is based on https://code.activestate.com/recipes/384122/

class infix:
    def __init__(self, _function):
        self.f = _function

    def __ror__(self, other):
        return LeftBind(self.f, other)

    def __or__(self, other):
        return RightBind(self.f, other)

    def __rlshift__(self, other):
        return LeftBind(self.f, other)

    def __rshift__(self, other):
        return RightBind(self.f, other)

    def __call__(self, value1, value2):
        return self.f(value1, value2)

    @staticmethod
    def infix(_function):
        return infix(_function)


class LeftBind:
    def __init__(self, function, bind):
        self.f = function
        self.b = bind

    def __or__(self, other):
        return self.f(self.b, other)

    def __rshift__(self, other):
        return self.f(self.b, other)

    def __call__(self, other):
        return self.f(self.b, other)


class RightBind:
    def __init__(self, function, bind):
        self.f = function
        self.b = bind

    def __ror__(self, other):
        return self.f(other, self.b)

    def __rlshift__(self, other):
        return self.f(other, self.b)

    def __call__(self, other):
        return self.f(other, self.b)


# Examples

# simple multiplication
x = infix(lambda x, y: x * y)
print(2 | x | 4)
# => 8

# class checking
isa = infix(lambda x, y: x.__class__ == y.__class__)
print([1, 2, 3] | isa | [])
print([1, 2, 3] << isa >> [])
# => True

# inclusion checking
is_in = infix(lambda x, y: x in y.keys())
print(1 | is_in | {1: 'one'})
print(1 << is_in >> {1: 'one'})
# => True

# an infix div operator
import operator

div = infix(operator.truediv)
print(10 | div | (4 | div | 2))
# => 5.0
print(8 | div | (2 | div | 2))


# functional programming (not working in jython, use the "curry" recipe! )
def curry(f, x):
    def curried_function(*args, **kw):
        return f(*((x,) + args), **kw)

    return curried_function


curry = infix(curry)

add5 = operator.add | curry | 5
print(add5(6))
# => 11

f = infix(lambda x, y: x * y)
g = 3 | f
print(g | 4)
g = f | 3
print(4 | g)

f = infix(lambda x, y: x * y)
g = 5 << f
print(g >> 4)
g = f >> 5
print(4 << g)


@infix
def x(x, y):
    return x * y


@infix
def isa(x, y):
    return x.__class__ == y.__class__


print(x(3, 7))
print(3 | x | 7)
print(3 << x >> 7)


