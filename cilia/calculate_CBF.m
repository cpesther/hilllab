%% Get Ciliary Beat Frequency from ROI
% This function calculates the ciliary beat frequency (CBF) from a video
% of cilia motion, returning the mean CBF over a region of interest (ROI),
% the CBF at each pixel, and the fraction of functional ciliated area.

function [mens_CBF, px_CBF, FFCA] = calculate_CBF(vidname,Fs,fthresh)
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
while hasFrame(video)
    vid = readFrame(video);
    if ~strcmp(video.VideoFormat,'Grayscale')
        gframe(:,:,k) = rgb2gray(vid(xs,ys,:)); % Convert RGB to grayscale
    else
        gframe(:,:,k) = vid(xs,ys,:);          % Already grayscale
    end
    k=k+1;
end

N = nframes; % Number of frames for FFT
ens_CBF = zeros(roi(3)*roi(4),length(1:N/2+1)); % Initialize ensemble CBF
px_CBF = zeros(roi(3),roi(4),1,length(1:N/2+1)); % Initialize pixel CBF
px_max = zeros(roi(3),roi(4)); % Initialize maximum power per pixel

% Loop over each pixel in the ROI
m=1;
for i = 1:length(xs)
    for j = 1:length(ys)
        x = squeeze(gframe(i,j,:,:))';  % Time series of pixel intensity
        xdft = fft(x-mean(x));          % FFT after removing mean
        xdft = xdft(1:N/2+1);           % Keep positive frequencies
        psdx = (1/(N*Fs)) * abs(xdft).^2; % Power spectral density
        psdx(2:end-1) = 2*psdx(2:end-1);  % Correct amplitude for one-sided PSD
        freq = 0:Fs/length(x):Fs/2;       % Frequency vector
        psdx(1:15) = 0;                   % Remove very low frequencies (noise)
        ens_CBF(m,:) = psdx;              % Store in ensemble
        px_CBF(i,j,1,:) = psdx;           % Store PSD for this pixel
        px_max(i,j) = max(psdx);          % Max power for this pixel
        m=m+1;
    end
end

% Calculate mean CBF over all pixels
mens_CBF = mean(ens_CBF,1);

% Plot the mean periodogram
figure;
plot(freq(1:end),mens_CBF(1:end))
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

% Compute fraction of functional ciliated area
spx = px_max(:);                  % Flatten max powers
FFCA = sum(spx>fthresh)/numel(spx); % Fraction exceeding threshold
figure;imshow(px_max/max(freq));  % Display max PSD per pixel as image

% Save results
save([vidname(1:end-4),'_CBF.mat'],'freq','mens_CBF','FFCA')
