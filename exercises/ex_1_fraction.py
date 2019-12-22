
def gcd(m, n):
	while m % n != 0:
		old_m = m
		old_n = n
		m = old_n
		n = old_m % old_n
	return n

class Fraction:
	def __init__(self, top, bottom):
		"""
		2. In many ways it would be better if all fractions were maintained in lowest terms right
		from the start. Modify the constructor for the Fraction class so that GCD is used to
		reduce fractions immediately. Notice that this means the __add__ function no longer
		needs to reduce. Make the necessary modifications.
		"""
		
		self.gcd = gcd(top, bottom)
		self.num = int(top) // self.gcd
		self.den = int(bottom) // self.gcd
	
	def __str__(self):
		return str(self.num) + "/" + str(self.den)
	
	def show(self):
		LOGGER.info(self.num, "/", self.den)
	
	def __add__(self, other_fraction):
		new_num = self.num * other_fraction.den + self.den * other_fraction.num
		new_den = self.den * other_fraction.den
		return Fraction(new_num, new_den)
	
	def __eq__(self, other):
		first_num = self.num * other.den
		second_num = other.num * self.den
		return first_num == second_num

	def __sub__(self, other):
		num = self.num * other.den - other.num * self.den
		den = self.den * other.den
		return Fraction(num, den)

	def __mul__(self, other):
		num  = self.num * other.num
		den = self.den * other.den
		
		return Fraction(num, den)

	def __truediv__(self, other):
		LOGGER.info("calling __truediv__")
		num = self.num * other.den
		den = self.den * other.num
		return Fraction(num, den)

	def __gt__(self, other) -> bool:
		return self.num * other.den > other.num * self.den

	def __ge__(self, other) -> bool:
		return self.num * other.den >= other.num * self.den

	def __lt__(self, other) -> bool:
		return self.num * other.den < other.num * self.den

	def __le__(self, other) -> bool:
		return self.num * other.den <= other.num * self.den

	def __ne__(self, other) -> bool:
		return self.num * other.den == other.num * self.den

	def __radd__(self, other_fraction):
		new_num = self.num * other_fraction.den + self.den * other_fraction.num
		new_den = self.den * other_fraction.den
		return Fraction(new_num, new_den)

	def __iadd__(self, other_fraction):
		new_num = self.num * other_fraction.den + self.den * other_fraction.num
		new_den = self.den * other_fraction.den
		return Fraction(new_num, new_den)

	def __repr__(self):
		return f'Fraction({self.num}/{self.den})'
	


	def get_num(self):
		return self.num

	def get_den(self):
		return self.den

def main():
	x = Fraction(10, 20)
	y = Fraction(20, 30)
	LOGGER.info(x + y)
	LOGGER.info(x == y)
	LOGGER.info(x.get_den())
	LOGGER.info(x.get_num())
	LOGGER.info(f'substract: {Fraction(2,5) - Fraction(3, 8)}')
	LOGGER.info(f'Multiply: {Fraction(2,5) * Fraction(3, 8)}')
	LOGGER.info(f'Division: {Fraction(2,5) / Fraction(3, 8)}')
	LOGGER.info(f'Greater: {Fraction(2,5) > Fraction(3, 8)}')
	LOGGER.info(f'Smaller: {Fraction(3, 8) < Fraction(2, 5)}')
	LOGGER.info(f'Smaller or equal: {Fraction(3, 8) <= Fraction(2, 8)}')
	LOGGER.info(f'Not equal: {Fraction(23, 8) != Fraction(3, 8)}')

	LOGGER.info(f'Smaller: {Fraction(2, 5) < Fraction(2, 5)}')
	first = Fraction(2, 5)
	first += Fraction(2, 5)
	LOGGER.info(f'Iadd: {first}')
	LOGGER.info(f'Repr: {repr(first)}')


if __name__ == '__main__':
	main()