import os
import shutil


def main():
    raw_path = "C:/MyComputer/Tools/VideoToBook.cn/VTBStart/Library/Preference/user/leolu/vtb/"
    new_path = "D:/Workoo_backup/book_pdf/"

    for value in os.listdir(raw_path):
        if "美音" in value:
            continue

        path = os.path.join(raw_path, value) + "/"
        for filename in os.listdir(path):
            filetype = filename.split(".")[-1]
            if filetype == "vtb":
                os.remove(os.path.join(path, filename))
            elif filetype == "mp3":
                dirname = os.path.join(
                    new_path, "{}/{}/mp3/".format(value,
                                                  filename.split(".")[0]))
                os.makedirs(dirname)
                shutil.move(os.path.join(path, filename), dirname)
                shutil.move(
                    os.path.join(new_path, filename.replace("mp3", "pdf")),
                    dirname.replace("mp3/", ""))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()