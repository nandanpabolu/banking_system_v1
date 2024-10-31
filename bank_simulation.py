import threading
import time
import random

# Global Shared Resources
safe_access = threading.Semaphore(2)  # Only 2 tellers can be in the safe
manager_access = threading.Semaphore(1)  # Only 1 teller can interact with the manager
door_access = threading.Semaphore(2)  # Only 2 customers can enter the bank at a time
line_lock = threading.Semaphore(1)  # Mutex for the customer line
customer_ready = threading.Semaphore(0)  # Signal for customers ready to be served

# Shared Data Structures
customer_line = []
customers_served = 0
customers_served_lock = threading.Semaphore(1)
TOTAL_CUSTOMERS = 5  # Reduced for testing

# Teller Thread Function
def teller_thread(id):
    global customers_served
    print(f"Teller {id} is ready to serve.")
    while True:
        # Wait for a customer to be ready
        customer_ready.acquire()
        
        # Check if all customers have been served
        customers_served_lock.acquire()
        if customers_served >= TOTAL_CUSTOMERS:
            customers_served_lock.release()
            customer_ready.release()  # Allow other tellers to exit
            break
        customers_served_lock.release()
        
        # Get customer from the line
        line_lock.acquire()
        if customer_line:
            customer = customer_line.pop(0)
            customer['teller_id'] = id  # Assign teller ID to customer
            line_lock.release()
        else:
            line_lock.release()
            continue
        
        print(f"Teller {id} is serving Customer {customer['id']}.")
        
        # Signal customer to proceed
        customer['teller_semaphore'].release()
        
        # Wait for customer to introduce themselves
        customer['teller_semaphore'].acquire()
        
        # Ask for transaction
        print(f"Teller {id} asks Customer {customer['id']} for the transaction.")
        customer['teller_semaphore'].release()
        
        # Wait for customer to tell transaction
        customer['teller_semaphore'].acquire()
        transaction = customer['transaction']
        print(f"Teller {id} is handling the {transaction} transaction for Customer {customer['id']}.")
        
        # Transaction processing steps
        if transaction == 'Withdrawal':
            print(f"Teller {id} is going to the manager.")
            manager_access.acquire()
            print(f"Teller {id} is getting the manager's permission.")
            time.sleep(random.uniform(0.005, 0.03))
            print(f"Teller {id} got the manager's permission.")
            manager_access.release()
        
        # Go to the safe
        print(f"Teller {id} is going to the safe.")
        safe_access.acquire()
        print(f"Teller {id} is in the safe.")
        time.sleep(random.uniform(0.01, 0.05))
        print(f"Teller {id} is leaving the safe.")
        safe_access.release()
        
        # Inform customer transaction is done
        print(f"Teller {id} informs Customer {customer['id']} the transaction is complete.")
        customer['teller_semaphore'].release()
        
        # Wait for customer to acknowledge and leave
        customer['teller_semaphore'].acquire()
        
        # Update customers served
        customers_served_lock.acquire()
        customers_served += 1
        customers_served_lock.release()
    
    print(f"Teller {id} is closing for the day.")

# Customer Thread Function
def customer_thread(id):
    transaction = random.choice(['Deposit', 'Withdrawal'])
    teller_semaphore = threading.Semaphore(0)  # For synchronization with teller
    
    customer_info = {
        'id': id,
        'transaction': transaction,
        'teller_semaphore': teller_semaphore,
        'teller_id': None
    }
    
    print(f"Customer {id} is going to the bank.")
    # Enter the bank
    print(f"Customer {id} is waiting to enter the bank.")
    door_access.acquire()
    print(f"Customer {id} has entered the bank.")
    
    # Get in line
    line_lock.acquire()
    customer_line.append(customer_info)
    print(f"Customer {id} is getting in line.")
    line_lock.release()
    
    # Signal that a customer is ready
    customer_ready.release()
    
    # Wait for teller to be assigned and to proceed
    teller_semaphore.acquire()
    assigned_teller_id = customer_info['teller_id']
    print(f"Customer {id} introduces itself to Teller {assigned_teller_id}.")
    teller_semaphore.release()
    
    # Wait for teller to ask for transaction
    teller_semaphore.acquire()
    print(f"Customer {id} asks for a {transaction} transaction.")
    teller_semaphore.release()
    
    # Wait for teller to complete transaction
    teller_semaphore.acquire()
    print(f"Customer {id} thanks Teller {assigned_teller_id} and leaves the bank.")
    teller_semaphore.release()
    
    # Leave the bank
    door_access.release()

# Main Function
def main():
    # Create Teller Threads
    tellers = []
    for i in range(3):
        t = threading.Thread(target=teller_thread, args=(i,))
        tellers.append(t)
        t.start()
    
    # Create Customer Threads
    customers = []
    for i in range(TOTAL_CUSTOMERS):
        c = threading.Thread(target=customer_thread, args=(i,))
        customers.append(c)
        c.start()
        time.sleep(0.01)  # Slight delay to simulate arrival times
    
    # Wait for Customers to Finish
    for c in customers:
        c.join()
    
    # Wait for Tellers to Finish
    for t in tellers:
        t.join()
    
    print("The bank is now closed.")

if __name__ == "__main__":
    main()
