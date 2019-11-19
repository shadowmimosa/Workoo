class ExcelOpea(object):
    def set_style(self, name, height, bold=False, color=0):

        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = color
        font.colour_index = color
        font.height = height

        al = xlwt.Alignment()
        al.horz = 0x01  # 设置左端对齐
        al.vert = 0x01  # 设置垂直居中
        style.alignment = al

        style.font = font

        if color == 0:
            self.style = style
        else:
            self.link_style = style
            
    def init_sheet(self):
        self.wkb = xlwt.Workbook()
        self.sheet = self.wkb.add_sheet('sheet1', cell_overwrite_ok=True)

        for index, value in enumerate(self.header):
            self.sheet.write(0, index, value)

        self.row = 1

    def save(self, path):

        self.wkb.save(path)

    def write(self, content):
        self.sheet_1.write(
            self.row, 0,
                content, self.link_style)
        self.row += 1