# Simple Python Project Template

The basics of creating an installable Python package.

To install this package, in the same directory as `setup.py` run the command:

```shell
pip install -e .
```

This will install `example_project` in your Python environment. You can now use it as:

```python
from example_project import returns_one
from example_project.functions_a import hello_world
from example_project.functions_b import multiply_and_sum
```

To change then name of the project, do the following:
   - change the name of the directory `example_project/` to your project's name (it must be a valid python variable name, e.g. no spaces allowed)
   - change the `PROJECT_NAME` in `setup.py` to the same name
   - install this new package (`pip install -e .`)

If you changed the name to, say, `my_proj`, then the usage will be:

```python
from my_proj import returns_one
from my_proj.functions_a import hello_world
from my_proj.functions_b import multiply_and_sum
```

You can read more about the basics of creating a Python package [here](https://www.pythonlikeyoumeanit.com/Module5_OddsAndEnds/Modules_and_Packages.html).


# Planning

### digital_sampling.py
   1. [TESTED] Function to use Mic to record data in form of NumPy array (Day 1, WorkingWithMic)
      * Takes in listenduration
      * Uses microphone record_audio with listenduration to get frames, samplingrate
      * Uses np.hstack on frames to join frames in a single array of digital samples
      * Calculates respective times
      * Return digital samples and times
   2. [TESTED] Function to convert any audio file to NumPy-array of digital samples (Day 1, AnalogToDigital)
      * Takes in file name and clipduration
      * Pathlib uses file name to find file path, stored as string
      * Uses librosa.load with filepath/samplerate/mono/duration to get samples, samplingrate
      * Calculates respective times
      * Returns digital samples and times

### find_peaks.py
   1. [TESTED] Function to make Spectrogram (Day 3 Notebook: Spectrogram + Day
    2 Notebook: DFT)
      * takes in digital samples
      * does fourier transforms
      * gets spectogram np array
   2. Function to find the peaks (Day 3 Notebook: Peak_finding + Day 2 Notebook: DFT) 
      * make binary structure
      * threshold (for each audio input)
      * use provided peak-finding function to return peak indices
      * will return list of tuples of indices of peaks (call indices)

### fingerprint.py
   1. [TESTED] findsfingerprints(indices, spectrogram)
      - (I think) neighborhood -> localpeaklocation -> _peaks() -> fingerprints
         NOTE: return list of fingerprint tuples and list of time values corresponding to each peak given, returned in the order the peaks are given, takes in list of peak indices ordered by column major
      - tested on small test case

### databases.py
Database Schemes
   # fingerprint_database = {<fingerprint>:[(intID, time), (intID, time)...]}
   # artist_database = {<intID>:<songInfo>, <intID>:<songInfo>}

   1. [TESTED] store_fingerprints(abs_times, fingerprints, fingerprint_database, songid)
      given a list of fingerprints, maps fingerprint to a tuple song id and absolute time
      calls the function to store song info to insert id and info into song info database
         (note: gets songid from add_artist_info)
   2. [TESTED] load_dictionary(file_path):
      loads a dictionary from a Pickle file
   3. [TESTED] save_dictionary(dict, file_path):
      saves a dictionary to a Pickle file
   4. [TESTED] add_artist_info(song, artist, artist_database): 
      Creating a unique string id, corresponds this id to the song name and artist name,
      adds this information to the song_info database, and returns the song id
   5. [TESTED] add_song(fingerprints, abs_times, name, artist, artist_database, fingerprint_database)
      adds song information to both the fingerprint and song info database
   10. [TESTED] get_id(fingerprint, fingerprint_database)
      returns all songids and absolute times associated with fingerprint
   13. [TESTED] most_frequent(somelist)
      this is needed to count which tuple most common in the give_matched_songid(), need the Counter import
   14. [TESTED] give_matched_songid(fingerprintslist, fingerprint_database, timeslist)
      Takes in list of fingerprints, the database for them, and the list of times corresponding to the beginning of each fingerprint
         Returns the songid (first term in the tuple)

   1. delete_song(name, artist, artist_database, fingerprint_database)
      deletes song information from both the fingerprint and song info databases
   2. [TESTED] delete_fingerprint_info(song_id, fingerprint_database)
      Deletes fingerprint information from the fingerprint database
   3. [TESTED] delete_artist_info(name, artist, artist_database, song_id)
      deletes song information from artist_database
   4. [TESTED] get_info(song_id, artist_database)
      Gets song metadata

-----OPTIONAL FEATURES-------
1. Finding more optimal parameters for thresholds and fanout_sizes to better match song audio to song names

2. Creating a function that can take an array of audio samples from a long (e.g. one minute) recording and produce random clips of it at a desired, shorter length. This can help with experimentation/analysis. For example you can record a 1 minutes clip of a song, played from your phone and then create many random 10 second clips from it and see if they all successfully match against your database.
   1. would need to convert audio samples to digital (function in day1/step 1)
   2. random slices with numpy

3. Recording long clips of songs under various noise conditions (e.g. some should be clips from studio recordings, others recorded with little background noise, some with moderate background noise, etc.) so that you can begin to test and analyze the performance of your algorithm.

4. Writing a sampling function to handle a folder full of .mp3 files