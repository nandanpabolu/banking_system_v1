# Bank Simulation

## Overview

This program simulates a bank with three tellers and multiple customers using Python's threading and synchronization mechanisms. The simulation involves customers entering the bank to perform transactions (either deposit or withdrawal) and interacting with tellers who process these transactions while adhering to specific constraints.

## Features

- **Three Tellers**: Each teller can serve one customer at a time.
- **Fifty Customers**: Customers randomly decide to perform a deposit or withdrawal.
- **Bank Constraints**:
  - Only two customers can enter the bank simultaneously.
  - Only two tellers can be in the safe at the same time.
  - Only one teller can interact with the manager at a time.
- **Synchronization**: Uses semaphores and locks to manage concurrent access to shared resources.

## Requirements

- **Python 3.x**: Ensure you have Python 3 installed on your system.
- **Standard Libraries**: Utilizes `threading`, `time`, and `random` modules from Python's standard library.

## How to Run the Program

1. **Save the Script**:
   - Copy the `bank_simulation.py` code and save it in a directory of your choice.

2. **Open a Terminal**:
   - Navigate to the directory containing the `bank_simulation.py` file.

3. **Run the Script**:
   - Execute the program using the following command:
     ```bash
     python bank_simulation.py
     ```
     - If `python` refers to Python 2 on your system, use:
       ```bash
       python3 bank_simulation.py
       ```

4. **Observe the Output**:
   - The program will print messages to the console, detailing the interactions between customers and tellers.

## Program Structure

### Global Shared Resources

- **Semaphores**:
  - `safe_access`: Limits safe access to two tellers.
  - `manager_access`: Ensures only one teller interacts with the manager at a time.
  - `door_access`: Limits bank entry to two customers at a time.
  - `line_lock`: Mutex for accessing the customer line.
  - `customer_ready`: Signals when a customer is ready to be served.
- **Shared Data**:
  - `customer_line`: Queue for customers waiting to be served.
  - `customers_served`: Counter for the number of customers served.
  - `customers_served_lock`: Mutex for updating `customers_served`.
  - `TOTAL_CUSTOMERS`: Set to 5 for testing; adjust as needed.

### Functions

#### 1. `teller_thread(id)`

- **Purpose**: Simulates the behavior of a teller.
- **Behavior**:
  - Signals readiness to serve customers.
  - Waits for a customer to be ready.
  - Interacts with the customer, processing their transaction.
  - Accesses the manager and safe as required.
  - Updates the count of customers served.
  - Closes when all customers have been served.

#### 2. `customer_thread(id)`

- **Purpose**: Simulates the behavior of a customer.
- **Behavior**:
  - Decides on a transaction type randomly.
  - Waits to enter the bank (limited by `door_access`).
  - Gets in line and waits to be served.
  - Interacts with the assigned teller.
  - Leaves the bank after the transaction is complete.

#### 3. `main()`

- **Purpose**: Entry point of the program.
- **Behavior**:
  - Creates and starts teller and customer threads.
  - Waits for all threads to complete.
  - Prints a message when the bank is closed.

## Adjusting the Simulation

- **Number of Customers**:
  - Change the `TOTAL_CUSTOMERS` variable to simulate more or fewer customers.
    ```python
    TOTAL_CUSTOMERS = 50  # Set to desired number
    ```
- **Customer Arrival Delay**:
  - Modify the sleep time in the customer creation loop to simulate different arrival rates.
    ```python
    time.sleep(0.01)  # Adjust delay as needed
    ```

## Output Explanation

- **Customer Messages**:
  - `"Customer X is going to the bank."`: Customer X starts their journey.
  - `"Customer X is waiting to enter the bank."`: Waiting due to door limit.
  - `"Customer X has entered the bank."`: Customer enters the bank.
  - `"Customer X is getting in line."`: Customer joins the line.
  - `"Customer X introduces itself to Teller Y."`: Begins interaction.
  - `"Customer X asks for a Deposit/Withdrawal transaction."`: Specifies transaction.
  - `"Customer X thanks Teller Y and leaves the bank."`: Transaction complete.

- **Teller Messages**:
  - `"Teller Y is ready to serve."`: Teller is available.
  - `"Teller Y is serving Customer X."`: Begins serving a customer.
  - `"Teller Y asks Customer X for the transaction."`: Requests transaction details.
  - `"Teller Y is handling the Deposit/Withdrawal transaction for Customer X."`: Processes transaction.
  - `"Teller Y is going to the manager."`: Needs manager's permission.
  - `"Teller Y is going to the safe."`: Accesses the safe.
  - `"Teller Y informs Customer X the transaction is complete."`: Notifies completion.

## Troubleshooting Tips

- **Common Issues**:
  - **Deadlocks**: Ensure every `acquire()` has a corresponding `release()`.
  - **Incorrect Output Order**: Due to threading, message order may vary.
  - **Exceptions/Errors**: Check for typos or indentation errors.

- **Debugging**:
  - Add additional `print()` statements to trace execution.
  - Test with a smaller number of customers to simplify output.

## Extending the Simulation

- **Modify Constraints**: Adjust semaphore values to change resource limits.
- **Additional Features**: Implement new roles or behaviors, such as loan officers or security guards.
- **Logging**: Redirect output to a file for analysis:
  ```bash
  python bank_simulation.py > output.txt









**Instructions:**

- **Saving the File**:
  - Copy the entire content between the triple backticks (` ``` `) and paste it into a new file.
  - Save the file as `README.md` in the same directory as your `bank_simulation.py` script.

- **Viewing the README**:
  - **On GitHub or GitLab**: If you place your files in a repository, the `README.md` file will be automatically rendered.
  - **Using a Markdown Viewer**: You can use a text editor or a Markdown viewer to read the file with proper formatting.
  - **Online Markdown Viewers**: You can also use online tools like [Dillinger](https://dillinger.io/) or [StackEdit](https://stackedit.io/) to view the rendered Markdown.

**Note**: The `README.md` file provides comprehensive information about the program, how to run it, and how to adjust its parameters. It serves as a helpful guide for anyone using or modifying the simulation.

If you have any questions or need further assistance, feel free to ask!
