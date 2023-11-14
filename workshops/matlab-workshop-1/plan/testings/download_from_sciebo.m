function  download_from_sciebo(url, file_out_relative_path)
     arguments 
            url {mustBeText}
            file_out_relative_path {mustBeText}
     end

% make any new directories that might be needed
if ~exist(fileparts(file_out_relative_path), 'dir') & fileparts(file_out_relative_path)~=""
       mkdir(fileparts(file_out_relative_path))
end
%change directory to where script is being run
cwd = fileparts(matlab.desktop.editor.getActiveFilename);
cd(cwd) 

full_download_location = fullfile(cwd, file_out_relative_path);

if url(end) == '/'
    download_url = strcat(url, 'download');
else
    download_url = strcat(url, '/download');
end
websave(full_download_location, download_url );
end