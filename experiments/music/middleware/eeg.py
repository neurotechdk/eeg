# Middleware to read EEG data from the EEG device
import time
from typing import List, Tuple
from nptyping import NDArray, Float64
import numpy as np
from scipy.signal import savgol_filter
import sounddevice as sd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, DetrendOperations
import pyxdf
import pandas as pd

class EEG(object):
  def __init__(self, dummyBoard = False):
    self.params = BrainFlowInputParams()
    self.curves = []
    if(dummyBoard):
      self._prepare_dummy_board()
    else:
      self._prepare_board()
    self.exg_channels = BoardShim.get_exg_channels(self.board_id)
    self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
    self.window_size = 4
    self.num_points = self.window_size * self.sampling_rate

    self.start_stream()
    
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

  """Pull latest data from ringbuffer."""
  def poll(self, clear = True) -> NDArray[Float64]:
    if clear:
      return self.board.get_board_data(self.num_points)
    else:
      return self.board.get_current_board_data(self.num_points)
    
  def tag(self, tag:int):
    self.board.insert_marker(tag)

  def stop(self):
    if self.board.is_prepared():
      self.board.stop_stream()
      self.board.release_session()
      
class Filtering(object):
  def __init__(self, exg_channels, sampling_rate):
    self.exg_channels = exg_channels
    self.sampling_rate = sampling_rate

  def butterworth_lowpass(self, data: NDArray[Float64], cutoff = 49.0) -> NDArray[Float64]:
    for _, channel in enumerate(self.exg_channels):
      # DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
      print(channel)
      DataFilter.perform_lowpass(data[channel], self.sampling_rate, cutoff, 1,
          FilterTypes.BUTTERWORTH.value, 0)
    return data

class Audio(object):
  middle_c: float = 261.63
  pcm_sr: int = 44100
  attenuate: float = 0.2

  def scale_eeg_to_pcm_amp(x: NDArray[Float64], out_range=(-32767, 32767)) -> NDArray[Float64]:
    domain = np.min(x), np.max(x)
    y = (x - (domain[1] + domain[0]) / 2) / (domain[1] - domain[0])
    return y * (out_range[1] - out_range[0]) + (out_range[1] + out_range[0]) / 2
  
  def resample(x: NDArray[Float64], sr_in: int, sr_out: int = None) -> NDArray[Float64]:
    if sr_out is None:
      sr_out = Audio.pcm_sr
    return np.interp(np.arange(0, len(x), sr_in / sr_out), np.arange(0, len(x)), x)

  def play(x: NDArray[Float64]):
    sd.play(x * Audio.attenuate, Audio.pcm_sr)
    time.sleep(len(x) / Audio.pcm_sr)
  
  def smooth(x: NDArray[Float64]):
    return np.convolve(x, np.ones(5), 'same') / 5

  def filter_savitzky_golay(x: NDArray[Float64], window_size: int = 5, order: int = 2) -> NDArray:
    return savgol_filter(x, window_size, order)

class EEGReader(object):
  def parse_obci_header(file: str) -> Tuple[dict, int]:
    skip = 0
    headers = {}
    with open(file, 'rt') as f:
      for line in f:
        if not line.startswith("%"):
          break
        skip += 1
        if line.startswith("%Number of channels"):
          headers["exg_channels"] = int(line.split("=")[1])
        elif line.startswith("%Sample Rate"):
          headers["sampling_rate"] = int(line.split("=")[1][:-3]) # remove " Hz"
        elif line.startswith("%Board"):
          headers["board"] = line.split("=")[1].strip()
    return headers, skip

  def read_openbci_txt(file: str) -> Tuple[pd.DataFrame, dict]:
    headers, skip = EEGReader.parse_obci_header(file)
    return pd.read_csv(file, sep=',', header=skip), headers

  def read_xdf(file: str) -> Tuple[List[dict], dict]:
    return pyxdf.load_xdf(file)

  