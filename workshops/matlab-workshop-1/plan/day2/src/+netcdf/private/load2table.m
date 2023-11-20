function dset = load2table(filename, varnames)
%LOAD2TABLE Loads data from a NetCDF file into a table.
%
%   dset = LOAD2TABLE(filename, varnames) loads data from the NetCDF file
%   specified by 'filename'. It returns a table 'dset' containing variables
%   and their corresponding data in a long format. If 'varnames' is provided,
%   only those variables are loaded. Otherwise, all variables are loaded.
%   The function ensures that there must be overlapping dimensions among
%   the requested variables to reshape the data correctly into a long format.
%
%   Inputs:
%       filename - A string specifying the path or name of the NetCDF file.
%       varnames - (Optional) A cell array of strings specifying the names
%                  of variables to be loaded. If not provided or empty, all
%                  non-dimension variables in the file are loaded.
%
%   Outputs:
%       dset - A table where each column corresponds to a variable or a 
%              dimension in the NetCDF file.
%
%   This function first checks if the requested variables have overlapping 
%   dimensions. If they do not, an error is raised. It then reads the data 
%   for each variable and reshapes it into a long format, suitable for a 
%   table structure. This is particularly useful for multivariate analysis 
%   or other forms of data processing that require data in a tabular format.
%
%   Note:
%   - The function requires that there must be overlapping dimensions
%     between the requested variables to allow reshaping the data into
%     a long format. If the dimensions do not overlap, an error is raised.
%   - Dimension variables are not included in the output table unless 
%     explicitly specified in 'varnames'.
%
%   Example:
%       data = load2table('example.nc', {'temperature', 'humidity'});
%       % This loads 'temperature' and 'humidity' variables from 'example.nc'
%       % and reshapes them into a long table format.
%
%   See also NCINFO, NCREAD.


% Get information about the variables in the NetCDF file
info = ncinfo(filename);

% If no varnames are not provided, load all variables
if isempty(varnames)
    varnames = {info.Variables.Name};
end
varnames = arrayfun(@string, varnames);

var_indices = [];
for ii = 1:length(info.Variables)
    var = info.Variables(ii);
    if ismember(var.Name, varnames) && ~ismember(var.Name, {info.Dimensions.Name})
        var_indices = [var_indices ii];
    end
end
vars = info.Variables(var_indices);


% Confirm that all the requested variables have overlapping Dimensions,
% raise Error otherwise
numDims = arrayfun(@(s) length(s.Dimensions), vars);
[~, sortedIndices] = sort(numDims, "descend");
varsSorted = vars(sortedIndices);

if isempty(varsSorted)
    if all(ismember(varnames, {info.Dimensions.Name}))
        error("Invalid DataVariable '%s': Must include a Non-Dimension Variable", varnames);
    end
end

var = varsSorted(1);
dims = {var.Dimensions.Name};
for var = varsSorted(2:end)
    for dimName = {var.Dimensions.Name}
        if ~ismember(dimName{1}, dims)
            error("Non-overlapping Dimension in table: %s %s", dimName{1}, cell2mat(dims))
        end
    end
end




% Prepare Output Variable
dset = struct();
bigVar = varsSorted(1);
if length(bigVar.Dimensions) == 1
    % Extract The only Dimension.
    name = bigVar.Dimensions(1).Name;
    dset.(name) = ncread(filename, name);

    % Extract Each Data Variable.
    for var = varsSorted
        dset.(var.Name) = ncread(filename, var.Name);
    end

else
    % Extract Each Dimension
    for ii = 1:length(bigVar.Dimensions)
        name = bigVar.Dimensions(ii).Name;
        data = ncread(filename, name);
        expanded = expandData(data, bigVar.Size, ii);
        dset.(name) = expanded(:);
    end
    
    % Extract Each Data Variable
    for var = varsSorted
        data = ncread(filename, var.Name);
        data_size = size(data);
        if length(var.Dimensions) == max(numDims)
            expanded = data;  % special case: quick and easy
        else
            indices = arrayfun(@(dim) find(strcmp({bigVar.Dimensions.Name}, dim.Name)), var.Dimensions);
            indices = num2cell(indices);
            expanded = expandData(data, bigVar.Size, indices{:});
        end
        dset.(var.Name) = expanded(:);
    end

end


dset = struct2table(dset);



