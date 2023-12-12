classdef Writer
    %WRITER Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        filename
    end
    

    
    methods (Access=public)
        function obj = Writer(filename, varargin)
            options = struct(overwrite=true);
            if nargin > 1
                options.overwrite = varargin{1};
            end
            obj.filename = filename;

            if options.overwrite && exist(filename, 'file')
                delete(filename)
            end
            fid = netcdf.create(filename, 'netcdf4');
            netcdf.close(fid);
        end

        function [] = write_dimension(obj, name, data, varargin)
            createNcDimension(obj.filename, name, data, varargin{:});
        end

        function [] = write_variable(obj, name, data, dimensions, varargin)
            createNcVariable(obj.filename, name, data, dimensions, varargin{:});
        end
        
        function [] = write_attributes(obj, varargin)
            createNcAttributes(obj.filename, varargin{:});
        end

        function [] = write_from_struct(obj, dset, varName, dimensions, varargin)
            dimensions = cellstr(dimensions);
            for name = dimensions
                name = name{1};
                data = dset.(name);
                try
                    createNcDimension(obj.filename, name, data);
                catch ME
                    if strcmp(ME.identifier, 'MATLAB:imagesci:netcdf:variableExists')
                        continue
                    else
                        rethrow(ME);
                    end
                end
            end
            size(dset.(varName))
            createNcVariable(obj.filename, varName, dset.(varName), dimensions, varargin{:})
        end


        function [] = print_info(obj)
            % Displays detailed information about the NetCDF file.
            ncdisp(obj.filename, "/", "full");
        end

        function info = info(obj)
            % Returns a structure containing detailed information about the file's contents.
            info = ncinfo(obj.filename);
        end
    end

    methods  (Access=private)
        function dims = get_dimension_names(obj)
            if ~exist(obj.filename, 'file')
                dims = {};
                return
            end
            dims = cellstr({obj.info().Dimensions.Name});
        end

    end
end