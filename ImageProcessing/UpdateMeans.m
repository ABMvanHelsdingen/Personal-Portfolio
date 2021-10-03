% This function updates the RGB values of the mean of each cluster as
% part of the k-means algorithim. 
% Inputs
% image: The 3D array containing the RGB values of each pixel in the image
% k: number of clusters
% clusters: a mxn array of cluster numbers of each pixel, output of AssignToClusters
% Output
% newMeans: kx1x3 array containing the RGB values of the re-calculated means
% Author: Alec van Helsdingen

function [newMeans]=UpdateMeans(image,k,clusters)

%Get number of rows and columns in image
[imageRows,imageCols,~]=size(image);

%preallocate newMeans, pixelsPerCluster and clusterPositions
newMeans=zeros(k,1,3);
pixelsPerCluster=zeros(k,1);
clusterPositions=zeros(imageRows,imageCols);

for i=1:k % for each cluster
    % find the pixels belonging to each cluster as a logical array
    clusterPositions=clusters==i;
    % sum the elements of array to find number of pixels in cluster
    pixelsPerCluster(i,1)=sum(sum(clusterPositions,1),2);
    
    % repeat clusterPositions in z-direction
    clusterPositions=repmat(clusterPositions,1,1,3);
    % multiply element-wise clusterPositions and image and sum across rows and
    % columns. This gives sums of R,G and B values of all the pixels of the cluster
    newMeans(i,1,:)=sum(sum(clusterPositions.*image,1),2);
end


for j=1:3 % for each colour
    % To get mean of RGB values, multiply by number of pixels in cluster
    newMeans(:,:,j)=newMeans(:,:,j)./pixelsPerCluster;
end

end


