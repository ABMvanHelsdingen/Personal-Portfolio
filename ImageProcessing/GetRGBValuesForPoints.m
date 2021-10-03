% This function gets the RGB values for the k seed means that were
% randomly selected in SelectKRandomPoints
% Inputs
% image: The 3D array containing the RGB values of each pixel in the image
% points: output of SelectKRandomPoints, contains row and column numbers of
% seed positions
% Outputs
% seedMeans: a kx1x3 array containing the RGB values for each seed mean
% Author: Alec van Helsdingen

function [seedMeans]=GetRGBValuesForPoints(image,points)

k=size(points,1); % get value of k

seedMeans=zeros(k,1,3); % preallocate seedMeans

for i=1:k % for each seed mean
    row=points(i,1); % get row of seed mean
    col=points(i,2); % get column of seed mean
    seedMeans(i,1,:)=image(row,col,:); % place RGB values in seedMeans
end

end

