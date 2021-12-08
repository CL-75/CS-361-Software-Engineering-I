import csv

#def sort_columns(col_header, data):

def reader(filepath):
    category_list = []

    csv_columns = [
        "uniq_id",
        "product_name",
        "number_of_reviews",
        "average_review_rating",
        "amazon_category_and_sub_category"
    ]

    with open(filepath, "r") as file:
        Reader = csv.reader(file)
        col_headers = next(Reader)
        for i in Reader:
            categories = []
            for x, y in enumerate(col_headers):
                if y in csv_columns:
                    categories[y] = sort_columns(y, i[x])
            category_list.append(categories)

        return category_list

