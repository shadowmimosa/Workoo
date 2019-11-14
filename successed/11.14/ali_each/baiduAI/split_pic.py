import os
from PIL import Image, ImageDraw, ImageFont


def classic_nine():
    filename = r'路径\美女.jpg'
    img = Image.open(filename)
    size = img.size
    print(size)

    # 准备将图片切割成9张小图片
    weight = int(size[0] // 3)
    height = int(size[1] // 3)
    # 切割后的小图的宽度和高度
    print(weight, height)

    for j in range(3):
        for i in range(3):
            box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
            region = img.crop(box)
            region.save('{}{}.png'.format(j, i))


def judge_pixel(pixels):
    black_num = 0
    if isinstance(pixels, list):
        for temp in pixels:
            if isinstance(temp, list):
                for item in temp:
                    if isinstance(item, tuple):
                        count = 0
                        for value in item:
                            count += value
                        if count / 3 < 222:
                            black_num += 1

        if black_num > 50:
            return "black"
        else:
            return "write"


def write_pic(img, coordinate):
    font = ImageFont.truetype(
        font=
        "C:\\Users\\ShadowMimosa\\Downloads\\FiraCode_1.206\\ttf\\FiraCode-Retina.ttf",
        size=30)
    draw = ImageDraw.Draw(img)
    draw.text(coordinate, ",", (51, 51, 51), font=font)
    return img


def deal_single_pic(img):
    for x in [115, 160, 200]:
        region = img.crop((x, 50, x + 45, 105))
        # region = img.crop((115, 55, 155, 100))
        # region.show()
        pixels = list(region.getdata())
        width, height = region.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

        if judge_pixel(pixels) == "write":
            return write_pic(img, (x + 10, 62))


def deal_pic():
    for dirname in ["./ali_each_orc/part1/", "./ali_each_orc/part2/"]:
        for filename in os.listdir(dirname):
            if ".png" not in filename:
                continue
            # if filename != "Snipaste_2019-10-16_11-41-27.png":
            #     continue
            # img = Image.open("./ali_each_orc/part2/Screenshot_2019-10-16-22-03-49-537_com.eg.android.AlipayGphone.png")
            img = Image.open("{}{}".format(dirname, filename))

            size = img.size

            weight = size[0]
            height = 335.5

            path = "{}{}/".format(dirname, filename.split("_")[1])
            try:
                os.mkdir(path)
            except FileExistsError:
                pass

            for i in range(int(size[1] / 335.5)):
                # i = 4
                box = (0, height * i, weight, height * (i + 1))
                region = img.crop(box)
                # if filename=="Screenshot_2019-10-16-21-52-53-195_com.eg.android.AlipayGphone.png" and i ==4:
                #     region.show()
                deal_single_pic(region).save("{}/{}.png".format(path, i))

            print(size)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    deal_pic()
