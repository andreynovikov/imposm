#!/bin/sh

PYTHONPATH=build/lib.linux-x86_64-2.7/ python2 -m imposm.app --read --cache-dir=/gis/imposm_cache --overwrite-cache --write --database=gis --user=andrey --deploy-production-tables --proj=EPSG:3857 --mapping-file=/gis/imposm/maptrek.py /gis/77-40.osm.pbf
