import os
import shutil


def main():
    raw_path = "D:/Wook/Tool/VideoToBook.cn/VTBStart/Library/Preference/user/leolu/vtb"
    new_path = "G:/Wookoo_double/VideoToBook/raw_pdf/"

    for value in os.listdir(raw_path):
        if "美音" in value:
            continue

        path = os.path.join(raw_path, value) + "/"
        for filename in os.listdir(path):
            filetype = filename.split(".")[-1]
            if filetype == "vtb":
                pass
                # os.remove(os.path.join(path, filename))
            elif filetype == "mp3":
                dirname = os.path.join(
                    new_path, "{}/{}/mp3/".format(value,
                                                  filename.split(".")[0]))
                try:
                    os.makedirs(dirname)
                except FileExistsError as exc:
                    pass
                except FileNotFoundError:
                    continue

                try:
                    shutil.move(os.path.join(path, filename), dirname)
                    # shutil.copyfile(os.path.join(path, filename), dirname)
                except FileNotFoundError as exc:
                    continue
                else:
                    # shutil.copyfile(
                    #     os.path.join(new_path, filename.replace("mp3", "pdf")),
                    #     dirname.replace("mp3/", ""))
                    try:
                        shutil.move(
                            os.path.join(new_path,
                                         filename.replace("mp3", "pdf")),
                            dirname.replace("mp3/", ""))
                    except FileNotFoundError as exc:
                        with open(
                                "G:/Wookoo_double/VideoToBook/raw_pdf/local.txt",
                                "w",
                                encoding="utf-8") as fn:
                            fn.write(filename.replace("mp3", "pdf"))


def main_new():
    raw_path = "D:/Wook/Tool/VideoToBook.cn/VTBStart/Library/Preference/user/leolu/vtb/"
    new_path = "G:/Wookoo_double/VideoToBook/raw_pdf/"

    for value in os.listdir(new_path):
        for root, _, files in os.walk(raw_path):
            for filename in files:
                if filename == value.replace(".pdf", ".mp3"):
                    dirname = os.path.join(
                        new_path, "{}/{}/mp3/".format(
                            root.split("/")[-1],
                            filename.split(".")[0]))
                    try:
                        os.makedirs(dirname)
                    except FileExistsError as exc:
                        pass
                    except FileNotFoundError:
                        continue

                    shutil.move(os.path.join(root, filename), dirname)
                    try:
                        shutil.move(
                            os.path.join(new_path, filename.replace("mp3", "pdf")),
                            dirname.replace("mp3/", ""))
                    except FileNotFoundError:
                        continue


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main_new()