import numpy as np

def concat_arrays(a, b, direction="horizontal"):
    try:
        if direction == "horizontal":
            # Check same number of rows
            if a.shape[0] != b.shape[0]:
                return "cannot concatenate because size mismatch"
            return np.hstack((a, b))
        
        elif direction == "vertical":
            # Check same number of columns
            if a.shape[1] != b.shape[1]:
                return "cannot concatenate because size mismatch"
            return np.vstack((a, b))
        
        else:
            return "Invalid direction. Use 'horizontal' or 'vertical'."
    
    except Exception as e:
        return f"Error: {e}"
