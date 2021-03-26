from vismap import Canvas, MercatorTransform
from vismap.tile_providers import Mapnik

import vispy.scene.visuals as visuals
from vispy import app
import numpy as np

import pandas as pd

# -----------------------------------------------------------------------------
# Glumpy / Qt5 integration example (c) LeMinaw, 2020
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------

import numpy as np
from glumpy import app as glumpy_app
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QTextEdit


glumpy_app.use("qt5")
glumpy_window = glumpy_app.Window()

qwindow = QMainWindow()
widget = QWidget()
button = QPushButton("Press me!")
text = QTextEdit()
qwindow.setCentralWidget(widget)
widget.setLayout(QVBoxLayout())
widget.layout().addWidget(text)
widget.layout().addWidget(button)


c = Canvas(tile_provider=Mapnik())
c.show()

df = pd.read_csv("../data/business-locations-us.txt", sep="\t")
df["fldHeading"] = df["fldHeading"].replace(np.nan, 'NAN_CATEGORY_MISSING', regex=True)

N = int(1e9)
C = list(df.fldBusinessName)[:N]

# points = visuals.Marker(np.array_equal)
points = visuals.Markers(
                    parent=c.view.scene)
@button.clicked.connect
def on_click():
    category = text.toPlainText().strip()
    mask = df["fldHeading"].str.contains(category)
    sub_df = df[mask]
    P = np.zeros((min(sub_df.shape[0], N), 2))
    P[:, 0] = sub_df.fldLng.values[:N]
    P[:, 1] = sub_df.fldLat.values[:N]

    points.set_data(P, face_color="lightblue")
# line = visuals.Line(np.array([[-97.4395, 35.2226], [-97.5164, 35.4676]]),
#                     parent=c.view.scene)

# line.transform = MercatorTransform()  # the magic line!
points.transform = MercatorTransform()  # the magic line!

qwindow.show()
glumpy_app.run()
app.run()



