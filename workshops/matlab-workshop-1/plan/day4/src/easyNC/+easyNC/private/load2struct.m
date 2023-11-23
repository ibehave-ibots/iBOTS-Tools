function dset = load2struct(filename, varnames)
%LOAD2STRUCT Loads data from a NetCDF file into a structure.
%
%   dset = LOAD2STRUCT(filename, varnames) loads data from the NetCDF file
%   specified by 'filename'. It returns a structure 'dset' containing 
%   variables and their corresponding data. If 'varnames' is provided, only
%   those variables are loaded. Otherwise, all variables are loaded.
%
%   Inputs:
%       filename - A string specifying the path or name of the NetCDF file.
%       varnames - (Optional) A cell array of strings specifying the names
%                  of variables to be loaded. If not provided or empty, all
%                  variables in the file are loaded.
%
%   Outputs:
%       dset - A structure where each field corresponds to a variable in
%              the NetCDF file. Fields are named after the variables.
%
%   This function first retrieves information about the variables in the
%   NetCDF file. It then loads the data for each requested variable into
%   the output structure. If a variable is a dimension, it is handled
%   specially: if the dimension data can be read directly, it is used;
%   otherwise, a default range (1 to the length of the dimension) is
%   created.
%
%   Example:
%       data = load2struct('example.nc', {'temperature', 'pressure'});
%       % This loads only 'temperature' and 'pressure' variables from 'example.nc'.
%
%   See also NCINFO, NCREAD.

% Get information about the variables in the NetCDF file
info = ncinfo(filename);

% If no varnames are not provided, load all variables
if isempty(varnames)
    varnames = {info.Variables.Name};
end
varnames = arrayfun(@string, varnames);


% Extract info for each requested variable
vars = [];
for var = info.Variables
    
    % Skip if variable is not in the list of requested variables
    if ~isempty(varnames) && ~any(ismember(var.Name, varnames))
        continue;
    end

    vars = [vars var];
end


% Initialize structure for output
dset = struct();

% Extract all the Dimensions
for var = vars
    % Load dimensions for each variable
    for dim = var.Dimensions
        % Skip if dimension already exists in structure
        if ismember(dim.Name, fieldnames(dset))
            continue;
        end

        % Try reading the dimension data, or create a default range
        try
            dset.(dim.Name) = ncread(filename, dim.Name);
        catch
            dset.(dim.Name) = (1:dim.Length)';
        end
    end
end

% Iterate over the variables in the file
for var = vars
    % Skip if variable already exists in structure
    if ismember(var.Name, fieldnames(dset))
        continue;
    end

    % Read variable data
    dset.(var.Name) = ncread(filename, var.Name);
end
end
