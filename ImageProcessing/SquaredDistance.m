% This function calculates the square of the distance in 3D space between two points.  
% Inputs
% point1, point2: Can be either 1x3, 3x1 or 1x1x3 arrays containing the
% co-ordinates of the points. Both must have the same dimensions
% Outputs
% distance: the SQUARE of the distance between the points
% Author: Alec van Helsdingen

function [distance]=SquaredDistance(point1,point2)

% Subtract the two arrays and square element-wise the result, giving the
% x,y and z (or R,G and B) components of the displacements.
distanceComponents=(point1-point2).^2;

%sum the components, giving the square of the distance between the points
distance=sum(distanceComponents);

end

