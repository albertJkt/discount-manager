import pytest

from discount_manager.discount import discount
from discount_manager.discount.provider import Provider

def test_discount_for_small_packages():
  input_line = '2015-02-01 S MR'
  output_line = '2015-02-01 S MR 1.50 0.50'

  test, discounted = discount.discount_for_small_packages(input_line, Provider('MR', ['S', 'M', 'L'], [2, 3, 4]), 0)

  assert  test == output_line
  assert discounted == 0.50

def test_discount_for_small_packages_with_accumulated_discount():
  input_line = '2015-02-01 S MR'
  output_line = '2015-02-01 S MR 1.90 0.10'

  test, discounted = discount.discount_for_small_packages(input_line, Provider('MR', ['S', 'M', 'L'], [2, 3, 4]), 9.9)

  assert  test == output_line
  assert discounted == 0.10

def test_discount_for_lp_large_packages():
  input_line = '2015-02-01 L LP'
  output_line = '2015-02-01 L LP 0.00 6.90'

  test, discounted = discount.discount_for_third_package_LP(input_line, Provider('LP', ['S', 'M', 'L'], [1.5, 4.9, 6.9]), 0)

  assert  test == output_line
  assert discounted == 6.90

def test_discount_for_lp_large_packages_with_accumulated_discount():
  input_line = '2015-02-01 L LP'
  output_line = '2015-02-01 L LP 2.90 4.00'

  test, discounted = discount.discount_for_third_package_LP(input_line, Provider('LP', ['S', 'M', 'L'], [1.5, 4.9, 6.9]), 6)

  assert  test == output_line
  assert discounted == 4.00

def test_discount_algorithm_max_discount_reached():
  input_line = '2015-02-01 L LP'
  output_line = '2015-02-01 L LP 6.90 -'

  test, discounted = discount.calculate_discount(6.9, 10, 6.9, input_line)

  assert test == output_line
  assert discounted == 0.00

def test_discount_algorithm_close_to_max():
  input_line = '2015-02-01 L LP'
  output_line = '2015-02-01 L LP 6.89 0.01'

  test, discounted = discount.calculate_discount(6.9, 9.99, 6.9, input_line)

  assert test == output_line
  assert discounted == 0.01

def test_discount_algorithm_full():
  input_line = '2015-02-01 L LP'
  output_line = '2015-02-01 L LP 0.00 6.90'

  test, discounted = discount.calculate_discount(6.9, 0, 6.9, input_line)

  assert test == output_line
  assert discounted == 6.90


