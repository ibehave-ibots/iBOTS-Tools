function  download_from_sciebo(sciebo_url, file_download_path, is_relative_path)
     arguments 
            sciebo_url {mustBeText}
            file_download_path {mustBeText}
            is_relative_path {mustBeNumericOrLogical} = true
     end
% Downloads a file from sciebo to the specified file_download_path
% By default, the file is downloaded to the same directory as the
% excecuting matlab script
% is_relative_path = false, allows the full path to be specified 
% eg. download_from_sciebo(sciebo_url, "/home/data/sciebo/data.dat", false)

% make any new directories that might be needed
file_download_dir = fileparts(file_download_path);
if ~exist(file_download_dir, 'dir') & file_download_dir~=""
       mkdir(file_download_dir)
end
%change directory to where script is being run
cwd = fileparts(matlab.desktop.editor.getActiveFilename);
cd(cwd) 

if is_relative_path
    full_download_location = fullfile(cwd, file_download_path);
else
    full_download_location = file_download_path;
end

if sciebo_url(end) == '/'
    download_url = strcat(sciebo_url, 'download');
else
    download_url = strcat(sciebo_url, '/download');
end
websave(full_download_location, download_url );
end