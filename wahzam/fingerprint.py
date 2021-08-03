import numpy as np

                         
def findsfingerprints(peakindices, fanoutsize = 15):
    """
        Takes in list of indices of peaks, returns list of fingerprint tuples

        Parameters
        ----------
        peakincides : List[Tuple(int, int)]
            The array of data containing the tuple indices of the peaks.
        fanoutsize : int
            Optional parameter, default of 15. How many numbers the peak in question should be compared to.

        Returns
        -------
        List[Tuple[int, int, int]]
            (fi, fj, tj-ti) index pair for each local peak location.
        List[int]
            List of time values corresponding to each fingerprint, returned in the order the peaks are given
        """

    prints = []                   #list to be filled with fingerprints
    init_times = []               #list to be filled with initial times for above fingerprints 

    for i in range(len(peakindices)):
        freq1 = peakindices[i][0]                 #frequency of peak i 
        time1 = peakindices[i][1]                 #time of peak i

        for j in range(fanoutsize):
            if ((i+j+1)<(len(peakindices))):
                freq2 = peakindices[i+j+1][0]                 #frequency of peak j, which we are comparing with peak i
                timefinal = peakindices[i+j+1][1] - time1     #relative time between peak i and j
                prints.append((freq1,freq2,timefinal))        #add tuple to prints list
                init_times.append(time1)                      #add absolute time to list containing absolute time per fingerprint
    print(len(prints))
    return prints, init_times


# testindices = [(0,1), (2,5), (3,6), (4,7),(9,9)]         #test case
# print(findsfingerprints(testindices, 3))


#the _peaks() function that generates these indices as shown in the jupyter nbs should return them already ordered by increasing row then increasing column, this function should work with that