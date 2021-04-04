def read_file(input_file):
    output = ''
    try:
        with open (input_file) as f:
            output = f.read()
            if not output:
                print('No data found in file: ' + input_file + ' exiting...')
                exit()
    except IOError as e:
        print(e)
    finally:
        return output

def find_provider_with_cheapest_shipping(providers, size):
    found_provider = ''
    lowest = providers[0].prices[0]
    for provider in providers:
        if provider.get_shipping_price_by_size(size) <= lowest:
            lowest = provider.get_shipping_price_by_size(size)
            found_provider = provider
    return found_provider

def get_provider_by_code(providers, code):
    for provider in providers:
      if code == provider.provider:
        return provider