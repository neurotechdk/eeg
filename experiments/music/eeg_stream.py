from middleware.eeg import EEG, Filtering, Audio
from nptyping import NDArray, Float64
import numpy as np
import time
import matplotlib.pyplot as plt





streamer = None
try:
  streamer = EEG(dummyBoard=True)
  print("Started EEG stream. Channels: {}, sample rate: {}".format(
    len(streamer.exg_channels), streamer.sampling_rate))
  filtering = Filtering(streamer.exg_channels, streamer.sampling_rate)
  while(True):
    time.sleep(1)
    # Just do a basic lowpass
    cur_data = streamer.poll()
    print(cur_data.shape)
    eeg_data: NDArray[Float64] = filtering.butterworth_lowpass(cur_data)
    cur_datat = None
    break
  #average_signal = np.average(eeg_data, axis=0)
  print(eeg_data.shape)
  average_signal = eeg_data[15,:]

  resampled = Audio.resample(average_signal, streamer.sampling_rate)
  print("mean amplitude: {}",np.mean(resampled))
  resampled = Audio.scale_eeg_to_pcm_amp(resampled)
  print("mean amplitude: {}",np.mean(resampled))
  print("shape: {}",resampled.shape)

  plt.plot(resampled)
  plt.show()
  #plt.plot(Audio.filter_savitzky_golay(resampled, window_size=1000, order=4))
  #plt.show()
  #plt.plot(Audio.smooth(resampled))
  #plt.show()
  # Audio.play(Audio.smooth(resampled))
  time.sleep(1)
    
except BaseException as e:
  print("Error: Could not initialize EEG streamer")
  print(e)
finally:
  if streamer is not None:
    streamer.stop()
