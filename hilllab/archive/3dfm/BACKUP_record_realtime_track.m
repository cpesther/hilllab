% Christopher Esther, Hill Lab, 9/26/2025

function [] = BACKUP_record_realtime_track(path, video_number, camera, total_frames, fps, timeout_seconds)
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

% Set up video capture with PointGrey Flea3 camera
vid = videoinput('pointgrey', 1, video_format);               % Create video input object
src = getselectedsource(vid);                                 % Get the camera source
src.FrameRate = fps;                                          % Set the frame rate

vid.FramesPerTrigger = total_frames;                          % Set number of frames per capture
vid.LoggingMode = 'disk&memory';                                   % Log frames to memory

% Set up disk logger to save video as grayscale AVI
diskLogger = VideoWriter([path sprintf('_%04d', video_number) '.avi'], 'Grayscale AVI');
diskLogger.FrameRate = fps;                                   % Match frame rate to acquisition
vid.DiskLogger = diskLogger;                                  % Attach disk logger to video object
preview(vid);                                                 % Open live preview window
running = true;                                               % Flag to control recording loop

% Here's the actual recording loop
while running

    % Prompt user
    prompt = 'Take video? Y/N [Y]: ';
    str = input(prompt, 's'); if isempty(str), str = 'Y'; end

    % If user chooses to record
    if strcmpi(str, 'y')
        disp('Press any key when ready to record.')
        pause                                % Wait for user to press a key

        start(vid);                          % Start video acquisition
        wait(vid, timeout_seconds);          % Wait until acquisition finishes or times out

        % Set up new disk logger for next video
        video_number = video_number + 1;     % Increment video counter
        diskLogger = VideoWriter([path sprintf('_%04d', video_number) '.avi'], 'Grayscale AVI');
        diskLogger.FrameRate = fps;
        vid.DiskLogger = diskLogger;

        pause(5)                             % Brief pause before next iteration
        beep                                 % Audio notification
    
    % If user chooses not to record
    elseif strcmpi(str, 'n')
        disp('Exiting...')
        running = false;                     % Exit the loop
    end

end

% Clean up video objects
closepreview(vid);                           % Close live preview window
imaqreset;                                   % Reset image acquisition hardware

end
