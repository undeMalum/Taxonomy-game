import sqlite3
from os import listdir, chdir
from photos_db import convert, exists, insert

conn = sqlite3.connect("photos.db")
cursor = conn.cursor()


def image_naming():
    chdir("all_photos")
    for in_all_photos in listdir():
        if in_all_photos != "classes":
            phylum_char_class = exists("phyla_characteristics", "phyla_characteristics_t", in_all_photos[:-2])
            print("in all photos: ", in_all_photos)
            if not phylum_char_class:
                # if this value is not contained in the table, add it
                insert("phyla_characteristics", "phyla_characteristics_t", in_all_photos[:-2])
            chdir(f"{in_all_photos}/{in_all_photos[:-2]}_2")
            for folders in listdir():
                found_phylum = exists("phyla", "phylum_name", folders)
                print("folders: ", folders)
                if not found_phylum:
                    # if this value is not contained in the table, add it
                    insert("phyla", "phylum_name", folders)
                chdir(f"{folders}")
                for filename in listdir():
                    binary_picture = convert(filename)
                    picture_found = exists("phyla_and_characteristics", "photo", binary_picture)
                    print("filename: ", filename)
                    if not picture_found:
                        # retrieve id based on the name of the variable "in_all_photos"
                        cursor.execute("""select phyla_characteristics_id from phyla_characteristics
                                                    where phyla_characteristics_t = (:phyla_or_characteristics);""",
                                       {"phyla_or_characteristics": in_all_photos[:-2]})
                        phyla_char = cursor.fetchone()[0]
                        # retrieve phylum id basen on the name of the variable "folder_2"
                        cursor.execute("""select phylum_id from phyla where phylum_name = (:phylum);""",
                                       {"phylum": folders})
                        phylum = cursor.fetchone()[0]
                        cursor.execute("""insert into phyla_and_characteristics values
                                        (:phyla_characteristics_id, :phylum_id, :photo);""",
                                       {"phyla_characteristics_id": phyla_char, "phylum_id": phylum,
                                        "photo": binary_picture})
                        conn.commit()

                chdir("..")
            chdir("../..")
        else:
            chdir(f"{in_all_photos}")
            for folders_2 in listdir():
                found_phylum = exists("phyla", "phylum_name", folders_2)
                print("folders_2", folders_2)
                if not found_phylum:
                    insert("phyla", "phylum_name", folders_2)
                chdir(f"{folders_2}")
                for folders_1 in listdir():
                    found_class = exists("name_classes", "class_name", folders_1)
                    print("folders_1: ", folders_1)
                    if not found_class:
                        insert("name_classes", "class_name", folders_1)
                    chdir(f"{folders_1}")
                    for filename in listdir():
                        binary_picture = convert(filename)
                        picture_found = exists("classes", "photo", binary_picture)
                        print("filename class: ", filename)
                        if not picture_found:
                            # retrieve id (phylum or characteristics)
                            # based on the name of the variable "in_all_photos"
                            cursor.execute("""select phylum_id from phyla where phylum_name = (:phylum);""",
                                           {"phylum": folders_2})
                            phylum = cursor.fetchone()[0]
                            # retrieve phylum id basen on the name of the variable "folder_2"
                            cursor.execute("""select class_id from name_classes where class_name = (:class);""",
                                           {"class": folders_1})
                            class_p = cursor.fetchone()[0]
                            cursor.execute("""insert into classes values (:phylum_id, :class_id, :photo);""",
                                           {"phylum_id": phylum, "class_id": class_p, "photo": binary_picture})
                            conn.commit()
                    chdir("..")
                chdir("..")
            chdir("..")
    chdir("..")


image_naming()
