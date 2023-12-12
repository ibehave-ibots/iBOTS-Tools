function dataExpanded = expandData(data, refSize, dim1, varargin)
%EXPANDDATA

dims = [dim1 cell2mat(varargin)];

% Reshape
new_shape = ones(1, length(refSize));
new_shape(dims) = refSize(dims);
new_shape = num2cell(new_shape);
dataReshaped = reshape(data, new_shape{:});

% Repeat
repmats = refSize;
repmats(dims) = 1;
dataExpanded = repmat(dataReshaped, repmats);

assert(all(size(dataExpanded) == refSize));

end