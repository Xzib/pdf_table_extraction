def delete_files(path):
    import os
    import shutil
    os.chdir(r"{}".format(path))        
    list_name = [name for name in os.listdir(".")]
    for i in list_name:
        os.remove(i)
    os.chdir(r"..")


if __name__ == "__main__":
    delete_files(path)        