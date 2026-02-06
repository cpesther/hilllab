# hilllab

## Autotracker Module

.. py:module:: hilllab.autotracker.autotrack_videos

.. py:function:: autotrack_videos(video_path=None, save_path=None, bead_size_pixels=21, trajectory_fraction=1.0, max_travel_pixels=5, memory=0, invert=False, performance_mode=’safe’, skip_existing=True, return_file_details=False, bypass_confirmation=False)
:module: hilllab.autotracker.autotrack_videos

Automatically processes and tracks particles in a batch of AVI
videos.

This function opens a file browser window, walks through all
subdirectories to identify AVI files, performs grayscale conversion,
detects and links particles using TrackPy, filters the results,
and saves the output as a VRPN file in the .mat format.

:type video_path: str
:param video_path: path to the folder with videos or to a single
video.
:type video_path: str
:type save_path: str
:param save_path: path to the folder where VRPNs should be saved
:type save_path: str
:type bead_size_pixels: int, optional
:param bead_size_pixels: Estimated diameter of the
particles in pixels. Default is 21.
:type bead_size_pixels: int, optional
:type trajectory_fraction: float, optional
:param trajectory_fraction: Minimum fraction of frames a
particle must appear in to be retained after filtering.
Default is 1.0.
:type trajectory_fraction: float, optional
:type max_travel_pixels: int, optional
:param max_travel_pixels: Maximum number of pixels a particle
can travel between frames for TrackPy to consider it to be
the same particle. Default is 5.
:type max_travel_pixels: int, optional
:type memory: int, optional
:param memory: Memory parameter for TrackPy’s linking,
specifying how long particles are remembered between frames.
Default is 0.
:type memory: int, optional
:type invert: bool, optional
:param invert: when false, bright spots on a dark background
will be tracked. When true, dark spots on a bright background
will be tracked.
:type invert: bool, optional
:type performance_mode: string, ‘safe’, ‘slow’, or ‘fast’
:param performance_mode: Controls
how many processes are used by TrackPy to allow this task to
be run safely in the background or sped up on demand.
:type performance_mode: string, ‘safe’, ‘slow’, or ‘fast’
:type return_file_details: bool, optional
:param return_file_details: allows the function to
return a dict containing file details useful for higher level
functions. Defaults to false.
:type return_file_details: bool, optional
:type bypass_confirmation: bool, optional
:param bypass_confirmation: when True, the function
will not ask for user confirmation of parameters before
running autotracking. Mostly used when nested in other
functions, defaults to false.
:type bypass_confirmation: bool, optional

:returns: Saves one `.vrpn.mat` file per video in `save_path`. These
contain particle position data in a structure compatible with
VRPN-based systems or legacy MATLAB tracking tools.
