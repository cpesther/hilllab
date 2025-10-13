%% Get Ciliary Beat Frequency from ROI
% This function calculates the ciliary beat frequency (CBF) from a video
% of cilia motion, returning the mean CBF over a region of interest (ROI),
% the CBF at each pixel, and the fraction of functional ciliated area.

function [x, xdft, xdft1, psdx] = cbfPullOnly(vidname,Fs,fthresh)
% Inputs:
%   vidname  - filename of the video
%   Fs       - sampling frequency (frames per second), default 60 fps
%   fthresh  - threshold to determine functional ciliated area, default 5 Hz
% Outputs:
%   mens_CBF - mean CBF over the selected ROI
%   px_CBF   - CBF for each pixel in the ROI
%   FFCA     - fraction of functional ciliated area

% Set default values if inputs are missing or empty
if (nargin<2) | ~isempty(Fs)
    Fs=60; % Default sampling rate 60 fps
end
if (nargin<3) | ~isempty(fthresh)
    fthresh=5; % Default threshold frequency 5 Hz
end

warning off  % Disable warnings

% Read video information
video = VideoReader(vidname);
lastF = read(video,inf);       % Read the last frame of the video
nframes = video.NumberOfFrames; % Total number of frames in video

% Define ROI (here the entire frame is used)
position = size(lastF);             % Get size of the frame
position = [1,1,position(2)-1,position(1)-1];  % Full frame ROI
roi = round(position);             % Round ROI to integer values

ys = roi(1):roi(1)+roi(3);         % Y-coordinates of ROI
xs = roi(2):roi(2)+roi(4);         % X-coordinates of ROI
video = VideoReader(vidname);      % Reopen video for reading frames

% Initialize array to store grayscale frames
k=1;
gframe = zeros(numel(xs),numel(ys),1,nframes);

% Read video frames and convert to grayscale if necessary
fprintf('loading video')
while hasFrame(video)
    vid = readFrame(video);
    if ~strcmp(video.VideoFormat,'Grayscale')
        gframe(:,:,k) = rgb2gray(vid(xs,ys,:)); % Convert RGB to grayscale
    else
        gframe(:,:,k) = vid(xs,ys,:);          % Already grayscale
    end
    k=k+1;
end
fprintf('finished loading')
% N = nframes; % Number of frames for FFT
% ens_CBF = zeros(roi(3)*roi(4),length(1:N/2+1)); % Initialize ensemble CBF
% px_CBF = zeros(roi(3),roi(4),1,length(1:N/2+1)); % Initialize pixel CBF
% px_max = zeros(roi(3),roi(4)); % Initialize maximum power per pixel

% Loop over each pixel in the ROI
i=1;
j=1;
N=nframes;
%for i = 1:length(xs)
%    for j = 1:length(ys)


x = squeeze(gframe(i,j,:,:))';  % Time series of pixel intensity
xdft = fft(x-mean(x));  % perform fft
xdft1 = xdft(1:N/2+1);

psdx = (1/(N*Fs)) * abs(xdft1).^2;
psdx(2:end-1) = 2*psdx(2:end-1);  % Correct amplitude for one-sided PSD

fprintf('xdft')
disp(xdft)
fprintf('xdft1')
disp(xdft1)
fprintf('psdx')
disp(psdx)