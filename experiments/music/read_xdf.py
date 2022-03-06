from middleware.eeg import EEG, Filtering, Audio, EEGReader
from nptyping import NDArray, Float64
import numpy as np
import time
import matplotlib.pyplot as plt


eeg_data, headers = EEGReader.read_openbci_txt(file = "./experiments/music/data/OpenBCI-RAW-2022-02-22_16-32-42.txt")
print(headers)
eeg_channels_only = eeg_data.iloc[:, 1:17].to_numpy().T

filtering = Filtering(list(range(0, headers['exg_channels'] - 1)), headers['sampling_rate'])


print(eeg_channels_only.shape)


eeg_data = filtering.butterworth_lowpass(eeg_channels_only)

average_signal = np.average(eeg_data, axis=0)



resampled = Audio.resample(average_signal, headers['sampling_rate'])
print("mean amplitude: {}",np.mean(resampled))
resampled = Audio.scale_eeg_to_pcm_amp(resampled)
resampled = Audio.filter_savitzky_golay(resampled, window_size=500, order=2)
print("mean amplitude: {}",np.mean(resampled))
print("shape: {}",resampled.shape)

plt.plot(resampled)
plt.show()
