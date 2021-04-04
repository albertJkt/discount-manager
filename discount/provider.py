class Provider:
  def __init__(self, provider, sizes, prices):
    self.provider = provider
    self.sizes = sizes
    self.prices = prices

  # 2 arrays with same sizes (sizes, prices)
  # sizes[0] maps to price [0]
  #i.e. If size[0] = 'S' and price[0] = 2
  # That means that price of shipping S size box is 2.
  def get_shipping_price_by_size(self, size):
    try:
      index = self.sizes.index(size)
    except ValueError:
      print('Provider does not ship provided size packages. Please check if your package size is specified correctly')
    else:
      return self.prices[index]
