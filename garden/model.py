from handbag import *
from garden import app

env = environment.open(app.config['HANDBAG_URL'])


class Distance(Validator):
    
    NOT_DISTANCE = "Not a valid distance"
    
    def validate(self, value):
        try:
            return float(value)
        except ValueError:
            raise InvalidError, self.NOT_DISTANCE


class Garden(env.Model):
    name = Text()
    seasons = OneToMany("GardenSeason", inverse="Garden")
    
    
class GardenSeason(env.Model):
    year = TypeOf(int)
    beds = OneToMany("Bed")
    dates = OneToMany("GardenDate")
    
    
class GardenDate(env.Model):
    name = Text()
    date = DateTime()
    
    
class GardenDateDelta(env.Model):
    days = TypeOf(int, optional=True, default=0)
    weeks = TypeOf(int, optional=True, default=0)
    months = TypeOf(int, optional=True, default=0)
    before = One(GardenDate)
    after = One(GardenDate)
    
    
class Bed(env.Model):
    name = Text()
    width = Distance()
    height = Distance()
    plantings = OneToMany("Planting")
    
    
class Planting(env.Model):
    plant = One("PlantVariety")
    quantity = TypeOf(int)


class Plant(env.Model):
    name = Text()
    varieties = OneToMany("PlantVariety", inverse='plant')
    
    
class PlantVariety(env.Model):
    name = Text()
    catalog_url = URL(optional=True)
    spacing = Distance(optional=True)
    thinned_spacing = Distance(optional=True)
    depth = Distance(optional=True)
    sowings = OneToMany("Sowing")
    harvestings = OneToMany("Harvesting")
    notes = GroupValidator(
        sowing=Text(optional=True),
        transplanting=Text(optional=True),
        harvesting=Text(optional=True),
        storage=Text(optional=True),
        optional=True
    )
    
class Sowing(env.Model):
    where = Enum("indoors", "outdoors", optional=True, default="outdoors")
    start = One("GardenDateDelta")
    stop = One("GardenDateDelta")
    repeat = One("GardenDateDelta")
    transplant = One("GardenDateDelta")
    notes = Text(optional=True)
    
    
class Harvesting(env.Model):
    start = One("GardenDateDelta")
    stop = One("GardenDateDelta")
    repeat = One("GardenDateDelta")
    notes = Text(optional=True)
    