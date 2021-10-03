% This function selects k random pixels from an image
% Inputs
% image: The 3D array containing the RGB values of each pixel in the image
% k: number of random pixels to select
% Outputs
% points: kx2 array containing the row and column numbers of the selected points
% Author: Alec van Helsdingen

function [points]=SelectKRandomPoints(image,k)

% Get the number of rows and columns in the image
[imageRows,imageCols,~]=size(image);

points=zeros(k,2); %preallocate points

%Select k unqiue numbers from 1 to the number of pixels in the image
pointIndexes=randperm(imageRows*imageCols,k);

for i=1:k
    % convert linear index to rows and columns. ind2sub takes too long
    col=ceil(pointIndexes(i)/imageRows);
    row=pointIndexes(i)-(col-1)*imageRows;
    points(i,:)=[row,col];
end

end



