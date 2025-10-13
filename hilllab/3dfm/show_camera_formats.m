% Christopher Esther, Hill Lab, 9/26/2025

function show_camera_formats(cameraID)
% SHOWCAMERAFORMATS Display supported video formats for a PointGrey camera.
%
%   showCameraFormats(cameraID) prints all video formats for the camera
%   with the given ID.
%
%   cameraID (int): Index of the camera (usually 1 for the first camera).

    if nargin < 1
        cameraID = 1; % default to first camera
    end

    % Get adaptor and device information
    hwInfo = imaqhwinfo('pointgrey');           % Adaptor info
    if cameraID > length(hwInfo.DeviceIDs)
        error('Camera ID %d does not exist.', cameraID);
    end
    deviceInfo = hwInfo.DeviceInfo(cameraID);  % Device-specific info

    fprintf('Supported formats for camera %d (%s):\n', cameraID, deviceInfo.DeviceName);

    % Loop over each supported format and print
    for k = 1:length(deviceInfo.SupportedFormats)
        fprintf('  %s\n', deviceInfo.SupportedFormats{k});
    end
end
