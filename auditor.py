inventory = 0
user_input = ""
error = 0

while user_input != "quit":
    user_input = input("Enter a stock quantity: ")

    if user_input == "quit":
        break                      # exit BEFORE validating/adding

    if not user_input.isdigit():
        print("Error: stock quantity must be a number")
        error += 1
        continue                   # skip to next iteration — don't add it

    quantity = int(user_input)

    if quantity < 0:
        print("Error: negative numbers not allowed")
        error += 1
        continue

    inventory += quantity

    if inventory > 500:
        print("Overstock — total inventory exceeds 500 units")
        break

# Totals print on both exit paths (quit and overstock), if required just add if statement to only print for quit and not overstock
# if user_input == "quit": 
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", error)