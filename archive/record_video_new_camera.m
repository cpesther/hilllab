
function [] = record_video_new_camera(file, file_number, frames, max_time, frame_rate)

%record_video.m -- Matthew Combs 5/7/2015
%
%function [] = record_video(file, file_number, frames, max_time, frame_rate)
%
%This function will record videos in .avi format to specified file names
%with a PointGrey Flea3 camera
%
%file == file name without video number or extension
%file_number == the number to be appended to the file name of the first
%               video taken -- automatically increments, default = 1
%frames == the number of frames to be taken per video, default = 1800
%max_time == the maximum time in seconds for the video logger to run before 
%            timing out, default = 60
%frame_rate == the frame rate in frames per second -- must be 15, 30, or 60,
%              default = 60

if (nargin < 2) || isempty(file_number),  file_number = 1; end;
if (nargin < 3) || isempty(frames),  frames = 1200; end; %2500 for long videos, 1200 for normal, 600 for hurricane
if (nargin < 4) || isempty(max_time),  max_time = 90*frames/1200; end;
if (nargin < 5) || isempty(frame_rate),  frame_rate = 60; end; %10 for long videos, 60 for normal

vid = videoinput('pointgrey', 1, 'F7_Raw8_2448x2048_Mode0');
src = getselectedsource(vid);
src.FrameRate = frame_rate;%num2str(frame_rate);

vid.FramesPerTrigger = frames;

vid.LoggingMode = 'disk&memory';

diskLogger = VideoWriter([file sprintf('_%04d',file_number) '.avi'], 'Grayscale AVI');

diskLogger.FrameRate = frame_rate;

vid.DiskLogger = diskLogger;

preview(vid);

running = true;

while running
    
    prompt = 'Take video? Y/N [Y]: ';
    str = input(prompt,'s');
    if isempty(str)
        str = 'Y';
    end
    
    if strcmpi(str,'y')
        disp('Press any key when ready to record.')
        pause
%     answer = questdlg('Record new video?', ...
% 	'Options', ...
% 	'Yes','No','Yes');
%     waitfor(answer)
%     % Handle response
%     switch answer
%         case 'Yes'
        
%     f = warndlg('Acquisition Paused', 'Close to proceed');

        start(vid);

        wait(vid,max_time);

        file_number = file_number+1;

        diskLogger = VideoWriter([file sprintf('_%04d',file_number) '.avi'], 'Grayscale AVI');

        diskLogger.FrameRate = frame_rate;

        vid.DiskLogger = diskLogger;
        pause(5)
        beep
    
%         case 'No'
    elseif strcmpi(str,'n')

            disp('Exiting...')
            running = false;

    end
    
end

closepreview(vid)
imaqreset

end