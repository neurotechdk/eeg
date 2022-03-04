# Middleware to read EEG data from the EEG device
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations


class EEG(object):
  def __init__(self, dummyBoard = False):
    self.params = BrainFlowInputParams()
    if(dummyBoard):
      self._prepare_dummy_board()
    else:
      self._prepare_board()
    self.exg_channels = BoardShim.get_exg_channels(self.board_id)
    self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
    self.window_size = 4
    self.num_points = self.window_size * self.sampling_rate

    self.start_stream()

    # self.app = QtGui.QApplication([])
    # self.win = pg.GraphicsWindow(title='BrainFlow Plot',size=(800, 600))

    # self._init_timeseries()

    # timer = QtCore.QTimer()
    # timer.timeout.connect(self.update)
    # timer.start(self.update_speed_ms)
    # QtGui.QApplication.instance().exec_()

  def start_stream(self):
    self.board.prepare_session()
    self.board.start_stream()
    
  def _prepare_board(self):
    self.params.serial_port = 'COM3'
    self.board_id = 2  # cyton daisy
    self.update_speed_ms = 50
    self.board = BoardShim(self.board_id, self.params)

  def _prepare_dummy_board(self):
    self.board_id = BoardIds.SYNTHETIC_BOARD.value
    self.board = BoardShim(self.board_id, self.params)
    self.update_speed_ms = 50

  def _init_timeseries(self):
    self.plots = list()
    self.curves = list()
    for i in range(len(self.exg_channels)):
      p = self.win.addPlot(row=i,col=0)
      p.showAxis('left', False)
      p.setMenuEnabled('left', False)
      p.showAxis('bottom', False)
      p.setMenuEnabled('bottom', False)
      if i == 0:
          p.setTitle('TimeSeries Plot')
      self.plots.append(p)
      curve = p.plot()
      self.curves.append(curve)

  def update(self):
    data = self.board.get_current_board_data(self.num_points)
    for count, channel in enumerate(self.exg_channels):
      # DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
      DataFilter.perform_lowpass(data[channel], self.sampling_rate, 49.0, 1,
          FilterTypes.BUTTERWORTH.value, 0)
      self.curves[count].setData(data[channel].tolist())
  
  def tag(self, tag:int):
    self.board.insert_marker(tag)

  def stop(self):
    if self.board.is_prepared():
      self.board.release_session()
      self.board.stop_stream()