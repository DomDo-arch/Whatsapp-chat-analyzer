import numpy as np

def gini(x):
    # Convert to a NumPy array and sort in ascending order
    x = np.asarray(x, dtype=np.float64)
    sorted_x = np.sort(x)
    n = len(x)
    
    # Check for zero mean to avoid division by zero
    if np.sum(sorted_x) == 0:
        return 0.0
        
    # Relative mean absolute difference formula
    # G = sum_i (2i - n - 1) * x_i / (n * sum_i x_i)
    index = np.arange(1, n + 1)
    return (np.sum((2 * index - n - 1) * sorted_x)) / (n * np.sum(sorted_x))
   
if __name__ == "__main__":
	
	k = 100
	initial_values = [1,2,3]
	
	print(gini(initial_values))
	print(gini([i+k for i in initial_values]))