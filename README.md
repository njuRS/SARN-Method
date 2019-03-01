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
- Write down the file path
- Set input **6 parameters**. 

| parameters | description |
|----|---|
|  |  **WV**: WorldView image  |
|  |  **SPOT**: SPOT image  |
|*sensor*  |  **Sentinel2**: Sentinle-2 image after NDWI calculation  |
|  |  **Landsat**: Landsat panchromatic image  |
|  |  **LandsatNDWILandsat**: image after NDWI calculation  |
|*inverse*  |set 1 to convert dark rivers into bright rivers (e.g., for panchromatic image); set 0 to keep bright rivers (e.g., for NDWI images)|
|*width*  |small river width for Gabor filter, default = 2|
|*ppo_length*  |path opening length, default = 20|
|*histCountThreshold*  |a pixel count threshold to stretch image pixel values, default = 1000|
|*Smooth (optional)*  |used for denoise algorithm. Because denoise algorithm is too slow and scale dependent, is abandoned for large images,  default = 0.7|

- Click **run**.

If you see these commands in the command window, the river detection code is running successfully.
![alt text](https://github.com/njuRS/picture/blob/master/1549183907(1).jpg?raw=true)
You will get 3 processed images. ``test_sentinel2_image_bandpass_gabor_cpo20.tif`` is the final result.
![alt text](https://github.com/njuRS/picture/blob/master/1549183928(1).jpg?raw=true)

# Acknowledgements
## Corresponding Author
- Xin Lu (xinlu.nju@gmail.com, School of Geography and Ocean Science, Nanjing University)
- Kang Yang (kangyang@nju.edu.cn, ph: 13814179324, School of Geography and Ocean Science, Nanjing University) 
- Yao Lu (yaolu.nju@gmail.com, School of Geography and Ocean Science, Nanjing University)
