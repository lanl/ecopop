# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:45:03 2022

@author: 318596
"""
import geopandas as gpd
from VotE import config
config.vote_db()
from VotE.streamflow import export_streamflow as es
from shapely.geometry import MultiPolygon


path_bounding_box = r"X:\Research\EpiEarth\Data\ecopop Layers\Finals\na_10k\trap_data_bb.gpkg" # shapefile of ROI
bb = gpd.read_file(path_bounding_box)
pgon = MultiPolygon(bb.geometry.tolist())
gage_params = {'within' : pgon,
               'max_drainarea_km2' : 10000,
               'fraction_valid' : .9,
               'vote_snapped' : True,
               'end_date': '2000-01-01',
               'min_span_years' : 10
              }
gage_ids = es.gage_selector(gage_params)
gages = es.get_gages(gage_ids)

# Export the gages and their watersheds (two files)
keepkeys = [k for k in gages.keys() if 'geom' not in k]
keepkeys = [k for k in keepkeys if 'chunk' not in k]
keepkeys.remove('id_duplicates')
gage_locs = gpd.GeoDataFrame(data=gages[keepkeys], geometry=gages['mapped_geom'], crs=gages.crs)
basins = gpd.GeoDataFrame(data=gages[keepkeys], geometry=gages['basin_geom_vote'], crs=gages.crs)

gage_locs['start_date'] = gage_locs['start_date'].astype(str)
gage_locs['end_date'] = gage_locs['start_date'].astype(str)
basins['start_date'] = basins['start_date'].astype(str)
basins['end_date'] = basins['start_date'].astype(str)

gage_locs.to_file(r'X:\Research\EpiEarth\Data\ecopop Layers\Finals\na_10k\gage_selection\trap_data_gages.gpkg', driver='GPKG')
basins.to_file(r'X:\Research\EpiEarth\Data\ecopop Layers\Finals\na_10k\gage_selection\trap_data_basins.gpkg', driver='GPKG')
