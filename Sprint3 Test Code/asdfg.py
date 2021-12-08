import csv


def data_reader(file_path=None):
    """ Receives a path to a csv file and returns an array of
        object with keys matching the headers. """

    # The desired columns to be read
    read_columns = [
        "uniq_id",
        "product_name",
        "number_of_reviews",
        "average_review_rating",
        "amazon_category_and_sub_category"
    ]

    data_arr = []

    with open(file_path, 'r') as csv_file:
        file_reader = csv.reader(csv_file)

        # First row of the csv is headers
        headers = next(file_reader)

        for line in file_reader:
            # This will be added to the output
            data_obj = {}

            for i, field in enumerate(headers):
                # Only specific columns returned
                if field in read_columns:
                    data_obj[field] = format_data(field, line[i])

            data_arr.append(data_obj)

    return data_arr

