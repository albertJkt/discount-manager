import pytest

from discount_manager.discount import helpers
from discount_manager.discount.provider import Provider

def test_helper_find_cheapest_provider_for_S_package():
  providers = [Provider('LP', ['S', 'M', 'L'], [1.5, 4.9, 6.9]), Provider('ZX', ['S', 'M', 'L'], [1, 4, 6]), Provider('LU', ['S', 'M', 'L'], [1.5, 4.9, 6.9])]

  found_provider = helpers.find_provider_with_cheapest_shipping(providers, 'S')

  assert found_provider.provider == 'ZX'
  assert found_provider.prices[0] == 1