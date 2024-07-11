import time

def timeit(func):
    def wrapper(*args, **kwargs):
        # Record the start time before the function execution
        start_time = time.time()
        
        # Call the original function and store its result
        result = func(*args, **kwargs)
        
        # Record the end time after the function execution
        end_time = time.time()
        
        # Calculate the execution time
        execution_time = end_time - start_time
        
        # Print the execution time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        # Return the result of the original function
        return result
    
    # Return the wrapper function
    return wrapper

# Example usage
@timeit
def some_function():
    # Simulate some work with a sleep
    time.sleep(2)

some_function()

# explanation
# Measure execution time