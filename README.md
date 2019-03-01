<h1 align="center">River Connection Code</h1>

# Environment
Python with ``ArcPy`` package
# Prepare data
- ``DEM-modeled drainage network.shp``: the DEM-modeled drainage network polyline
- ``RS-mapped river network.shp``: the river centerlines of the RS water body mask 
- ``RS water mask.tif``: the binary water body mask, water is set to 1, non-water is 0

![alt text](https://github.com/njuRS/picture/blob/master/data.jpg?raw=true)


**In order to ensure this code runs correctly, please make sure the coordinates are consistent**
# Create Geodatabase
Create a ``File Geodatabase.gdb`` and import the three files in it. All process data will be saved in this database.

![alt text](https://github.com/njuRS/picture/blob/master/create_database.png?raw=true)



![alt text](https://github.com/njuRS/picture/blob/master/add_files_into_geodatabase.png?raw=true)


# Run river connection code

- Open ``connect_river.py`` in Python. 
- Set input **6 parameters**. 

| parameters | description |
|----|---|
|*workspace*  |the path of the geodatabaseset|
|*DEM*  |the name of the DEM-modeled drainage network|
|*RS_vector*  |the name of the RS-mapped river centerlines|
|*RS_Raster*  |the name of the RS binary water body mask|
|*cell size*  |the cell size of the images, Sentinel-2 imagery is 10|
|*delete_length*  |river length less than 300 m will be deleted|

- Click **run**.

- These two shapefiles in the red box are the result. ``unspit_split_coincide + DEM name.shp`` is the RS-mapped river segments, and ``unspit_split_connect + DEM name.shp`` is the DEM-modeled river segments.

![alt text](https://github.com/njuRS/picture/blob/master/result.png?raw=true)

![alt text](https://github.com/njuRS/picture/blob/master/result2.png?raw=true)

# Acknowledgements
## Corresponding Author
- Xin Lu (xinlu.nju@gmail.com, ph:15951756762, School of Geography and Ocean Science, Nanjing University)
- Kang Yang (kangyang@nju.edu.cn, School of Geography and Ocean Science, Nanjing University) 
- Yao Lu (yaolu.nju@gmail.com, School of Geography and Ocean Science, Nanjing University)
