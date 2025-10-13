% Christopher Esther, Hill Lab, 9/26/2025

function compile_memmap_video(memmap_path, suffix, fps, width, height)
    % Compiles the video data stored in a .bin memory map produced during
    % record_realtime_track.m into a standard .avi file. 

    % Ensure memmapPath is a character vector (MATLAB is picky)
    if isstring(memmap_path)
        memmap_path = char(memmap_path);
    end

    % Ensure suffix is a string/char if provided
    if nargin >= 2 && ~isempty(suffix)
        if ~ischar(suffix) && ~isstring(suffix)
            suffix = num2str(suffix);  % convert numeric suffix
        end
    else
        suffix = '';
    end

    % Output .avi path (with optional suffix in filename)
    [folder, name, ~] = fileparts(memmap_path);
    if ~isempty(suffix)
        aviName = [name '_' suffix '.avi'];  % append suffix
    else
        aviName = [name '.avi'];
    end
    aviPath = fullfile(folder, aviName);

    % Open memmap
    m = memmapfile(memmap_path, 'Writable', false);
    totalFrames = numel(m.Data) / (width * height);

    % Reshape directly into [height, width, frames]
    frames = reshape(m.Data, [height, width, totalFrames]);

    % Create AVI video
    v = VideoWriter(aviPath, 'Uncompressed AVI');
    v.FrameRate = fps;
    open(v);

    for i = 1:totalFrames
        frame = frames(:,:,i);
        writeVideo(v, mat2gray(frame)); % normalize grayscale to [0,1]
    end

    close(v);
    fprintf('Video written to %s\n', aviPath);
end
