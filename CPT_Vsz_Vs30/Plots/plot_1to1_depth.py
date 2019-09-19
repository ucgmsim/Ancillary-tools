import numpy as np
import matplotlib.pyplot as plt


def plot_1to1_depth(Vs30PrevFile, Vs30NewFile):
    '''
    Comparing Vs30 estimates between new model and previous model for McGann 
    Split into six groups based on their CPT determination depth
    Plots without disriminating between different surficial geologies'''
    
    fig, axes = plt.subplots(3, 2, figsize=(10, 10))
    row = 0
    col = 0
    fig.text(0.5, 0.04, 'Previous McGann Estimate of Vs30 (m/s)', ha='center')
    fig.text(0.04, 0.5, 'Current McGann Estimate of Vs30 (m/s)', va='center', rotation='vertical')    
    for k in range(len(Vs30PrevFile)):
        
        # extract the x and y points
        Vs30Prev = np.loadtxt(Vs30PrevFile[k], usecols=2)
        Vs30New = np.loadtxt(Vs30NewFile[k], usecols=0, skiprows=1)
        VsLower = np.loadtxt(Vs30NewFile[k], usecols=2, skiprows=1)
        VsUpper = np.loadtxt(Vs30NewFile[k], usecols=3, skiprows=1)

        
        # plot all points
        prev_res = Vs30Prev
        curr_res = Vs30New
        lower = VsLower
        upper = VsUpper      
        VsLowerError = curr_res - lower
        VsUpperError = upper - curr_res      
        
        
        # plot points that do not cover 1:1 line
        '''
        prev_res = np.array([])
        curr_res = np.array([])
        lower = np.array([])
        upper = np.array([])
        for i in range(len(Vs30Prev)):
            if VsLower[i]/Vs30Prev[i] > 1 or VsUpper[i]/Vs30Prev[i] < 1:
                prev_res = np.append(prev_res, Vs30Prev[i])
                curr_res = np.append(curr_res, Vs30New[i])
                lower = np.append(lower, VsLower[i])
                upper = np.append(upper, VsUpper[i])
        VsLowerError = curr_res - lower
        VsUpperError = upper - curr_res
        '''
        
        # shape an array for the error and add error - as this is a specification for the errorbar function
        error = np.zeros((2, len(prev_res)))
        error[0, 0:len(prev_res)] = VsLowerError
        error[1, 0:len(prev_res)] = VsUpperError
        
        if col < 1:
            axes[row, col].set_xlim(50, 500)
            axes[row, col].set_ylim(50, 500)
            axes[row, col].errorbar(prev_res, curr_res, yerr=error, fmt='o', markersize=3, markerfacecolor='k', elinewidth=0.5, alpha=0.5, capsize=3, color='tomato')
            axes[row, col].plot([0, 1000], [0, 1000], linestyle='solid', color='k')
            axes[row, col].text(450, 100, '({})'.format(k+1))
            col += 1
        else:
            axes[row, col].set_xlim(50, 500)
            axes[row, col].set_ylim(50, 500)
            axes[row, col].errorbar(prev_res, curr_res, yerr=error, fmt='o', markersize=3, markerfacecolor='k', elinewidth=0.5, alpha=0.5, capsize=3, color='tomato')
            axes[row, col].plot([0, 1000], [0, 1000], linestyle='solid', color='k')
            axes[row, col].text(450, 100, '({})'.format(k+1))
            col = 0
            row += 1