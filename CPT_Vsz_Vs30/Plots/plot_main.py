def plot_main():
    from plot_1to1_depth import plot_1to1_depth
    import os
    
    '''
    A main function to control all the plotting features
    '''
    
    # Comparing Vs30 estimates between new model and previous model for McGann
    # (split into six groups based on their CPT determination depth)
    filename1 = ['vs30cpt_5to10m.txt', 'vs30cpt_10to15m.txt', 'vs30cpt_15to20m.txt', 'vs30cpt_20to25m.txt', 'vs30cpt_25to30m.txt', 'vs30cpt_30m.txt']
    filename2 = ['McGann_5to10m.txt', 'McGann_10to15m.txt', 'McGann_15to20m.txt', 'McGann_20to25m.txt', 'McGann_25to30m.txt', 'McGann_30to999m.txt']
    Vs30PrevFile = []  # results from previous model
    Vs30NewFile = []   # results from McGann model
    for i in range(len(filename1)):
        Vs30PrevFile.append(os.path.abspath('Christchurch\\{}'.format(filename1[i])))
        Vs30NewFile.append(os.path.abspath('Christchurch\\{}'.format(filename2[i])))
    plot_1to1_depth(Vs30PrevFile, Vs30NewFile)
        

plot_main()