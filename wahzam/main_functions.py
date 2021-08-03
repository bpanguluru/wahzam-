# Assembled functions to be used in the final sound-recognition program,
# distinguishes the different processes involved with sound-recognition

import numpy as np
from microphone import record_audio
import librosa
import pathlib
import pickle
from collections import Counter

from .databases import *
from .find_peaks import *
from .fingerprint import *
from .digital_sampling import *

def digital_sample():
    """
    Prompts the user for a file or microphone recording to be used in populating/querying the database

    Parameters
    ----------
    None 

    Returns
    ------
    (samples, times) : Tuple[ndarray, ndarray]
        The shape-(N,) array of samples and the corresponding shape-(N,) array of times
    """
    recording_type = int(input("Enter 0 to load an audio file, Enter 1 to record from the microphone: "))
    samples = np.array([])
    times = np.array([])
    # Audio File Sample
    if recording_type == 0:
        filename = input("What's the name of the desired audio file? (Include file extension): ")
        cliptime = int(input("How many seconds should the audio file be sampled for? "))
        samples, times = filesample(filename, cliptime)
    # Microphone Recording Sample
    elif recording_type == 1:
        listentime = int(input("How many seconds should the microphone record? "))
        samples, times = micsample(listentime)
    # Invalid Option
    else:
        print("Error: Invalid Option")  
    return samples, times

def initialize_database():
    """
    Initalizes a dictionary database 

    Parameters
    ----------
    None
    
    Returns
    ------
    database : dict
        initialized database
    """
    database = {}
    dictionary_type = int(input("Enter 0 to input a pickled dictionary, Enter 1 to have it initialized: "))
    # Pickled Dictionary
    if dictionary_type == 0:
        file_path = input("Enter the file path and file name to the dictionary: ")
        database = load_dictionary(file_path)
    # We initialized 
    elif dictionary_type == 1:
        pass
    # Invalid Option
    else:
        print("Error: Invalid Option") 
    return database
    
def query_database(samples, times, fingerprint_database, artist_database, amp_min_percent = 75, cutoff = 20): 
    """
    Finds spectrogram, peaks, and fingerprints from given digital sample and returns final song ID

    Parameters
    ----------
    samples : ndarray
        the shape-(N,) array of samples
        
    times : ndarray
        the shape-(N,) array of times
        
    Returns
    ------
    final_song_info : Tuple(string, string)
        the artist & song name guessed by wahzam
    """
    # Empty check
    if(samples.size == 0 or times.size == 0):
        return tuple()
    # Make spectrogram
    spectrogram = make_spectogram(samples, times)
    # Find peaks
    peak_indices = local_peak_locations(spectrogram, amp_min_percent, cutoff)
    # Find fingerprints
    prints, init_times = findsfingerprints(peak_indices, fanoutsize = 15)
    # Get song id and song info from databases, return guesses song
    final_song_id = give_matched_songid(prints, fingerprint_database, init_times)
    final_song_info = get_info(final_song_id, artist_database)
    return final_song_info

def populate_database(songname, artistname, samples, times, fingerprint_database, artist_database, amp_min_percent = 75, cutoff = 20):
    """
    Populate the dictionary database 

    Parameters
    ----------
    fingerprints: List
        list of the fingerprints from the song
    abs_times: List  
        list of the absolute times, each of which corresponds to a fingerprint at the same index
    name: string
        song name
    artist: string
        artist name
    fingerprints: List
        List of each fingerprint for the song corresponding to songid
    artist_database: Dict
        Database that maps songid to artist name and song name
    fingerprint_database: dictionary
        database of the fingerprints
    
    Returns
    ------
    List[Dict]:
        The two populated databases

    """
    spec = make_spectogram(samples,times)
    peakindices = local_peak_locations(spec, amp_min_percent, cutoff)
    fingerprints, init_times = findsfingerprints(peakindices, fanoutsize = 15)
    
    #add_artist_info(songname, artistname, artist_database)
    add_song(fingerprints, init_times, songname, artistname, artist_database, fingerprint_database)
    return [artist_database, fingerprint_database]