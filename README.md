# Debris Flow Data

## To Download

`python3 -m pip install -r requirements.txt` 

`python3 download_data.py`

## Data Format

Each data file consists of 10,000 rows, with the same headers across
all.

The headers will have more information than needed. For example, some
headers end with `.type` can be ignored. 

Each mudslide event has a unique id. This is given in the
`mudslide_id.value` column. Each mudslide event can be associated with
one or more other events that happened in the same are.

If there are multiple natural disasters that happened relative to a
single debris flow, then for each natural disaster, there will be a row
with the corresponding debris flow event.


### Relevant Headers

- `mudslide_id.value`: The identifier of the mudslide
- `mudslide_description.value`: The text description of the mudslide
- `mudslide_date.value`: The date that the mudslide happened
- `mudslide_geometry.value`: The geometry of the mudslide
- `natural_disaster_id.value`: The identifier of a disaster that
  happened in the same location as a mudslide
- `natural_disaster_description.value`: The text description of the
  natural disaster
- `natural_disaster_start_date.value`: Optional start date of the
  natural disaster
- `natural_disaster_end_date.value`: Optional end date of the natural
  disaster
- `natural_disaster_year.value`: Optional year that the natual disaster
  happened
- `natural_disaster_geometry.value`: Geometry of the natural disaster