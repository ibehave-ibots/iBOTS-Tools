function [] = createNcAttributes(filename, varargin)

for ii = 1:2:length(varargin)
    key = varargin{ii};
    value = varargin{ii+1};
    ncwriteatt(filename, '/', key, value);
end
