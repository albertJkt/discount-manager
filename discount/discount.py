from discount.provider import Provider
import discount.helpers as helper

provider_LP = Provider('LP', ['S', 'M', 'L'], [1.5, 4.9, 6.9])
provider_MR = Provider('MR', ['S', 'M', 'L'], [2, 3, 4])

INPUT_FILE = 'input2.txt'
TOTAL_MONTHLY_DISCOUNT = 10
PACKAGE_SIZE_FOR_LOWEST_PRICE = 'S'
DISCOUNT_FOR_LP_PACKAGE_SIZE = 'L'
DISCOUNT_FOR_LP_PROVIDER_CODE = 'LP'
PROVIDERS = [provider_LP, provider_MR]

def discount_for_small_packages(line, provider, acc_discount):
  #Find cheapest shipping provider from known providers (should work with more than 2 known providers)
  cheapest_provider = helper.find_provider_with_cheapest_shipping(PROVIDERS, PACKAGE_SIZE_FOR_LOWEST_PRICE)
  cheapest_price = cheapest_provider.get_shipping_price_by_size(PACKAGE_SIZE_FOR_LOWEST_PRICE)
  
  if provider.provider == cheapest_provider.provider:
    line = line + ' ' + str(format(cheapest_price, '.2f')) + ' -'
    return line, 0
  else:
    price = provider.get_shipping_price_by_size(PACKAGE_SIZE_FOR_LOWEST_PRICE)
    requested_discount = price - cheapest_price
    line, actual_discount = calculate_discount(price, acc_discount, requested_discount, line)
    return line, actual_discount

def discount_for_third_package_LP(line, provider, acc_discount):
  price = provider.get_shipping_price_by_size(DISCOUNT_FOR_LP_PACKAGE_SIZE)
  requested_discount = price
  line, actual_discount = calculate_discount(price, acc_discount, requested_discount, line)
  return line, actual_discount

def calculate_discount(price, acc_discount, discount, line):
  if acc_discount + discount < TOTAL_MONTHLY_DISCOUNT:
    line = line + ' ' + str(format(price - discount, '.2f')) + ' ' + str(format(discount, '.2f'))
  else:
    if TOTAL_MONTHLY_DISCOUNT - acc_discount > 0:
      discount = TOTAL_MONTHLY_DISCOUNT - acc_discount
      line = line + ' ' + str(format(price - discount, '.2f')) + ' ' + str(format(discount, '.2f'))
    else:
      discount = 0
      line = line + ' ' + str(format(price, '.2f')) + ' -'
  #Since we are dealing with floats, sometimes it can return not what we actually expect it to return
  #For example in case discount is close to 0.1, python sometimes can return value 0.09999999999999964
  #So for the safety we will round discount to 2 numbers after .
  return line, round(discount,2)
  

def apply_discount_rules():
    #INITIATE VARIABLES THAT ARE REQUIRED
    current_month = ''
    previous_month = ''
    total_discount = 0
    l_package_lp_during_month = 0

    data = helper.read_file(INPUT_FILE)

    for line in data.splitlines():
      contents = line.split()
      package_size = ''
      provider_code = ''

      #Check if line is correct (date, size, provider)
      #Array is split by whitespace and always must contain 3 elements
      if len(contents) == 3:
        if previous_month == '': previous_month = line[5:7]
        package_size = contents[1]
        provider_code = contents[len(contents)-1]
      else:
        print(line + ' Ignored')
        continue
      
      current_month = line[5:7]
      #Get current month and check if it's new month. If it's new month update discount balance and counter for 3rd L package 
      if current_month != previous_month:
        l_package_lp_during_month = 0
        total_discount = 0
      provider = helper.get_provider_by_code(PROVIDERS, provider_code)

      #APPLY DISCOUNTS ACCORDING TO RULES
      if package_size == PACKAGE_SIZE_FOR_LOWEST_PRICE:
        line, discount = discount_for_small_packages(line, provider, total_discount)
        total_discount += discount
      elif provider.provider == DISCOUNT_FOR_LP_PROVIDER_CODE and package_size == DISCOUNT_FOR_LP_PACKAGE_SIZE:
        #previous_month == '' - in case we hit scenario where 1st occurance is LP with L size
        #So previous month is still not set but we want index to increase
        if current_month == previous_month:
          l_package_lp_during_month += 1
          #APPLY DISCOUNT ONLY IF IT'S 3RD OCCURANCE
          if l_package_lp_during_month < 3 or l_package_lp_during_month > 3:
            line = line + ' ' + str(format(provider.get_shipping_price_by_size(package_size), '.2f')) + ' -'
          else:
            line, discount = discount_for_third_package_LP(line, provider, total_discount)
            total_discount += discount
      else:
        line = line + ' ' + str(format(provider.get_shipping_price_by_size(package_size), '.2f')) + ' -'
      
      print(line)
      previous_month = current_month