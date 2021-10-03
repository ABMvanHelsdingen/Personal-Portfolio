% This function creates an image of k colours only by replacing each pixel
% in the original image with the mean of the cluster that the pixel belongs to. 
% Inputs (both outputs of KMeansRGB)
% clusters: a mxn array containing the cluster number that each pixel has been assigned
% means:  kx1x3 array containing the RGB values of the final cluster means
% Output
% newImage: mxnx3 array containing the RGB values of each pixel of the k-colour image
% Author: Alec van Helsdingen

function [newImage]=CreateKColourImage(clusters,means)

% Get number of rows and columns in image
[imageRows,imageCols]=size(clusters);

newImage=zeros(imageRows,imageCols,3,'uint8'); %preallocate newImage in unit8 format

for i=1:imageRows % for each row
    for j=1:imageCols % for each column
        clusterNumber=clusters(i,j); % get the cluster number of the pixel
        % For the pixel in the new image, set the RGB values to the mean of
        % the cluster
        newImage(i,j,:)=means(clusterNumber,1,:);
    end
end

end


        
    