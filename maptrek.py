from imposm.mapping import (
    Options,
    Points, LineStrings, Polygons,
    String, Bool, Integer, OneOfInt,
    LocalizedName, Name, Class,
    WayZOrder, ZOrder, Direction,
    GeneralizedTable, UnionView,
    FieldType, FixInvalidPolygons,
    PseudoArea, meter_to_mapunit, sqr_meter_to_mapunit,
)

import logging
log = logging.getLogger(__name__)

# # internal configuration options
# # uncomment to make changes to the default values
# import imposm.config
#
# # import relations with missing rings
# imposm.config.import_partial_relations = False
#
# # select relation builder: union or contains
# imposm.config.relation_builder = 'contains'
#
# # log relation that take longer than x seconds
# imposm.config.imposm_multipolygon_report = 60
#
# # skip relations with more rings (0 skip nothing)
# imposm.config.imposm_multipolygon_max_ring = 0
#
# # split ways that are longer than x nodes (0 to split nothing)
# imposm.config.imposm_linestring_max_length = 50
#
# # cache coords in a compact storage (with delta encoding)
# # use this when memory is limited (default)
# imposm.config.imposm_compact_coords_cache = True

db_conf = Options(
    # db='osm',
    host='localhost',
    port=5432,
    user='osm',
    password='osm',
    sslmode='allow',
    prefix='osm_new_',
    proj='EPSG:3857',
)


class Height(String):
    """
    Field for height values.

    :PostgreSQL datatype: INTEGER

    """

    column_type = "INTEGER"

    def value(self, val, osm_elem):
        multiplier = 100
        if val and val.lower().endswith('m'):
            val = val[:-1]
            val = val.strip()
        if val and val.lower().endswith('ft'):
            val = val[:-2]
            val = val.strip()
            multiplier = 30.48
        if val:
            try:
                return int(float(val.replace(',', '.')) * multiplier)
            except ValueError, ex:
                log.warn('failed to process height value for %s: %s', osm_elem.osm_id, val)
                log.exception(ex)
                return None
        else:
            return val


class Building(Polygons):
    fields = (
        ('building', String()),
        ('amenity', String()),
        ('shop', String()),
        ('historic', String()),
        ('tourism', String()),
        ('religion', String()),
        ('fee', String()),
        ('access', String()),
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('building:parts', String()),
        ('height', Height()),
        ('min_height', Height()),
        ('building:levels', Integer()),
        ('building:min_level', Integer()),
        ('building:colour', String()),
        ('roof:colour', String()),
        ('building:material', String()),
        ('roof:material', String()),
        ('addr:housenumber', String()),
    )

buildings = Building(
    name = 'buildings',
    with_type_field = False,
    with_label_field = True,
    mapping = {
        'building': (
            '__any__',
        ),
        'amenity': (
            'police',
            'fire_station',
            'place_of_worship',
            'pharmacy',
            'doctors',
            'veterinary',
            'cafe',
            'pub',
            'bar',
            'fast_food',
            'restaurant',
            'bank',
            'atm',
            'bus_station',
            'fuel',
            'post_office',
            'theatre',
            'cinema',
            'shelter',
            'bicycle_rental',
            'parking',
            'library',
            'car_repair',
            'toilets',
        ),
        'shop': (
            'bakery',
            'hairdresser',
            'supermarket',
            'doityourself',
            'mall',
            'pet',
            'car',
            'car_repair',
        ),
        'tourism': (
            'wilderness_hut',
            'alpine_hut',
            'camp_site',
            'caravan_site',
            'guest_house',
            'motel',
            'hostel',
            'hotel',
            'attraction',
            'viewpoint',
            'museum',
            'information',
        ),
        'historic': (
            'memorial',
            'castle',
            'ruins',
            'monument',
        ),
    }
)

building_parts = Building(
    name = 'building_parts',
    with_label_field = True,
    mapping = {
        'building:part': (
            '__any__',
        ),
    }
)

amenities = Points(
    name='amenities',
    with_type_field = False,
    fields = (
        ('amenity', String()),
        ('shop', String()),
        ('historic', String()),
        ('tourism', String()),
        ('leisure', String()),
        ('religion', String()),
        ('fee', String()),
        ('access', String()),
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
    ),
    mapping = {
        'amenity': (
            'drinking_water',
            'police',
            'fire_station',
            'place_of_worship',
            'pharmacy',
            'doctors',
            'veterinary',
            'cafe',
            'pub',
            'bar',
            'fast_food',
            'restaurant',
            'bank',
            'atm',
            'bus_station',
            'fuel',
            'post_office',
            'theatre',
            'cinema',
            'shelter',
            'bicycle_rental',
            'fountain',
            'telephone',
            'parking',
            'post_box',
            'library',
            'car_repair',
            'toilets',
            'university',
            'school',
            'college',
            'kindergarten',
            'hospital',
        ),
        'leisure': (
            'playground',
        ),
        'shop': (
            'bakery',
            'hairdresser',
            'supermarket',
            'doityourself',
            'mall',
            'pet',
            'car',
            'car_repair',
        ),
        'tourism': (
            'wilderness_hut',
            'alpine_hut',
            'camp_site',
            'caravan_site',
            'guest_house',
            'motel',
            'hostel',
            'hotel',
            'attraction',
            'viewpoint',
            'museum',
            'information',
            'picnic_site',
            'artwork',
        ),
        'historic': (
            'memorial',
            'castle',
            'ruins',
            'monument',
        ),
    }
)

class Highway(LineStrings):
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('tunnel', Bool()),
        ('bridge', Bool()),
        ('layer', Integer()),
        ('oneway', Direction()),
        ('ref', String()),
        ('access', String()),
        ('z_order', WayZOrder()),
    )
    field_filter = (
        ('area', Bool()),
    )

motorways = Highway(
    name = 'motorways',
    mapping = {
        'highway': (
            'motorway',
            'motorway_link',
            'trunk',
            'trunk_link',
            'primary'
        ),
    }
)

mainroads = Highway(
    name = 'mainroads',
    mapping = {
        'highway': (
            'primary_link',
            'secondary',
            'secondary_link',
            'tertiary',
            'tertiary_link',
            'road',
            'unclassified',
        ),
    }
)

transport_points = Points(
    name='transport_points',
    fields = (
        ('class', Class()),
        ('station', String()),
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
    ),
    mapping = {
        'highway': (
            'traffic_signals',
            'bus_stop',
        ),
        'railway': (
            'station',
            'halt',
            'tram_stop',
            'crossing',
            'level_crossing',
            'subway_entrance',
        ),
        'aeroway': (
            'aerodrome',
            'heliport',
            'helipad',
        ),
    }
)

landusages = Polygons(
    name = 'landusages',
    with_label_field = True,
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('area', PseudoArea()),
        ('z_order', ZOrder([
            'military',
            'nature_reserve',
            'protected_area',
            'national_park',
        ])),
    ),
    mapping = {
        'landuse': (
            'military',
        ),
        'leisure': (
            'nature_reserve',
            'protected_area',
            'national_park',
        ),
        'boundary': (
            'nature_reserve',
            'protected_area',
            'national_park',
        ),
})

forests = Polygons(
    name = 'forests',
    fields = (
        ('area', PseudoArea()),
    ),
    mapping = {
        'landuse': (
            'forest',
            'wood',
        ),
        'natural': (
            'forest',
            'wood',
        ),
})

waterways = LineStrings(
    name = 'waterways',
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
    ),
    mapping = {
        'barrier': (
            'ditch',
        ),
        'waterway': (
            'stream',
            'river',
            'canal',
            'drain',
            'ditch',
        ),
    },
    field_filter = (
        ('tunnel', Bool()),
    ),
)

waterareas = Polygons(
    name = 'waterareas',
    with_label_field = True,
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('area', PseudoArea()),
    ),
    mapping = {
        'waterway': ('riverbank','dock'),
        'natural': ('water',),
        'landuse': ('basin', 'reservoir'),
    },
)

railways = LineStrings(
    name = 'railways',
    fields = (
        ('tunnel', Bool()),
        ('bridge', Bool()),
        ('layer', Integer()),
        ('z_order', WayZOrder()),
    ),
    mapping = {
        'railway': (
            'rail',
            'tram',
            'light_rail',
            'monorail',
            'miniature',
            'subway',
            'narrow_gauge',
            'preserved',
            'funicular',
            'monorail',
            'disused',
            'abandoned',
            'preserved',
        )}
)

places = Points(
    name = 'places',
    mapping = {
        'place': (
            'ocean',
            'sea',
            'country',
            'state',
            'region',
            'island',
            'city',
            'town',
            'village',
            'hamlet',
            'suburb',
            'neighbourhood',
            'locality',
            'isolated_dwelling',
        ),
    },
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('z_order', ZOrder([
            'ocean',
            'sea',
            'country',
            'state',
            'region',
            'island',
            'city',
            'town',
            'village',
            'hamlet',
            'suburb',
            'neighbourhood',
            'locality',
            'isolated_dwelling',
        ])),
        ('population', Integer()),
        ('admin_level', Integer()),
        ('capital', Integer()),
    ),
)

admin = Polygons(
    name = 'admin',
    mapping = {
        'boundary': (
            'administrative',
        ),
    },
    fields = (
        ('admin_level', OneOfInt('1 2 3 4 5 6'.split())),
    ),
)

barrierpoints = Points(
    name = 'barrierpoints',
    mapping = {
        'barrier': (
            'block',
            'bollard',
            'border_control',
            'chain',
            'cycle_barrier',
            'gate',
            'lift_gate',
            'toll_booth',
            'yes',
        )}
)

barrierways = LineStrings(
    name = 'barrierways',
    mapping = {
        'barrier': (
            'city_wall',
            'fence',
            'hedge',
            'retaining_wall',
            'wall',
        )}
)

labelednatureareas = Polygons(
    name = 'labelednatureareas',
    with_label_field = True,
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('class', Class()),
        ('area', PseudoArea()),
    ),
    mapping = {
        'natural': ('marsh','wetland',),
        'place': ('island',),
    },
)

natureareas = Polygons(
    name = 'natureareas',
    fields = (
        ('class', Class()),
        ('area', PseudoArea()),
    ),
    mapping = {
        'landuse': (
            'meadow',
            'grass',
            'vineyard',
            'farmland',
            'greenhouse_horticulture',
            'plant_nursery',
        ),
        'natural': (
            'grassland',
            'scrub',
            'scree',
            'shingle',
            'sand',
            'beach',
            'mud',
            'glacier',
        ),
    },
)

labeledurbanareas = Polygons(
    name = 'labeledurbanareas',
    with_label_field = True,
    fields = (
        ('name', Name()),
        ('name:en', Name()),
        ('name:de', Name()),
        ('name:ru', Name()),
        ('class', Class()),
        ('area', PseudoArea()),
    ),
    mapping = {
        'landuse': (
            'cemetery',
        ),
        'leisure': (
            'dog_park',
            'park',
            'playground',
            'sports_centre',
            'water_park',
        ),
        'amenity': (
            'university',
            'school',
            'college',
            'kindergarten',
            'hospital',
            'place_of_worship',
        ),
        'tourism': (
            'zoo',
        ),
    },
)

urbanareas = Polygons(
    name = 'urbanareas',
    fields = (
        ('class', Class()),
        ('area', PseudoArea()),
    ),
    mapping = {
        'amenity': (
            'fountain',
        ),
        'landuse': (
            'residential',
            'retail',
            'commercial',
            'industrial',
            'village_green',
            'recreation_ground',
            'allotments',
            'quarry',
            'farmyard',
        ),
        'leisure': (
            'garden',
            'golf_course',
            'pitch',
            'stadium',
            'common',
        ),
        'tourism': (
            'picnic_site',
        ),
    },
)
