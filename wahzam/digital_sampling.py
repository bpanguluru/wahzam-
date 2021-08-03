# Creating functions for converting all variety of audio recordings, 
# be them recorded from the microphone or digital audio files, into a 
# NumPy-array of digital samples. (Nicholas Won)

import numpy as np
from microphone import record_audio
import librosa
import pathlib

def micsample(listentime):
    """
    Uses the microphone to record audio and returns a numpy array
    of digital samples

    Parameters
    ----------
    listentime : float
        length of recording in seconds
        
    Returns
    -------
    (samples, times) : Tuple[ndarray, ndarray]
        the shape-(N,) array of samples and the corresponding shape-(N,) array of times
    """
    frames, sampling_rate = record_audio(listentime)
    samples = np.hstack([np.frombuffer(i, np.int16) for i in frames])
    times = np.arange(samples.size) / sampling_rate
    return samples, times

def filesample(filename, cliptime):
    """
    Uses librosa to read in audio samples from a sound file and returns
    a numpy array of digital samples

    Parameters
    ----------
    filename : string 
        file name of audio file to be analyzed

    cliptime : float
        duration of file to sample from
        
    Returns
    -------
    (samples, times) : Tuple[ndarray, ndarray]
        the shape-(N,) array of samples and the corresponding shape-(N,) array of times
    """
    p = pathlib.Path(filename)
    filepath = str(p.absolute())
    samples, sampling_rate = librosa.load(filepath, sr=44100, mono=True, duration=cliptime)
    times = np.arange(samples.size) / sampling_rate
    return samples, times

# OPTIONAL
# def foldersample(foldername, cliptimes)

# OPTIONAL
# Creating a function that can take an array of audio samples from 
# a long (e.g. one minute) recording and produce a random clip of it 
# at a desired, shorter length. This can help with experimentation/analysis. 
# def randomsplice(samples, times, length):
    """
    description

    Parameters
    ----------
    samples : ndarray
        the shape-(N,) array of samples
        
    times : ndarray
        the shape-(N,) array of times

    length : int
        the desired shorter length of the random clip

    Returns
    -------
    """
#   numpy to get random splice dimensions
#   splice both samples and times
#   return spliced_samples, spliced_times
