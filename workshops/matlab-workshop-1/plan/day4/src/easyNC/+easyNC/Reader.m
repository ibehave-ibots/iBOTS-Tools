classdef Reader
    % NetCDF is a class for handling NetCDF files in MATLAB.
    % It allows for reading data from these files and provides information about their contents.
    %
    % Properties:
    %   filename: A string storing the path or name of the NetCDF file.
    %   variables: A cell array of strings containing names of loadable variables from the file.
    %
    % Methods:
    %   NetCDF: Constructor for initializing the NetCDF object with a file.
    %   read2struct: Reads data from the file and returns it as a structure.
    %   read2table: Reads data from the file and returns it as a table.
    %   print_info: Displays detailed information about the file's contents.
    %   info: Retrieves detailed information about the file's contents.
    %   getLoadableVariables: Identifies and returns loadable variables from the file.


    properties
        filename  % Path or name of the NetCDF file
        variables % Cell array of loadable variable names
    end

    methods
        function obj = Reader(filename)
            % Constructor for the NetCDF class.
            % Initializes a new NetCDF object with the specified filename.
            %
            % Parameters:
            %   filename: String specifying the NetCDF file name or path.
            %
            % Returns:
            %   obj: Initialized instance of the NetCDF class.

            obj.filename = filename;
            obj.variables = obj.getLoadableVariables();
        end

        function dset = read2struct(obj, varargin)
            % Reads data from the NetCDF file and returns it as a structure.
            % Optionally, specific variables can be read.
            %
            % Parameters:
            %   varnames: (Optional) Cell array containing names of variables to be read.
            %             If empty, all variables are read.
            %
            % Returns:
            %   dset: Structure where each field corresponds to a variable in the file.

            if isempty(varargin)
                varnames = {};
            else
                varnames = varargin{1};
            end
            dset = load2struct(obj.filename, varnames);
        end

        function df = read2table(obj, varargin)
            % Reads specified variables from the NetCDF file and returns them as a long table.
            %
            % Parameters:
            %   varnames: Cell array of strings specifying the names of variables to be read.
            %
            % Returns:
            %   df: Table containing the specified variables.
            if isempty(varargin)
                varnames = {};
            else
                varnames = varargin{1};
            end
            df = load2table(obj.filename, varnames);
        end

        function [] = print_info(obj)
            % Displays detailed information about the NetCDF file.
            ncdisp(obj.filename, "/", "full");
        end

        function info = info(obj)
            % Returns a structure containing detailed information about the file's contents.
            info = ncinfo(obj.filename);
        end

        function vars = getLoadableVariables(obj)
            % Identifies and returns the names of variables in the NetCDF file that can be loaded.
            % Excludes variables that are dimensions.
            vars = {};
            info = ncinfo(obj.filename);
            variables_all = {info.Variables.Name};
            for var = variables_all
                if ~ismember(var, {info.Dimensions.Name})
                    vars = [vars var];
                end
            end
        end

        function dimNames = getDimensionNames(obj)
            % Retrieves the names of dimensions in the NetCDF file.
            %
            % Returns:
            %   dimNames: Cell array of strings containing names of dimensions.

            info = ncinfo(obj.filename);      % Get information about the NetCDF file
            dimNames = {info.Dimensions.Name}; % Extract the names of the dimensions
        end

    end
end