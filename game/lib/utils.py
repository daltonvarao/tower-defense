import math


def assets_file(file):
    return f"./game/assets/{file}"


class Vector:
    def __init__(self, x=None, y=None, sprite=None):
        allowed_types = (int, float)
        if (isinstance(x, allowed_types) and isinstance(y, allowed_types)): 
            self.x = x
            self.y = y
        elif sprite:
            self.x = sprite.rect.centerx
            self.y = sprite.rect.centery
        else:
            raise Exception('Expected coords or Sprite instance')
    
    def distance_to(self, vector):
        return (vector - self).magnitude()

    def magnitude(self):
        return math.sqrt((self.x)**2 + (self.y)**2)

    def normalize(self):
        try:
            return self / self.magnitude()
        except ZeroDivisionError:
            return self / (self.magnitude() + 0.00000001)

    def direction_to(self, vector):
        return (vector - self).normalize()

    def __sub__(self, vector):
        return Vector(
            x=self.x - vector.x,
            y=self.y - vector.y 
        )

    def __truediv__(self, factor):
        return Vector(
            x=self.x / factor,
            y=self.y / factor 
        )

    def __repr__(self):
        return f"<Vector (x: {self.x}, y: {self.y})>"