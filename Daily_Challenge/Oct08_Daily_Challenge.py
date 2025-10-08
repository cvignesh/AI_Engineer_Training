import numpy as np

def reshare_nparray(array_to_shape,rows,cols):
    try:
        return array_to_shape.reshape(rows,cols)
    except ValueError:
        print("Cannot reshape")

if __name__ == "__main__":
    my_array = np.array([1,2,3,4,5,6])
    print(reshare_nparray(my_array,5,2))
    print(reshare_nparray(my_array,2,3))



