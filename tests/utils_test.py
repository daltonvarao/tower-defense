import unittest

from game.lib.utils import Vector, assets_file
from game.lib.skull import Skull


class TestVector(unittest.TestCase):
    def test_vector_constructor_should_receive_coords(self):
        x, y = 0, 0
        vector = Vector(x=x, y=y)
        self.assertEqual(vector.x, x)
        self.assertEqual(vector.y, y)

    def test_vector_constructor_should_receive_sprite_instance(self):
        skull = Skull('./game/assets/skull.png', pos_xy=(0, 0), coords=[])
        vector = Vector(sprite=skull)
        self.assertEqual(vector.x, skull.rect.centerx)
        self.assertEqual(vector.y, skull.rect.centery)

    def test_vector_construct_should_return_error_if_empty(self):
        self.assertRaises(Exception, lambda: Vector())

    def test_vector_distance_to_should_return_distance_between_two_vectors(self):
        vector_one = Vector(x=5, y=10)
        vector_two = Vector(x=1, y=7)
        dist_one_to_two = vector_one.distance_to(vector_two)
        dist_two_to_one = vector_two.distance_to(vector_one)

        self.assertEqual(dist_one_to_two, 5)
        self.assertEqual(dist_two_to_one, 5)
        self.assertNotEqual(dist_one_to_two, 25)
        self.assertNotEqual(dist_two_to_one, 25)
        self.assertEqual(dist_one_to_two, dist_two_to_one)
    
    def test_vector_sub_should_return_diff_between_two_vectors(self):
        vector_one = Vector(x=5, y=10)
        vector_two = Vector(x=1, y=7)
        diff_one_to_two = vector_one - vector_two

        self.assertEqual(diff_one_to_two.x, 4)
        self.assertEqual(diff_one_to_two.y, 3)

    def test_vector_magnitude_should_return_norma_of_vector(self):
        vector = Vector(x=4, y=3)
        magnitude = vector.magnitude()
        self.assertEqual(magnitude, 5)

    def test_normalize_should_return_division_between_coords_and_magnitude(self):
        vector = Vector(x=6, y=8)
        result = vector.normalize()
        self.assertEqual(result.x, 0.6)
        self.assertEqual(result.y, 0.8)


class TestModuleMethods(unittest.TestCase):
    def test_assets_file_should_return_a_string_with_path_to_file_in_assets_folder_(self):
        file = assets_file('tower.png')
        self.assertIsInstance(file, str)
        self.assertEqual(file, './game/assets/tower.png')

if __name__ == "__main__":
    unittest.main()
