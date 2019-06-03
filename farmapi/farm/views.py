from flask import Blueprint, jsonify, request, make_response
from farmapi import db
from farmapi.farm.models import House, Condition, Harvest, Crop, Day
from farmapi.farm.models import DaySchema, CropSchema
from farmapi.farm.models import ConditionSchema, HarvestSchema


farmapi = Blueprint('farmapi', __name__)

"""
Initialize Schemas
"""
crop_schema = CropSchema(strict=True)
day_schema = DaySchema(strict=True)
condition_schema = ConditionSchema(strict=True)
conditions_schema = ConditionSchema(many=True, strict=True)
harvest_schema = HarvestSchema(strict=True)


@farmapi.route('/')
@farmapi.route('/home', methods=['OPTIONS', 'GET'])
def home():
    return jsonify({"Products": "From The Farm"})


"""
The next three routes are all POST.
They initialize the house, crop and day of the crop
"""
@farmapi.route('/house', methods=['POST'])
def add_house():
    house_name = request.json['house']
    house_chk = House.query.filter_by(name=house_name).first()
    if not house_chk:
        house = House(house_name)
        db.session.add(house)
        db.session.commit()
        return jsonify({"House": house_name}), 201
    return jsonify({"Message": "House Present"})


@farmapi.route('/crop', methods=['POST'])
def add_crop():
    house_name = request.json['house']
    crop_no = request.json['crop_no']
    crop_name = request.json['crop_name']
    start_date = request.json['start_date']

    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "The house {} is not present".format(house_name)}), 404

    crop_chk = house.crop.filter_by(crop_number=crop_no).first()
    if crop_chk:
        return jsonify({"Message": "Crop Number Present"})

    crop = Crop(house, crop_name, crop_no, start_date)
    db.session.add(crop)
    db.session.commit()
    return crop_schema.jsonify(crop), 201


@farmapi.route('/day', methods=['POST'])
def add_day():
    house_name = request.json['house']
    day_no = request.json['day']
    crop_no = request.json['crop_no']
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop {} of house {} not found".format(crop_no, house_name)}), 404
    day_chk = crop.day.filter_by(day=day_no).first()
    if day_chk:
        return jsonify({"Message": "Day {} of the crop {} is present".format(day_no, crop_no)})
    day = Day(crop, day_no)
    db.session.add(day)
    db.session.commit()
    return day_schema.jsonify(day), 201


"""
House Condition Routes
"""
@farmapi.route('/condition/<house_name>/<crop_no>/<day_no>', methods=['GET'])
def get_condition(house_name, crop_no, day_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House not present"}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop not present"}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day not present"}), 404
    condition = day.condition.all()
    if not condition:
        return jsonify({"Message": "No condition update"}), 404
    result = conditions_schema.dump(condition)
    # app.logger.info(type(result.data))
    return jsonify(result.data)


@farmapi.route('/condition', methods=['POST'])
def add_condition():
    house = request.json['house']
    crop_no = request.json['crop_no']
    day_no = request.json['day']
    time = request.json['time']
    temp = request.json['temp']
    humidity = request.json['humidity']
    house_name = House.query.filter_by(name=house).first()
    if not house_name:
        return jsonify({"Message": "The house {} does not exist".format(house)}), 404
    crop = house_name.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "The Crop {} does not exist".format(crop_no)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "The day does not exist"}), 404
    time_chk = day.condition.filter_by(time=time).first()
    if time_chk:
        return jsonify({"Message": "Data already filled"})

    cond = Condition(day, temp, humidity, time)
    db.session.add(cond)
    db.session.commit()
    return condition_schema.jsonify(cond), 201


"""
Harvest routes
"""
# Single day harvest
@farmapi.route('/harvest/<house_name>/<crop_no>/<day_no>', methods=['GET'])
def get_harvest_day(house_name, crop_no, day_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day %s of crop number %s in house %s not found" % (day_no, crop_no, house_name)})

    harvest = day.harvest.all()
    return harvest_schema.jsonify(harvest[0])


# Crop Harvest
@farmapi.route('/harvest/<house_name>/<crop_no>', methods=['GET'])
def get_harvest_crop(house_name, crop_no):
    pass


# POST daily harvest
@farmapi.route('/harvest/<house_name>/<crop_no>', methods=['POST'])
def add_harvest(house_name, crop_no):
    day_no = request.json['day_no']
    panets = request.json['panets']

    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day %s of crop number %s in house %s not found" % (day_no, crop_no, house_name)})

    panets_chk = day.harvest.all()
    if panets_chk:
        return jsonify({"Message": "Harvest for day %s present, consider updating" % day_no})

    harvest = Harvest(day, panets)
    db.session.add(harvest)
    db.session.commit()

    return harvest_schema.jsonify(harvest), 201
