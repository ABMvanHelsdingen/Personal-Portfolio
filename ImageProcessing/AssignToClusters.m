% This function computes the distance from each pixel to each of the  k means. 
% Each pixel is assigned to the cluster whose mean it is closest to. 
% Inputs
% image: The 3D array containing the RGB values of each pixel in the image
% means: a kx1x3 array containing the RGB values for each mean. Output of
% either GetRGBValuesForPoints or UpdateMeans
% Output
% clusters: a mxn array containing the cluster number that each pixel has been assigned
% Author: Alec van Helsdingen

function [clusters]=AssignToClusters(image,means)

% Get number of rows and columns in image
[imageRows,imageCols,~]=size(image);

k=size(means,1); % get value of k

Distance=zeros(imageRows,imageCols,k); % preallocate Distance

for i=1:k % for each mean
    % Repeat the RGB values for the mean giving an array with dimensions mxnx3
    points=repmat(means(i,:,:),imageRows,imageCols);
    % For every pixel, subtract the RGB values of the mean, and square element-wise
    components=(image-points).^2;
    % Sum the R,G and B components of the distance from the mean for each pixel
    Distance(:,:,i)=sum(components,3);
end

% Get the indices of these minimum values in the z-direction of Distance
% These indices are the cluster numbers for each pixel
[~,clusters]=min(Distance,[],3);

end

