input = input('digit: ')

try:
	digit = int(float(input))
	if digit < 0:
		digit *= -1
	if digit > 10:
		digit = 10
	print(digit, 'is a digit')
except:
	print(input, 'is not a digit')


print('the last digit of digit is: ', str(input)[-1])