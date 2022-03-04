from middleware.eeg import EEG

streamer = None
try:
  streamer = EEG(dummyBoard=False)
except BaseException as e:
  print("Error: Could not initialize EEG streamer")
  print(e)
finally:
  if streamer is not None:
    streamer.destroy()
