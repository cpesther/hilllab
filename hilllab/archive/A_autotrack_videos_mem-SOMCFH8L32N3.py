# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:40:34 2019

@author: Administrator
"""

# New version created by Christopher Esther on 7/18/2025 with memory allocation implemented
# to find the pesky memory leak(s) causing us issues.

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3



record_snapshot(breakpoint='importstart')

def autotrack_videos(exp_dir, save_dir, bead_sz = 21, frac_vid_len = 1.0, frame_dist = 5, mem = 0):

    write_log('Start of function')
    import tracemalloc  # for capturing memory snapshots
    tracemalloc.start()  # start memory monitoring

    import scipy.io as sio
    import os
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    # Optionally, tweak styles.
    mpl.rc('figure',  figsize=(10, 5))
    mpl.rc('image', cmap='gray')
    
    import numpy as np
    import pandas as pd
    from pandas import DataFrame, Series  # for convenience
    
    import pims
    from pims import Frame
    import trackpy as tp
    import time
    
    try:
        from tkinter import Tk
        from tkFileDialog import askdirectory
    except:
        from tkinter import Tk
        from tkinter import filedialog

    write_log('Finished imports')
    
    @pims.pipeline
    def gray(image):
        return image[:, :, 1]  # Take just the green channel
    
    print('Beginning batch process!')
    write_log('Beginning batch process')

    record_snapshot(breakpoint='start')
    start_time = time.time() # Start a timer for the whole batch

    # Crawl through every subdirectory in exp_dir
    flist =[] # array of obnoxiously long, full filenames
    fnames = [] # array of the individual movie names
    nfiles = 0 # count how many videos are to be processed

    print('Walking folders...')
    write_log('Walking folders')

    for root, dirs, files in os.walk(exp_dir):
        for file in files:
            if file.endswith(".avi"):
                flist.append(os.path.join(root,file))
                fnames.append(file)
                nfiles=nfiles+1

    print('Found '+str(nfiles)+' Videos!')
    write_log('Done walkign folders')
    record_snapshot(breakpoint='postwalk')

    fname_ind = 0

    print('Iterating on files...')
    write_log('Iterating on files')
    for fname in flist:
        
        write_log(f'Processing {fname}')
        record_snapshot(breakpoint='itstart')

        print('Extracting frames...')

        frames = gray(pims.PyAVReaderIndexed(fname))
        fv = [frames[fr] for fr in range(len(frames))]

        track_time = time.time()
        print('Starting tracking...')
        write_log(f'Started tracking {fname}')

        f = tp.batch(fv, bead_sz, minmass = 750*(bead_sz/21)**3, processes = 14)  # heres the main operative line
        print("--- %s seconds to track ---" % (time.time() - track_time))
        write_log(f'Finished tracking {fname}')

        try:
            t = tp.link(f,frame_dist, memory=mem)
        except RuntimeError:
            print("Likely no beads in this video")
            continue
        
        print('Filtering...')
        write_log(f'Filtering t1 {fname}')


        t1 = tp.filter_stubs(t,len(frames)*frac_vid_len)

        print('Before: ', t['particle'].nunique())
        print('After: ', t1['particle'].nunique())

        t2 = t1[((t1['mass'] < 35000) & (t1['size'] < 7.5*(bead_sz/21)) & (t1['size'] > 3.5*(bead_sz/21)) & (t1['ecc'] < 0.3))]
#        t2 = t1[(t1['mass'] > 6000*(bead_sz/21)**3) & (t1['size'] < 6.7*(bead_sz/21))]
        
        
        write_log(f'Filtering t3 {fname}')

        t3 = tp.filter_stubs(t2,len(frames)*frac_vid_len)

        print('Converting and exporting...')

        # Take the trackpy DataFrames and make them into .vrpn.mat files
        write_log(f'Extracting trackpy DFs for {fname}')

        nparts = len(t3['particle'].unique())
        vrpn_out = np.zeros((len(frames)*nparts,10))
        k=0
        jj=0

        # Make a structure that looks like the VRPNs from SpotTracker
        write_log(f'Building VRPN for {fname}')

        for i in t3['frame'].unique():
            for  j in t3['particle'].unique():
                try:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, t3[t3['particle']==j]['x'][i], t3[t3['particle']==j]['y'][i], 0, 0, 0, 0]
                except KeyError:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, np.NAN, np.NAN, 0, 0, 0, 0]
                k=k+1
                jj = jj+1
            jj=0

        write_log(f'Collecting final info for {fname}')

        info = {'vrpnLogToMatlabVersion':'05.00','matOutputFileName':fname+'.vrpn.mat'}
        spot3DSecUsecIndexFramenumXYZRPY = vrpn_out

        tracking = {'info':info, 'spot3DSecUsecIndexFramenumXYZRPY':vrpn_out}
        vrpn = {'tracking':tracking}

        write_log(f'Saving results for {fname}')

        # Now save that data structure as a .vrpn.mat file
        filename = fnames[fname_ind]
        full_name = save_dir+'/'+filename[:-4]+'.vrpn.mat'
        sio.savemat(full_name, vrpn, long_field_names=True)
        print('Saved '+filename+' to '+full_name)
        fname_ind = fname_ind+1
        print("--- %s seconds to track and save ---" % (time.time() - track_time))

        write_log(f'Finished processing for {fname}')

        record_snapshot(breakpoint='itend')


    record_snapshot(breakpoint='end')
    write_log(f'End of function {fname}')

    print("--- %s seconds to process %s videos ---" % (time.time() - start_time, fname_ind+1))
    
def autotrack_CASA(exp_dir, save_dir, bead_sz = 21, frac_vid_len = 1.0, frame_dist = 12, mem = 3, sperm=False):

    import scipy.io as sio
    import os
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    # Optionally, tweak styles.
    mpl.rc('figure',  figsize=(10, 5))
    mpl.rc('image', cmap='gray')
    
    import numpy as np
    import pandas as pd
    from pandas import DataFrame, Series  # for convenience
    
    import pims
    from pims import Frame
    import trackpy as tp
    import time
    
    try:
        from tkinter import Tk
        from tkFileDialog import askdirectory
    except:
        from tkinter import Tk
        from tkinter import filedialog
    
    @pims.pipeline
    def gray(image):
        return image[:, :, 2]  # Take just the blue channel
    
    print('Beginning batch process!')
    start_time = time.time() # Start a timer for the whole batch

    # Crawl through every subdirectory in exp_dir
    flist =[] # array of obnoxiously long, full filenames
    fnames = [] # array of the individual movie names
    nfiles = 0 # count how many videos are to be processed

    for root, dirs, files in os.walk(exp_dir):
        for file in files:
            if file.endswith(".mp4") or file.endswith(".avi"):
                flist.append(os.path.join(root,file))
                fnames.append(file)
                nfiles=nfiles+1

    print('Found '+str(nfiles)+' Videos!')

    fname_ind = 0

    for fname in flist:

        frames = gray(pims.PyAVReaderIndexed(fname))
        fv = [frames[fr] for fr in range(len(frames))]
#        v = tp.locate(fv[0], bead_sz, minmass = 3500)

        track_time = time.time()
        f = tp.batch(fv, bead_sz, minmass = 750*(bead_sz/21)**3, processes = 14)
        print("--- %s seconds to track ---" % (time.time() - track_time))
        
        if sperm & (frac_vid_len==1.0):
            frame_dist = 35
            mem=2
            frac_vid_len = 0.1
            print('Sperm flag set to true. Minimum trajectory length set to 10% of video length')
        
        try:
            t = tp.link(f[~((f['y']>490)&(f['x']<220))],frame_dist, memory=mem)
        except (RuntimeError, SubnetOversizeException) as e:
            print("Likely no beads in this video")
            continue
        
        t1 = tp.filter_stubs(t,len(frames)*frac_vid_len)

        print('Before: ', t['particle'].nunique())
        print('After: ', t1['particle'].nunique())
        
        if sperm:
            t2 = t1[((t1['mass'] < 35000) & (t1['size'] < 9.5*(bead_sz/21)) & (t1['size'] > 2.0*(bead_sz/21)) & (t1['ecc'] < 0.5))]
        else:
            t2 = t1[((t1['mass'] < 35000) & (t1['size'] < 7.5*(bead_sz/21)) & (t1['size'] > 2.5*(bead_sz/21)) & (t1['ecc'] < 0.3))]
#        t2 = t1[(t1['mass'] > 6000*(bead_sz/21)**3) & (t1['size'] < 6.7*(bead_sz/21))]
        t3 = tp.filter_stubs(t2,len(frames)*frac_vid_len)

        # Take the trackpy DataFrames and make them into .vrpn.mat files
        nparts = len(t3['particle'].unique())
        vrpn_out = np.zeros((len(frames)*nparts,10))
        k=0
        jj=0

        # Make a structure that looks like the VRPNs from SpotTracker
        for i in t3['frame'].unique():
            for  j in t3['particle'].unique():
                try:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, t3[t3['particle']==j]['x'][i], t3[t3['particle']==j]['y'][i], 0, 0, 0, 0]
                except KeyError:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, np.NAN, np.NAN, 0, 0, 0, 0]
                k=k+1
                jj = jj+1
            jj=0

        info = {'vrpnLogToMatlabVersion':'05.00','matOutputFileName':fname+'.vrpn.mat'}
        spot3DSecUsecIndexFramenumXYZRPY = vrpn_out

        tracking = {'info':info, 'spot3DSecUsecIndexFramenumXYZRPY':vrpn_out}
        vrpn = {'tracking':tracking}


        # Now save that data structure as a .vrpn.mat file
        filename = fnames[fname_ind]
        full_name = save_dir+'/'+filename[:-4]+'.vrpn.mat'
        sio.savemat(full_name, vrpn, long_field_names=True)
        print('Saved '+filename+' to '+full_name)
        fname_ind = fname_ind+1
        print("--- %s seconds to track and save ---" % (time.time() - track_time))

    print("--- %s seconds to process %s videos ---" % (time.time() - start_time, fname_ind+1))
    
def autotrack_videos_BB(exp_dir, save_dir, bead_sz = 21, frac_vid_len = 1.0, frame_dist = 5, mem = 0):

    import scipy.io as sio
    import os
    
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    
    # Optionally, tweak styles.
    mpl.rc('figure',  figsize=(10, 5))
    mpl.rc('image', cmap='gray')
    
    import numpy as np
    import pandas as pd
    from pandas import DataFrame, Series  # for convenience
    
    import pims
    from pims import Frame
    import trackpy as tp
    import time
    
    try:
        from tkinter import Tk
        from tkFileDialog import askdirectory
    except:
        from tkinter import Tk
        from tkinter import filedialog
    
    @pims.pipeline
    def gray(image):
        return image[:, :, 1]  # Take just the green channel
    
    print('Beginning batch process!')
    start_time = time.time() # Start a timer for the whole batch

    # Crawl through every subdirectory in exp_dir
    flist =[] # array of obnoxiously long, full filenames
    fnames = [] # array of the individual movie names
    nfiles = 0 # count how many videos are to be processed

    for root, dirs, files in os.walk(exp_dir):
        for file in files:
            if file.endswith(".avi"):
                flist.append(os.path.join(root,file))
                fnames.append(file)
                nfiles=nfiles+1

    print('Found '+str(nfiles)+' Videos!')

    fname_ind = 0

    for fname in flist:

        frames = gray(pims.PyAVReaderIndexed(fname))
        fv = [frames[fr] for fr in range(len(frames))]

        track_time = time.time()
        f = tp.batch(fv, bead_sz, minmass = 750*(bead_sz/21)**3, processes = 14)
        print("--- %s seconds to track ---" % (time.time() - track_time))
        
        try:
            t = tp.link(f,frame_dist, memory=mem)
        except RuntimeError:
            print("Likely no beads in this video")
            continue
        
        t1 = tp.filter_stubs(t,len(frames)*frac_vid_len)

        print('Before: ', t['particle'].nunique())
        print('After: ', t1['particle'].nunique())

        t2 = t1[((t1['mass'] < 35000) & (t1['size'] < 7.5*(bead_sz/21)) & (t1['size'] > 3.5*(bead_sz/21)) & (t1['ecc'] < 0.3))]
#        t2 = t1[(t1['mass'] > 6000*(bead_sz/21)**3) & (t1['size'] < 6.7*(bead_sz/21))]
        t3 = tp.filter_stubs(t2,len(frames)*frac_vid_len)

        # Take the trackpy DataFrames and make them into .vrpn.mat files
        nparts = len(t3['particle'].unique())
        vrpn_out = np.zeros((len(frames)*nparts,10))
        k=0
        jj=0

        # Make a structure that looks like the VRPNs from SpotTracker
        for i in t3['frame'].unique():
            for  j in t3['particle'].unique():
                try:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, t3[t3['particle']==j]['x'][i], t3[t3['particle']==j]['y'][i], 0, 0, 0, 0]
                except KeyError:
                    vrpn_out[k,:] = [1.4613e9, 123456, jj, i, np.NAN, np.NAN, 0, 0, 0, 0]
                k=k+1
                jj = jj+1
            jj=0

        info = {'vrpnLogToMatlabVersion':'05.00','matOutputFileName':fname+'.vrpn.mat'}
        spot3DSecUsecIndexFramenumXYZRPY = vrpn_out

        tracking = {'info':info, 'spot3DSecUsecIndexFramenumXYZRPY':vrpn_out}
        vrpn = {'tracking':tracking}


        # Now save that data structure as a .vrpn.mat file
        filename = fnames[fname_ind]
        full_name = save_dir+'/'+filename[:-4]+'.vrpn.mat'
        sio.savemat(full_name, vrpn, long_field_names=True)
        print('Saved '+filename+' to '+full_name)
        fname_ind = fname_ind+1
        print("--- %s seconds to track and save ---" % (time.time() - track_time))

    print("--- %s seconds to process %s videos ---" % (time.time() - start_time, fname_ind+1))


record_snapshot(breakpoint='importend')
