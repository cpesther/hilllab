from multiprocessing import Pool
def square(x):
    return x**2

if __name__ == "__main__":
 
    numbers = [1, 2, 3, 4, 5]
    
    with Pool() as pool:
        squares = pool.map(square, numbers)
    
    print(squares)
    