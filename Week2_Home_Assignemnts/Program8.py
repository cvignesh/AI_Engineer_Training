prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

#a) Extract the middle five primes: Create a new list containing the five primes in the middle 
# of the original list.
print("Middle Five primes:", prime_numbers[2:8])

#b) Get every second prime: Create a new list containing every second number from the original list,
# starting from the beginning.
Updated_list1 = prime_numbers[ : :2]
print("Every Second prime List:", Updated_list1)

#c) Use negative indexing: Create a new list containing the last three primes of the list.
print("Last 3 primes:", prime_numbers[-4:-1])

#d) Reverse the list: Create a new list that contains all the elements of the original list 
# in reverse order.
reverse_list = prime_numbers[: :-1]
print("Reverse in original order",reverse_list)

#e) Descending Order: Sort the list in descending order and store it in a new list.
sorted_reverse_list = sorted(prime_numbers, reverse=True)
print("Sorted in reverse:", sorted_reverse_list)