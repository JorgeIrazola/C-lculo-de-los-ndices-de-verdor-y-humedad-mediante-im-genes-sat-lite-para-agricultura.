# se realiza la peticion de las imagenes satelite mediante la API sentinelsat
sentinelsat -u jorgeirazola -p ledesma8 -g map.geojson -s 20180801 -e 20180831 --sentinel 2 --cloud 5 -d --path C:\Users\UserUNIR1\Desktop\FINAL_WIT\ImagenesSentinel2\

# Options
# -u 	--user 	TEXT 	Username [required] (or environment variable DHUS_USER)
# -p 	--password 	TEXT 	Password [required] (or environment variable DHUS_PASSWORD)
# --url 	TEXT 	Define another API URL. Default URL is 'https://scihub.copernicus.eu/apihub/'.
# -s 	--start 	TEXT 	Start date of the query in the format YYYYMMDD.
# -e 	--end 	TEXT 	End date of the query in the format YYYYMMDD.
# -g 	--geometry 	PATH 	Search area geometry as GeoJSON file.
# --uuid 	TEXT 	Select a specific product UUID instead of a query. Multiple UUIDs can separated by commas.
# --name 	TEXT 	Select specific product(s) by filename. Supports wildcards.
# --sentinel 	  	Limit search to a Sentinel satellite (constellation).
# --instrument 	  	Limit search to a specific instrument on a Sentinel satellite.
# --producttype 	  	Limit search to a Sentinel product type.
# -c 	--cloud 	INT 	Maximum cloud cover in percent. (requires --sentinel to be 2 or 3)
# -o 	--order-by 	TEXT 	Comma-separated list of keywords to order the result by. Prefix '-' for descending order.
# -l 	--limit 	INT 	Maximum number of results to return. Defaults to no limit.
# -d 	--download 	  	Download all results of the query.
# --path 	PATH 	Set the path where the files will be saved.
# -q 	--query 	TEXT 	Extra search keywords you want to use in the query. Separate keywords with comma. Example: 'producttype=GRD,polarisationmode=HH'.
# -f 	--footprints 	  	Create geojson file search_footprints.geojson with footprints of the query result.
# --version 	  	Show version number and exit.
# --help 	  	Show help message and exit.