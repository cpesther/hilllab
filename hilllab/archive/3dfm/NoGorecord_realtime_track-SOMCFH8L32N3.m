% Christopher Esther, Hill Lab, 9/26/2025

function [] = record_realtime_track(path, video_number, camera, total_frames, fps, timeout_seconds)
% RECORD_REALTIME_TRACK Capture and track particles in near real-time using
% a PointGrey Flea3 camera.
%
% This function captures video from a PointGrey Flea3 camera, sends frames 
% to a Python script for near real-time particle tracking, displays the 
% annotated video, and savesthe raw frames to an .avi file at the path.
% Some of this code is based on the standard video recording function. 
%
% ARGUMENTS:
% path (string): Folder path where the .avi video should be saved.
%
% video_number (int, optional): Number appended to the first video's 
% filename. Automatically increments. Default is 1.
%
% camera (string, optional): The camera being used. Determines which video
% format can be used. Defaults to 'GS3'. Other valid values is 'FL3'.
%
% total_frames (int, optional): Number of frames to record per video. 
% Default is 1800.
%
% fps (int, optional): Frames per second. Must be 15, 30, or 60. 
% Default is 60.
%
% timeout_seconds (int, optional): Maximum allowed runtime in seconds 
% before timing out. Default is 60.

% Set default arguments if not provided
if nargin < 2 || isempty(video_number)
    video_number = 1;
end

if nargin < 3 || isempty(camera)
    camera = 'GS3';
end

if nargin < 4 || isempty(total_frames)
    total_frames = 1200;
end

if nargin < 5 || isempty(timeout_seconds)
    timeout_seconds = 90 * total_frames / 1200;
end

if nargin < 6 || isempty(fps)
    fps = 60;
end

% Set the correct video format depending on the camera used
if strcmp(camera, 'GS3')
    video_format = 'F7_Raw8_2448x2048_Mode0';
elseif strcmp(camera, 'FL3')
    video_format = 'F7_Raw8_1280x1024_Mode0';
else
    error('Unsupported camera type: %s', camera);
end

% Extract frame size from the format string
tokens = regexp(video_format, '_(\d+)x(\d+)_', 'tokens');
dims = str2double(tokens{1});  % dims = [width height]
height = dims(2);
width  = dims(1);

%% --------------------------
% Memory-mapped file setup
%% --------------------------
folderPath = fileparts(path);  % folder containing the video
max_frames = total_frames;

% --- Raw grayscale frames ---
raw_file = fullfile(folderPath,'shared_frame_raw.bin');

% Preallocate file for all frames
fid = fopen(raw_file,'w');
fwrite(fid, zeros(height*width,max_frames,'uint8'),'uint8');
fclose(fid);

raw_map = memmapfile(raw_file, ...
    'Format', {'uint8', [height width max_frames], 'frames'}, ...
    'Writable', true);

% --- Metadata arrays (frame number + timestamp) ---
frame_numbers = int32(zeros(max_frames,1));
timestamps    = zeros(max_frames,1);

% --- Annotated frames (RGB) ---
annot_file = fullfile(folderPath,'shared_frame_annot.bin');

fid = fopen(annot_file,'w');
fwrite(fid, zeros(height*width*3,max_frames,'uint8'),'uint8');
fclose(fid);

annot_map = memmapfile(annot_file, ...
    'Format', {'uint8', [height width 3 max_frames], 'frames'}, ...
    'Writable', true);

%% --------------------------
% Video capture setup
%% --------------------------
vid = videoinput('pointgrey', 1, video_format);
src = getselectedsource(vid);
src.FrameRate = fps;

vid.FramesPerTrigger = 1;       % grab one frame at a time
vid.LoggingMode = 'disk&memory';

diskLogger = VideoWriter([path sprintf('_%04d', video_number) '.avi'], 'Grayscale AVI');
diskLogger.FrameRate = fps;
vid.DiskLogger = diskLogger;

preview(vid);
running = true;
frame_idx = 1;
start_time = tic;

%% --------------------------
% Recording loop (real-time frames)
%% --------------------------
preview(vid);       % open live preview
disp('Press Y to start recording, N to exit');

str = input('Take video? Y/N [Y]: ','s');
if isempty(str), str = 'Y'; end

if strcmpi(str,'y')
    start(vid);                % start acquisition
    start_time = tic;
    frame_idx = 1;

    while frame_idx <= total_frames
        frame = getsnapshot(vid);
        gray  = im2gray(frame);

        % --- Write raw frame to memmap ---
        raw_map.Data.frames(:,:,frame_idx) = gray;

        % --- Save metadata ---
        frame_numbers(frame_idx) = int32(frame_idx);
        timestamps(frame_idx)    = toc(start_time);

        frame_idx = frame_idx + 1;
    end

    stop(vid);                 % stop acquisition
    disp('Recording finished.');

else
    disp('Exiting without recording.');
end

%% --------------------------
% Cleanup
%% --------------------------
try
    closepreview(vid);
catch
    % ignore if preview already closed
end

imaqreset;

% Save metadata
save(fullfile(folderPath,'frame_metadata.mat'),'frame_numbers','timestamps');

%% --------------------------
% Cleanup
%% --------------------------
closepreview(vid);
imaqreset;
