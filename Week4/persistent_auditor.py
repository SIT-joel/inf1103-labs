def load_inventory():
    with open("inventory.txt","r+") as f:
        inventory = f.read()
        if len(inventory) == 0: # Empty file or just created file
            transaction_history = []
            total = 0
        else:
            transaction_history = inventory.splitlines()
            total = transaction_history.pop()
        
    return transaction_history,total

def get_valid_input(transaction_history,total,failed_attempts):
    user_input = ""
    product_name = ""
    while True:
        while True:
            product_name = input("Enter Product Name (or 'quit' to exit): ")
            if len(product_name) != 0:
                break
            else:
                print("Invalid Product Name! ")
        overstock = False

        if product_name == "quit":
            return ("quit",failed_attempts,transaction_history,total)

        user_input = input("Enter a stock quantity: ")

        if user_input == "quit":
            return ("quit",failed_attempts,transaction_history,total)              

        if not user_input.isdigit():
            print("Error: stock quantity must be a number or it must not be a negative number")
            failed_attempts += 1
            continue               

        quantity = int(user_input)
        
        order_no = 1001 + len(transaction_history)
        transaction = f"{order_no}, {product_name}, {quantity}"
        transaction_history.append(transaction)
        total = int(total) + 1
        print(f"New Order Added: \n{transaction} \nTax: $0.10 | Total Inventory: {len(transaction_history)} \n")

        return (quantity,failed_attempts,transaction_history,total) 

def save_inventory(transaction_history,total):
    with open("inventory.txt","w") as f:
        content = ""
        for transaction in transaction_history:
          content += (transaction + "\n")
        content += str(total)
        f.write(content)
    return None

def audit_report(transaction_history,total,failed_attempts):
    print("=== Audit Report ===")
    print(f"Total Transactions Recorded: {len(transaction_history)}")
    print(f"Total Units Processed: {total}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def main():
    failed_attempts = 0
    transaction_history,total = load_inventory()
    print("Current Orders:")
    for past_transaction in transaction_history:
        print(past_transaction)
    while True:
        quantity,failed_attempts,transaction_history,total = get_valid_input(transaction_history,total,failed_attempts)
        if quantity == "quit": # break if quit
            save_inventory(transaction_history,total)
            print("Order successfully saved to inventory.txt")
            audit_report(transaction_history,total,failed_attempts)
            break

main()