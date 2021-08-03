from numba import njit
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from typing import Tuple, List
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure
from mygrad import sliding_window_view


def make_spectogram(digital_samples, times):
    """
    Makes a spectogram
    
    Parameters
    ----------
    digital_samples : numpy.ndarray, shape-(H, W)
        numpy array of N audio samples
    
    
    Returns
    -------
    spectrogram:numpy.ndarray
        spectrogram is the 2-D array whose rows corresponds to frequencies and whose columns correspond to time. 
        freqs is an array of the frequency values corresponding to the rows
        times is an array of time values corresponding to the columns.
    """
   
    # The desired temporal duration (seconds) of each window of audio data
    recorded_dt = np.diff(times)[0]
    window_dt = recorded_dt  # you can adjust this value later


    # Compute the number of samples that should fit in each
    # window, so that each temporal window has a duration of `window_dt`
    # Hint: remember that the audio samples have an associated
    # sampling rate of 44100 samples per second

    # Define this as `window_size` (an int)
    # <COGINST>
    extend_factor = 1  # adjust this later for trying overlapping windows
    window_dt *= extend_factor
    window_size = int(window_dt * 44100)
    # </COGINST>

    # Using the above window size and `sliding_window_view`, create an array 
    # of non-overlapping windows of the audio data.
    # What should the step-size be so that the windows are non-overlapping?

    # Define `windowed_audio` to be a 2D array where each row contains the
    # samples of the recording in a temporal window.
    # The shape should be (M, N), where M is the number of temporal windows
    # and N is the number of samples in each window
    # <COGINST>
    windowed_audio = sliding_window_view(
        digital_samples, window_shape=(window_size,), step=window_size // extend_factor
    )

    M, N = windowed_audio.shape
    ck_for_each_window = np.fft.rfft(windowed_audio, axis=-1)
    ak_for_each_window = np.absolute(ck_for_each_window) / N
    ak_for_each_window[:, 1 : (-1 if N % 2 == 0 else None)] *= 2
    spectrogram = ak_for_each_window.T  # rows: freq, cols: time
    return spectrogram
    # ! You need to take a look at Nicholas's work and get the sampled audio from there rather than taking
    # ! Purely the recorded audio and sampling rate
    
    
    
    # S, freqs, times = mlab.specgram(
    #     recorded_audio,
    #     NFFT=4096,
    #     Fs=sampling_rate,
    #     window=mlab.window_hanning,
    #     noverlap=4096 // 2,
    #     mode='magnitude'
    # )
    #return S, freqs, times



@njit
def _peaks(
    data_2d: np.ndarray, rows: np.ndarray, cols: np.ndarray, amp_min: float
) -> List[Tuple[int, int]]:
    """
    A Numba-optimized 2-D peak-finding algorithm.
    
    Parameters
    ----------
    data_2d : numpy.ndarray, shape-(H, W)
        The 2D array of data in which local peaks will be detected.

    rows : numpy.ndarray, shape-(N,)
        The 0-centered row indices of the local neighborhood mask
    
    cols : numpy.ndarray, shape-(N,)
        The 0-centered column indices of the local neighborhood mask
        
    amp_min : float
        All amplitudes at and below this value are excluded from being local 
        peaks.
    
    Returns
    -------
    List[Tuple[int, int]]
        (row, col) index pair for each local peak location. 
    """
    peaks = []  # stores the (row, col) locations of all the local peaks

    # Iterate over the 2-D data in col-major order
    # we want to see if there is a local peak located at
    # row=r, col=c
    for c, r in np.ndindex(*data_2d.shape[::-1]):
        if data_2d[r, c] <= amp_min:
            # The amplitude falls beneath the minimum threshold
            # thus this can't be a peak.
            continue
        
        # Iterating over the neighborhood centered on (r, c)
        # dr: displacement from r
        # dc: discplacement from c
        for dr, dc in zip(rows, cols):
            if dr == 0 and dc == 0:
                # This would compare (r, c) with itself.. skip!
                continue

            if not (0 <= r + dr < data_2d.shape[0]):
                # neighbor falls outside of boundary
                continue

            # mirror over array boundary
            if not (0 <= c + dc < data_2d.shape[1]):
                # neighbor falls outside of boundary
                continue

            if data_2d[r, c] < data_2d[r + dr, c + dc]:
                # One of the amplitudes within the neighborhood
                # is larger, thus data_2d[r, c] cannot be a peak
                break
        else:
            # if we did not break from the for-loop then (r, c) is a peak
            peaks.append((r, c))
    return peaks

# # `local_peak_locations` is responsible for taking in the boolean mask `neighborhood`
# # and converting it to a form that can be used by `_peaks`. This "outer" code is 
# # not compatible with Numba which is why we end up using two functions:
# # `local_peak_locations` does some initial pre-processing that is not compatible with
# # Numba, and then it calls `_peaks` which contains all of the jit-compatible code
def local_peak_locations(data_2d: np.ndarray, amp_min_percentile = 75, cutoff = 20): #should be 20, just messin around
    """
    Defines a local neighborhood and finds the local peaks
    in the spectrogram, which must be larger than the specified `amp_min`.
    
    Parameters
    ----------
    data_2d : numpy.ndarray, shape-(H, W)
        The 2D array of data in which local peaks will be detected
    
    neighborhood : numpy.ndarray, shape-(h, w)
        A boolean mask indicating the "neighborhood" in which each
        datum will be assessed to determine whether or not it is
        a local peak. h and w must be odd-valued numbers
        
    amp_min : float
        All amplitudes at and below this value are excluded from being local 
        peaks.
    
    Returns
    -------
    List[Tuple[int, int]]
        (row, col) index pair for each local peak location.
    
    Notes
    -----
    Neighborhoods that overlap with the boundary are mirrored across the boundary.
    
    The local peaks are returned in column-major order.
    """
    #Amp Min Calculate
    data_2d = np.clip(data_2d, 1e-20, None)
    log_S = np.log(data_2d).ravel()  # flattened array
    ind = round(len(log_S) * 0.01*  amp_min_percentile)
    amp_min = np.partition(log_S, ind)[ind]
    soklasklutch = np.log(data_2d)
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, cutoff)
    rows, cols = np.where(neighborhood)
    assert neighborhood.shape[0] % 2 == 1
    assert neighborhood.shape[1] % 2 == 1

    # center neighborhood indices around center of neighborhood
    rows -= neighborhood.shape[0] // 2
    cols -= neighborhood.shape[1] // 2
    print(len(_peaks(soklasklutch, rows, cols, amp_min=amp_min)))
    return _peaks(soklasklutch, rows, cols, amp_min=amp_min)






# def local_peak_locations(data_2d: np.ndarray, neighborhood: np.ndarray, amp_min: float):
#     """
#     Defines a local neighborhood and finds the local peaks
#     in the spectrogram, which must be larger than the specified `amp_min`.
    
#     Parameters
#     ----------
#     data_2d : numpy.ndarray, shape-(H, W)
#         The 2D array of data in which local peaks will be detected
    
#     neighborhood : numpy.ndarray, shape-(h, w)
#         A boolean mask indicating the "neighborhood" in which each
#         datum will be assessed to determine whether or not it is
#         a local peak. h and w must be odd-valued numbers
        
#     amp_min : float
#         All amplitudes at and below this value are excluded from being local 
#         peaks.
    
#     Returns
#     -------
#     List[Tuple[int, int]]
#         (row, col) index pair for each local peak location.
    
#     Notes
#     -----
#     Neighborhoods that overlap with the boundary are mirrored across the boundary.
    
#     The local peaks are returned in column-major order.
#     """
#     rows, cols = np.where(neighborhood)
#     assert neighborhood.shape[0] % 2 == 1
#     assert neighborhood.shape[1] % 2 == 1

#     # center neighborhood indices around center of neighborhood
#     rows -= neighborhood.shape[0] // 2
#     cols -= neighborhood.shape[1] // 2

#     return _peaks(data_2d, rows, cols, amp_min=amp_min)



# def local_peaks_mask(data: np.ndarray, cutoff: float) -> np.ndarray:
#     """Find local peaks in a 2D array of data.

#     Parameters
#     ----------
#     data : numpy.ndarray, shape-(H, W)

#     cutoff : float
#          A threshold value that distinguishes background from foreground

#     Returns
#     -------
#     Binary indicator, of the same shape as `data`. The value of
#     1 indicates a local peak."""
#     # Generate a rank-2, connectivity-2 binary mask
#     neighborhood_mask = generate_binary_structure(2, 2)

#     # Use that neighborhood to find the local peaks in `data`.
#     # Pass `cutoff` as `amp_min` to `local_peak_locations`.
#     peak_locations = local_peak_locations(data, neighborhood_mask, cutoff)  

#     # Turns the list of (row, col) peak locations into a shape-(N_peak, 2) array
#     # Save the result to the variable `peak_locations`
#     peak_locations = np.array(peak_locations)

#     # create a mask of zeros with the same shape as `data`
#     mask = np.zeros(data.shape, dtype=bool)

#     # populate the local peaks with `1`
#     mask[peak_locations[:, 0], peak_locations[:, 1]] = 1
#     return mask