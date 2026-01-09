function TESTrun_CBF_on_folder(rootFolder, Fs, fthresh)
% Recursively finds all AVI files and runs TESTGet_CBF_and_pctCilia on each

    if ~isfolder(rootFolder)
        error('Provided path is not a valid folder.');
    end

    aviFiles = dir(fullfile(rootFolder, '**', '*.avi'));
    nFiles = numel(aviFiles);

    fprintf('Found %d AVI files in:\n%s\n', nFiles, rootFolder);

    if nFiles == 0
        warning('No AVI files found. Exiting.');
        return;
    end

    userResp = input('Proceed with processing? (y/n): ', 's');
    if ~strcmpi(userResp, 'y')
        fprintf('Operation cancelled by user.\n');
        return;
    end

    for k = 1:nFiles
        vidPath = fullfile(aviFiles(k).folder, aviFiles(k).name);
        fprintf('Processing (%d of %d): %s\n', k, nFiles, vidPath);

        try
            TESTGet_CBF_and_pctCilia(vidPath, Fs, fthresh);
        catch ME
            warning('Failed on %s\n%s', vidPath, ME.message);
        end
    end
end
