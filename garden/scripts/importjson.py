import json
import os.path
from urlparse import urlparse
import shutil
import codecs
from datetime import datetime
from flask.ext.script import Command, Option
from garden import app

class ImportJSON(Command):
    """Import some garden data from a json file"""
    
    option_list = [
        Option('--clobber', '-c', action='store_true', help="Clobber the target database, if it exists"),
        Option('--file', '-f', dest="json_file")
    ]
    
    def run(self, clobber, json_file):
        if clobber:
            url = urlparse(app.config['HANDBAG_URL'])
            if os.path.exists(url.path):
                shutil.rmtree(url.path)
        
        global model
        from garden import model
        
        data = json.load(codecs.open(json_file))
        self.context = {}
        
        with model.env.write():
            g = model.Garden(name=data['name'])
            season = model.GardenSeason(year=data['year'])
            g.seasons.add(season)
            self.context['garden'] = g
        
        with model.env.write():
            self.context['dates'] = {}
            for k,v in data['dates'].items():
                month, day = map(int, v.split('-'))
                d = model.GardenDate(name=k, date=datetime(season.year, month, day))
                season.dates.add(d)
                self.context['dates'][k] = d
            
        for plant_data in data['plants']:
            self.handle_plant(plant_data)
        
        
    def handle_plant(self, data):
        with model.env.write():
            plant = model.Plant(name=data['name'])
        for variety_data in data.get('varieties', []):
            v = self.get_variety(variety_data)
            with model.env.write():
                plant.varieties.add(v)
        
        
    def get_variety(self, data):
        with model.env.write():
            v = model.PlantVariety(
                name=data.get('name'),
                catalog_url=data.get('catalog'),
                spacing=data.get('spacing'),
                thinned_spacing=data.get('thin'),
                depth=data.get('depth'),
                notes=data.get('notes')
            )
        
        for sow_data in data.get('sow'):
            sowing = self.get_sowing(sow_data)
            with model.env.write():
                v.sowings.add(sowing)
        
        for harvest_data in data.get('harvest', []):
            harvesting = self.get_harvesting(harvest_data)
            with model.env.write():
                v.harvestings.add(harvesting)
        
        return v
            
            
    def get_sowing(self, data):
        with model.env.write():
            sowing = model.Sowing(
                where=data.get('where'),
                notes=data.get('notes')
            )
            for k in ['start','stop','repeat','transplant']:
                delta_data = data.get(k)
                if delta_data:
                    setattr(sowing, k, self.get_date_delta(delta_data))
        return sowing
        
        
    def get_harvesting(self, data):
        with model.env.write():
            harvesting = model.Harvesting(
                notes=data.get('notes')
            )
            for k in ['start','stop','repeat']:
                delta_data = data.get(k)
                if delta_data:
                    setattr(harvesting, k, self.get_date_delta(delta_data))
        return harvesting
            
        
    def get_date_delta(self, data):
        with model.env.write():
            delta = model.GardenDateDelta(
                days=data.get('days'),
                weeks=data.get('weeks'),
                months=data.get('months')
            )
            before = self.context['dates'].get(data.get('before'))
            if before:
                delta.before = before
            after = self.context['dates'].get(data.get('after'))
            if after:
                delta.after = after
        
        return delta
        