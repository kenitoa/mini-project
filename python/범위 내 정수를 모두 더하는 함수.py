def sum_all(start, end):
    output=0
    for i in range(start, end+1):
        output+=i
    return output

print(sum_all(0, 100))