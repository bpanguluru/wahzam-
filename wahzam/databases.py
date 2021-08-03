# storing song information and fingerprints in python dictionaries
import pickle
from collections import Counter
# Functions to be implemented:
#   - Compare UNKNOWN fingerprint to fingerprint database to get MATCHES

def store_fingerprints(abs_times, fingerprints, fingerprint_database, song_id):
    """
    given a list of fingerprints, maps fingerprint to a tuple song id and absolute time
    calls the function to store song info to insert id and info into song info database

    Parameters
    ----------
    abs_times: list of absolute times of fingerprints 
        the absolute times of each fingerprints
    fingerprints: list of fingerprints
        each fingerprint for the song corresponding to songid
    fingerprint_database: dictionary
        database of the fingerprints
    songid: string
        corresponding song's id
    
    Returns
    -------
    None

    Notes
    -----
    
    """

    for i in range (len(fingerprints)):
        if fingerprint_database.__contains__(fingerprints[i]):
            temptuple = (song_id, abs_times[i])
            fingerprint_database[fingerprints[i]].append(temptuple) 
        else:
            fingerprint_database[fingerprints[i]] = [(song_id, abs_times[i])] 

# Mindy's Datbase
def add_artist_info(song, artist, artist_database): # input song name, artist title
    """Creating a unique string id, corresponds this id to the song name and artist name,
    adds this information to the song_info database, and returns the song id
    
    Parameters
    ----------
    song : string
        The name of the song of the fingerprints
    
    artist : string
        The name of the artist of the song

    artist_database : dict
        A dictionary of the unique song id's corresponding to its song name and
        artist name

    Returns
    -------
    song_id : string
        The unique id of the song added to the artist_database

    Notes
    -----
    The returned song_id should be used as the song id when the fingerprint tuples
    are being saved in the store_fingerprints method
    """
    song_id = "Song" + str(len(artist_database))
    artist_database[song_id] = (song, artist)
    return song_id
    

def add_song(fingerprints, abs_times, name, artist, artist_database, fingerprint_database):
    """
    adds song information to both the fingerprint and song info databases

    Parameters
    ----------
    fingerprints: list
        list of the fingerprints from the song
    abs_times: list of absolute times of fingerprints 
        the absolute times, each of which corresponds to a fingerprint at the same index
    name: string
        song name
    artist: string
        artist name
    fingerprints: list of fingerprints
        each fingerprint for the song corresponding to songid
    artist_database: dictionary
        database that maps songid to artist name and song name
    fingerprint_database: dictionary
        database of the fingerprints
    
    Returns
    -------
    None
    
    Notes
    -----
    
    """
    song_id = add_artist_info(name, artist, artist_database)
    store_fingerprints(abs_times, fingerprints, fingerprint_database, song_id)

def delete_song(name, artist, artist_database, fingerprint_database):
    """
    deletes song information from both the fingerprint and song info databases

    Parameters
    ----------
    name: string
        song name
    artist: string
        artist name
    fingerprints: list of fingerprints
        each fingerprint for the song corresponding to songid
    artist_database: dictionary
        database that maps songid to artist name and song name
    fingerprint_database: dictionary
        database of the fingerprints
    
    Returns
    -------
    None
    
    Notes
    -----
    
    """
    key_list = artist_database.keys()
    value_list = artist_database.values()

    index = value_list.index((name, artist))
    # find the song_id of the deleted song based on name and artist input
    song_id = key_list[index]

    # delete the song info from artist_database
    delete_artist_info(song_id, name, artist, artist_database)
    # delete the fingerprint info from fingerprint_database
    delete_fingerprint_info(song_id, fingerprint_database)

def delete_artist_info(song_id, name, artist, artist_database):
    """
    deletes song information from artist_database

    Parameters
    ----------
    song_id: string
        song_id of song that needs to be deleted
    name: string
        song name
    artist: string
        artist name
    artist_database: dictionary
        database that maps songid to artist name and song name
    
    Returns
    -------
    None
    
    Notes
    -----
    Because we use the length of the artist_database to create new song_ids,
    we must iterate through each value and replace the preceeding song info
    with the new song info to maintain the song_id order. Then, simply delete
    the last value of the dictionary.
    """
    # create list of keys from artist_database
    key_list = list(artist_database.keys())

    # iterate through indices of the key_list
    for i in range(len(key_list)):
        # check if the key at this index is equal to the song_id
        if str(key_list[i]) == song_id:
            # iterate through the last part of the for loop and begin replacing values with the values proceeding it
            for i in range(i, len(key_list) - 1):
                artist_database[key_list[i]] = artist_database[key_list[i + 1]]
        
            # delete the last element of the dictionary and break the loop
            artist_database.pop(key_list[len(key_list) - 1])
            break

def delete_fingerprint_info(song_id, fingerprint_database):
    """
    Deletes fingerprint information from the fingerprint database

    Parameters
    ----------
    song_id: string
        song_id of song that needs to be deleted   
    fingerprint_database: dictionary
        database of the fingerprints
    
    Returns
    -------
    None
    
    Notes
    -----
    As we edited the song_ids in the artist_database, this change in the song_ids 
    must be reflected in the fingerprint_database as well. If the song we want 
    deleted is located in the list of tuples following each fingerprint, it must
    be removed from the list, and if a fingerprint is only from that song, the 
    entire fingerprint can be removed.
    """
    
    # fingerprint_database = {<fingerprint>:[(songID1, time1),  (songID2, time2)...]}
    
    # iterate through every item in fingerprint_database
    key_list = list(fingerprint_database.keys())
    value_list = list(fingerprint_database.values())
    key_len = len(key_list)
    j = 0

    while j < key_len:
        i = 0
        value_len = len(value_list[j])
        # iterate through every tuple in the list of songs corresponding to each fingerprint
        while i < value_len:
            # if the song_id matches one of the song IDs of the tuples, remove it from the list
            if value_list[j][i][0] == song_id:
                del fingerprint_database[key_list[j]][i]
                value_len -= 1
            # if the number of the song_id is greater than the deleted song's song_id, subtract 1 from its value
            elif str(value_list[j][i][0]).split(" ")[1] > song_id.split(" ")[1]:
                song = ("Song " + str(int(str(value_list[j][i][0]).split(" ")[1]) - 1), value_list[j][i][1])
                del fingerprint_database[key_list[j]][i]
                fingerprint_database[key_list[j]].insert(i, song)
                i += 1
            else:
                i += 1
        
        # if the length of the list is 0, that means the list is empty and the fingerprint is unneeded
        if value_len == 0:
            del fingerprint_database[key_list[j]]

        j += 1


def get_info(song_id, artist_database):
    """
    return info
    Parameters
    ----------
    songID: string
        songID of song to get artist & song name from artist_database
    artist_database: dictionary
        database of song info
    Returns
    -------
    Tuple(string, string)
        artist & song name 
    
    Notes
    -----
    
    """
#     if not artist_database.__contains__(song_id):
#         return None
    return artist_database[song_id]
        

def get_id(fingerprint, fingerprint_database):
    """
    returns all songids and absolute times associated with fingerprint
    Parameters
    ----------
    fingerprint: Tuple[int]
        fingerprint to search for
    fingerprint_database: dictionary
        database of fingerprints
    Returns
    -------
    List[Tuple(string, int)]
        song id & absolute time for each song that has fingerprint
    
    Notes
    -----
    returns None if has no corresponding entry
    """
    if not fingerprint_database.__contains__(fingerprint):
        return None
    return fingerprint_database[fingerprint]

def load_dictionary(file_path):
    """
    loads a dictionary from a Pickle file
    Parameters
    ----------
    file_path: string
        path and name of file
    
    Returns
    -------
    dictionary 
        unpickled dictionary

    Notes
    -----
    
    """
    with open(file_path, mode = "rb") as opened_file:
        return pickle.load(opened_file)
    

def save_dictionary(dict, file_path):
    """
    saves a dictionary to a Pickle file
    Parameters
    ----------
    dict: dictionary
        dictionary to pickle
    file_path: string
        path and name of file to store dictionary to 
    Returns
    -------
    None
    
    Notes
    -----
    
    """
    with open(file_path, mode = "wb") as opened_file:
        pickle.dump(dict, opened_file)

def most_frequent(somelist):
    #this is needed to count which tuple most common in the give_matched_songid(), need the Counter import
    occurences_count = Counter(somelist)
    return occurences_count.most_common(1)[0][0]
    
def give_matched_songid(fingerprintslist, fingerprint_database, timeslist):
    """
        Takes in list of fingerprints, the database for them, and the list of times corresponding to the beginning of each fingerprint
        Returns the songid (first term in the tuple)

        Parameters
        ----------
        fingerprintslist : list
            The list of data containing all fingerprints.
        timeslist : list
            The list of data corresponding to the initial times at which each fingerprint in the fingerprintslist is taken.
        Returns
        -------
        finalsongid : string
              returns first term in tuple of (songID, time) of the most frequent occurance
        """
    final_list = []
    dictionarylist = []
    for i in range(len(fingerprintslist)):

        # check if fingerprint is in dictionary
        if fingerprintslist[i] in fingerprint_database:

            # if so, use the fingerprint as key to pull from dictionary the songids/times(in dictionary)
            dictionarylist = fingerprint_database[fingerprintslist[i]]
            # generate new list of tuples by keeping the song id, and subtracting the times(in dictionary) and the initial times (from clip fingerprint)
            #dictionary = [list(ele) for ele in dictionarylist]
            for j in range(0,len(dictionarylist),3):
                temptuple = (dictionarylist[j][0], dictionarylist[j][1] - timeslist[i])
                final_list.append(temptuple)
    # print(len(dictionarylist))

    # final_list = [(j[0],j[1]-timeslist[i]) for j in dictionarylist]
    # find which (song_id, offset time) occurs the most
    finaltuple = most_frequent(final_list)
    finalsongid = finaltuple[0]
    # print(final_list)

    return finalsongid


'''
def compare_unknown(fingerprint, fingerprint_database):
    """
    compares an unknown fingerprint to each fingerprint in the database to find the most similar fingerprint
    Parameters
    ----------
    fingerprint: List[int]
        fingerprint to search for
    fingerprint_database: dictionary
        database of fingerprints
    Returns
    -------
    Tuple(string, int)
        matching song info 
    
    Notes
    -----
    returns None if no matches
    """

    for fp in fingerprint_database.keys():
        
    return None
'''