from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os

app = QApplication([])
wind = QWidget()

papka_btn = QPushButton('directory')
image_list = QListWidget()
text = QLabel('image')
left_btn = QPushButton('<-')
raight_btn = QPushButton('->')
mirror_btn = QPushButton('mirror')
contrast_btn = QPushButton('contrast')
bw_btn = QPushButton('B/W')
image = QLabel('image')

main_line = QHBoxLayout()
choose_image_line = QVBoxLayout()
center_Vline = QVBoxLayout()
button_line = QHBoxLayout()

choose_image_line.addWidget(papka_btn)
choose_image_line.addWidget(image_list)
button_line.addWidget(raight_btn)
button_line.addWidget(left_btn)
button_line.addWidget(mirror_btn)
button_line.addWidget(contrast_btn)
button_line.addWidget(bw_btn)
center_Vline.addWidget(image)

center_Vline.addLayout(button_line)
main_line.addLayout(choose_image_line)
main_line.addLayout(center_Vline)
wind.setLayout(main_line)

workdir = ''
def filter():
    global workdir
    exetions_ = ['png', 'jpg', 'jpeg', 'gif', 'bmp' ]
    files = os.listdir(workdir)
    filterd_files = []
    for f in files:
        lf = f.split('.')
        for ext in exetions_:
            if ext in lf:
                filterd_files.append(f)         
    image_list.addItems(filterd_files)

def choose_Workdir():
    global workdir
    browser = QFileDialog()
    workdir = browser.getExistingDirectory()
    image_list.clear()
    filter()


class ImageProcessor:
    def __init__(self):
        self.image = None
        self.name = ''
        self.load

    def load(self):
        self.name = image_list.selectedItems()[0].text()
        self.image = Image.open(workdir + '/' + self.name)
        
    def showImage(self, path):
        image.hide()
        pixmap = QPixmap(path)
        w = image.width()
        h = image.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.show()

    def showChoosenImage(self):
        self.load()
        self.showImage(os.path.join(workdir, self.name))
    
    def saveImage(self):
        try:
            os.mkdir(os.path.join(workdir, 'Modified'))
        except FileExistsError:
            pass
        self.p_image.save(os.path.join(workdir, 'Modified', self.name))
    
    def do_bw(self):
        self.load()
        self.p_image = self.image.convert("L")
        self.saveImage()
    
    def do_mir(self):
        self.load()
        self.p_image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()

    def do_left(self):
        self.load()
        self.p_image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
    
    def do_raight(self):
        self.load()
        self.p_image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
    
    def do_contrast(self):
        self.load()
        image = ImageEnhance.Contrast(self.image)
        self.p_image = image.enhance(0.5)
        self.saveImage()

workimage = ImageProcessor()

papka_btn.clicked.connect(choose_Workdir)
image_list.itemClicked.connect(workimage.showChoosenImage)
bw_btn.clicked.connect(workimage.do_bw)
mirror_btn.clicked.connect(workimage.do_mir)
left_btn.clicked.connect(workimage.do_left)
raight_btn.clicked.connect(workimage.do_raight)
contrast_btn.clicked.connect(workimage.do_contrast)

wind.show()
app.exec_()