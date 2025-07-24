with open("1.txt", "r") as f:
    content = f.read().replace("\n", "\\n")
    print(content)