from pyprocessing import PVector
import unittest

class TestPVectorMethods(unittest.TestCase):

	def setUp(self):
		self.A = PVector(1, 0)
		self.B = PVector(0, 5)
		self.C = PVector(3,4)
		self.D = PVector(4, 4)

	def test_cross(self):
		# <1, 0> x <0, 5> = 5 - 0 = 5
		self.assertEqual(self.A.cross(self.B), 5)
		# switching order should be inverse
		self.assertEqual(self.B.cross(self.A), -5)

	def test_dot(self):
		# <3, 4> * <4, 4> = 3*4 + 4*4 = 12 + 16 =  28
		self.assertEqual(self.C.dot(self.D), 28)

	def test_mag(self):
		# sqrt(3**2 + 4**2) = 5
		self.assertEqual(self.C.mag(), 5)

	def test_theta(self):
		self.assertEqual(self.A.theta(), 0)
		self.assertEqual(self.B.theta(), 90)
		self.assertEqual(self.D.theta(), 45)

	def test_theta_radians(self):
		# 45 degrees is pi/4
		self.assertAlmostEqual(self.D.theta(degree=False),
								3.14159/4.0, places=2)

	def test_setMag(self):
		self.A.setMag(self.B.mag())
		self.assertEqual(self.A.mag(), self.B.mag())

	def test_scale(self):
		self.B.scale(2)
		# 2 * 5 is 10
		self.assertEqual(self.B.mag(), 10)
		self.B.scale(-2)
		# opposite length is still length
		self.assertEqual(self.B.mag(), 20)

	def test_norm(self):
		self.C.norm()
		self.assertEqual(self.C.mag(), 1)

	def test_rotate(self):
		self.A.rotate(90)
		self.assertEqual(self.A.theta(), self.B.theta())

	def test_angle_between(self):
		self.A.x, self.A.y = 0, 1
		self.assertEqual(self.A.get_angle_between(self.B), 0)
		self.assertAlmostEqual(self.D.get_angle_between(self.A), 45)

if __name__ == '__main__':
	unittest.main()

