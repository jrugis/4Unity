load('/Users/jrug001/Desktop/nesi00119/4Unity/dynamic_data/lumen_prop.mat');

x = lumen_prop.disc_centres(:,1);
y = lumen_prop.disc_centres(:,2);
z = lumen_prop.disc_centres(:,3);
plot3(x(1:191),y(1:191),z(1:191),"o");