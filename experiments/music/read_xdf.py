import pyxdf
streams, fileheader = pyxdf.load_xdf("./experiments/music/data/session_2022-03-02_20-18-29.xdf")
print(streams)