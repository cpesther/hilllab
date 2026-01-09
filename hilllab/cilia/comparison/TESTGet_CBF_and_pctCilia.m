%% Get Ciliary Beat Frequency from ROI

function [mens_CBF, px_CBF, FFCA] = TESTGet_CBF_and_pctCilia(vidname,Fs,fthresh)
% Outputs:
% mens_CBF - ensemble mean CBF for the whole ROI selected
% px_CBF - "CBF" for each pixel
% FFCA - fraction of functional ciliated area

if (nargin<2) | ~isempty(Fs)
    Fs=60; % Set default sampling rate to 60 fps
end
if (nargin<3) | ~isempty(fthresh)
    fthresh=5; % Set default sampling rate to 60 fps
end

warning off

% % % % video = VideoReader(vidname);
% % % % img = readFrame(video);
% % % % himg = figure;
% % % % imshow(img)
% % % % title('Click and Drag over Ciliated ROI: Double-Click to Proceed')
% % % 
% % % video = VideoReader(vidname);
% % % lastF = read(video,inf);
% % % nframes = video.NumberOfFrames;
% % % 
% % % % h = imrect;
% % % position = size(lastF);
% % % position = [1,1,position(2)-1,position(1)-1];
% % % roi = round(position);
%%
video = VideoReader(vidname);
img = readFrame(video);
% himg = figure;
%imshow(img)
%title('Click and Drag over Ciliated ROI: Double-Click to Proceed')

video = VideoReader(vidname);
lastF = read(video,inf);
nframes = video.NumberOfFrames;

%h = imrect;
%position = wait(h);
%roi = round(position);

% Hardcoded ROI (alternative to above)
% [x, y, width, height]

roi = [10, 10, 1000, 1000];

%%

ys = roi(1):roi(1)+roi(3);
xs = roi(2):roi(2)+roi(4);
video = VideoReader(vidname);

k=1;
gframe = zeros(numel(xs),numel(ys),1,nframes);
while hasFrame(video)
    vid = readFrame(video);
    if ~strcmp(video.VideoFormat,'Grayscale')
        gframe(:,:,k) = rgb2gray(vid(xs,ys,:));
    else
        gframe(:,:,k) = vid(xs,ys,:);
    end
    k=k+1;
    fprintf('Conversion %d\r', k)
end

N = nframes;
ens_CBF = zeros(roi(3)*roi(4),length(1:N/2+1));
px_CBF = zeros(roi(4),roi(3),1,length(1:N/2+1));
px_max = zeros(roi(4),roi(3));

m=1;
for i = 1:length(xs)
    for j = 1:length(ys)
        x = squeeze(gframe(i,j,:,:))';
        xdft = fft(x-mean(x));
        xdft = xdft(1:N/2+1);
        psdx = (1/(N*Fs)) * abs(xdft).^2;
        psdx(2:end-1) = 2*psdx(2:end-1);
        freq = 0:Fs/length(x):Fs/2;
        psdx(1:15) = 0;
        ens_CBF(m,:) = psdx;
        px_CBF(i,j,1,:) = psdx;
        px_max(i,j) = max(psdx);
        m=m+1;
        fprintf('Calculation %d\r', m)
    end
end


mens_CBF = mean(ens_CBF,1);
figure;
plot(freq(1:end),mens_CBF(1:end))
grid on
title('Periodogram Using FFT')
xlabel('Frequency (Hz)')
ylabel('Power/Frequency (dB/Hz)')

spx = px_max(:);
FFCA = sum(spx>fthresh)/numel(spx);

fprintf('FFCA: %d', FFCA)
disp('Reached save point')


outDir = 'C:\Users\cpesther\Desktop\CBF MatLab Output';

[~, vidBase, ~] = fileparts(vidname);

% Ensure vidBase is a character vector
vidBase = char(vidBase);  

% Construct full path
outFile = fullfile(outDir, [vidBase '_CBF.mat']);

% Save
save(outFile, 'freq', 'mens_CBF', 'FFCA')



%figure;imshow(px_max/max(freq));
%save([vidname(1:end-4),'_CBF.mat'],'freq','mens_CBF','FFCA')
end
