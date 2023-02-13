from io import BytesIO
from photos_db import select_one, select_unusual


def random_photos(number_of_photos, selected, species_characteristics):
    # determining the range of phyla to consider based on a user's choice
    ids = []
    for chosen in selected:
        phylum_id = select_one("phyla", "phylum_id", "phylum_name", chosen[0])
        ids.append(phylum_id)
    ids = tuple(ids)

    # change to be given in function parameters
    if species_characteristics == "classes":
        # for fetching photos with answers (corresponding classes)
        table_photo = "classes"
        column_selected = "class_id"

        # for converting ids into names
        table_ans = "name_classes"
        column_ans = "class_name"

        # fetching photos with corresponding phyla (ie. answers)
        prompt = f"""select photo, {column_selected} from {table_photo} where phylum_id = (:id) order by random() 
        limit {number_of_photos};"""
        photos_and_answers = select_unusual(prompt, "id", ids[0])
    else:
        # for fetching photos with answers (corresponding phyla)
        table_photo = "phyla_and_characteristics"
        column_selected = "phylum_id"

        # for converting ids into names
        table_ans = "phyla"
        column_ans = "phylum_name"

        # fetching photos with corresponding phyla (ie. answers)
        phyla_char = select_one("phyla_characteristics", "phyla_characteristics_id", "phyla_characteristics_t",
                                species_characteristics)
        prompt = f"""select photo, {column_selected} from {table_photo} where phylum_id in {ids} and 
        phyla_characteristics_id = (:phyla_char) order by random() limit {number_of_photos};"""
        photos_and_answers = select_unusual(prompt, "phyla_char", phyla_char)

    # converting blob data to 'normal' type and converting id of phyla into their word equivalent
    directories, files = [], []
    for photo_or_answer in photos_and_answers:
        # converting photos
        files.append(BytesIO(photo_or_answer[0]))

        # fetching phyla name (answers) based on id
        direc = select_one(table_ans, column_ans, column_selected, photo_or_answer[1])
        directories.append(direc)

    return directories, files
    # later use these variables: directories, files
