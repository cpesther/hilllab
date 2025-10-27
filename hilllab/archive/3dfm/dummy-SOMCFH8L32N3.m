% Extract frame size from the format string
camera = 'FL3';

switch camera
    case 'GS3'
        video_format = 'F7_Raw8_2448x2048_Mode0';
    case 'FL3'
        video_format = 'F7_Raw8_1280x1024_Mode0';
    otherwise
        error('Unsupported camera type: %s', camera);
end

% Parse width and height from the format string
tokens = regexp(video_format, '_(\d+)x(\d+)_', 'tokens');
dims = str2double(tokens{1});  % dims = [width height]

width = dims(1);
height = dims(2);

fprintf('Frame size: %d x %d\n', width, height);
