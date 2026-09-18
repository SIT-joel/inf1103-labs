def get_valid_input(inventory,failed_attempts):
    user_input = ""
    while True:
        overstock = False
        user_input = input("Enter a stock quantity: ")

        if user_input == "quit":
            return ("quit",failed_attempts,overstock,inventory)              

        if not user_input.isdigit():
            print("Error: stock quantity must be a number or it must not be a negative number")
            failed_attempts += 1
            continue               

        quantity = int(user_input)

        # if quantity < 0:
        #     print("Error: negative numbers not allowed")
        #     failed_attempts += 1
        #     continue
        
        inventory += quantity
        if inventory > 500:
          print("Overstock — total inventory exceeds 500 units")
          overstock = True
          return (quantity,failed_attempts,overstock,inventory)

        return (quantity,failed_attempts,overstock,inventory) 

def delivery_cost_calculator(quantity):
    delivery_cost = 0.1 # Unit of delivery per item of stock
    current_total = quantity * delivery_cost
    return current_total

def process_delivery(current_total,new_value):
    current_total = current_total + new_value
    return current_total

def calculate_tax(amount):
    tax = 0.1 # 10% tax aplied on delivery_cost
    amount = amount * tax
    print(amount)
    return amount

def generate_report(total_units, failed_attempts):
    print("Total Units Processed including tax and delivery fee:", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)

def main():
    quantity = 0
    inventory = 0
    failed_attempts = 0
    current_value = 0
    while quantity != "quit":
      quantity,failed_attempts,overstock,inventory = get_valid_input(inventory,failed_attempts)
      if quantity != "quit":
        new_value = delivery_cost_calculator(quantity)
        taxed_value = calculate_tax(new_value)
        current_value = process_delivery(current_value,taxed_value)
        if overstock == True: break
      else:
        break
    generate_report(current_value,failed_attempts)

main()