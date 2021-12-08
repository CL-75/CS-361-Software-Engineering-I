import csv

def writer(header, data, path):
    with open(path, "w") as file:
        write = csv.writer(file)
        write.writerow(header)

        for i in data:
            write.writerow([str(j) for j in i])


if __name__ == "__main__":
    print()