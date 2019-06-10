from flask import Blueprint, jsonify, request
from farmapi import db
from farmapi.farm.models import House, Condition, Harvest, Crop, Day, Activities
from farmapi.farm.models import HouseSchema, CropSchema, DaySchema
from farmapi.farm.models import ConditionSchema, HarvestSchema, ActivitiesSchema


farmapi = Blueprint('farmapi', __name__)

"""
Initialize Schemas
"""
house_schema = HouseSchema(strict=True)
houses_schema = HouseSchema(many=True, strict=True)
crop_schema = CropSchema(strict=True)
crops_schema = CropSchema(many=True, strict=True)
days_schema = DaySchema(many=True, strict=True)
day_schema = DaySchema(strict=True)
condition_schema = ConditionSchema(strict=True)
conditions_schema = ConditionSchema(many=True, strict=True)
harvest_schema = HarvestSchema(strict=True)
activity_schema = ActivitiesSchema(strict=True)
activities_schema = ActivitiesSchema(many=True, strict=True)


@farmapi.route('/')
@farmapi.route('/home', methods=['OPTIONS', 'GET'])
def home():
    return jsonify({"Products": "From The Farm"})


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


@farmapi.route('/get/houses')
def get_houses():
    houses = House.query.all()
    if not houses:
        return jsonify({"Message": "No Houses Created"}), 404
    result = houses_schema.dump(houses)
    return jsonify(result.data)


@farmapi.route('/get/<house_name>')
def get_house(house_name):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "The house {} is not present".format(house_name)}), 404
    return house_schema.jsonify(house)


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


@farmapi.route('/get/crops/<house_name>')
def get_crops(house_name):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "The house {} does not exist".format(house)}), 404
    crop = house.crop.all()
    result = crops_schema.dump(crop)
    return jsonify(result.data)


@farmapi.route('/get/crop/<house_name>/<crop_no>')
def get_crop(house_name, crop_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop {} of house {} not found".format(crop_no, house_name)}), 404
    return crop_schema.jsonify(crop)


@farmapi.route('/get/days/<house_name>/<crop_no>')
def get_days(house_name, crop_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop {} of house {} not found".format(crop_no, house_name)}), 404

    days = crop.day.all()
    result = days_schema.dump(days)
    return jsonify(result.data)


@farmapi.route('/day', methods=['POST'])
def add_day():
    house_name = request.json['house']
    day_no = request.json['day']
    crop_no = request.json['crop_no']
    date = request.json['date']
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop {} of house {} not found".format(crop_no, house_name)}), 404
    day_chk = crop.day.filter_by(day=day_no).first()
    if day_chk:
        return jsonify({"Message": "Day {} of the crop {} is present".format(day_no, crop_no)})

    day = Day(crop, day_no, date)
    db.session.add(day)
    db.session.commit()
    return day_schema.jsonify(day), 201


@farmapi.route('/day/<house_name>/<crop_no>/<day_no>')
def get_day(house_name, crop_no, day_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House not present"}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop not present"}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day not present"}), 404

    return day_schema.jsonify(day)


"""
House Condition Routes
"""
@farmapi.route('/condition/<house_name>/<crop_no>/<day_no>')
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
    return jsonify(result.data)


@farmapi.route('/condition/<house_name>/<crop_no>')
def get_condition_crop(house_name, crop_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House not present"}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop not present"}), 404
    days = crop.day.all()
    condDays = {}
    i = 0
    for day in days:
        cond = day.condition.all()
        rst = conditions_schema.dump(cond)
        if rst.data:
            condDays[day.day] = rst.data[0]
        elif not rst.data and not condDays:
            return jsonify({"Message": "No conditions update as yet"}), 404
        i += 1
    return jsonify(condDays)


@farmapi.route('/condition', methods=['POST'])
def add_condition():
    house = request.json['house']
    crop_no = request.json['crop_no']
    day_no = request.json['day']
    time = request.json['time']
    temp = request.json['temperature']
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
    test_cond = day.condition.all()
    if test_cond:
        return jsonify({"Message": "Data already filled"}), 404

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
    if not harvest:
        return jsonify({"Message": "No harvest record for day %s" % day_no}), 404
    return harvest_schema.jsonify(harvest[0])


# Crop Harvest
@farmapi.route('/harvest/<house_name>/<crop_no>', methods=['GET'])
def get_harvest_crop(house_name, crop_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    days = crop.day.all()
    harvest_days = {}
    for day in days:
        day_no = day.day
        harv = day.harvest.all()
        if harv:
            punnets = harv[0].punnets
            harvest_days[day_no] = punnets
    return jsonify(harvest_days)


# POST daily harvest
@farmapi.route('/harvest', methods=['POST'])
def add_harvest():
    house_name = request.json['house']
    crop_no = request.json['crop_no']
    day_no = request.json['day_no']
    punnets = request.json['punnets']

    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day %s of crop number %s in house %s not found" % (day_no, crop_no, house_name)}), 404

    punnets_chk = day.harvest.all()
    if punnets_chk:
        return jsonify({"Message": "Harvest for day %s present, consider updating" % day_no})

    harvest = Harvest(day, punnets)
    db.session.add(harvest)
    db.session.commit()

    return harvest_schema.jsonify(harvest), 201


"""
Activities
"""
@farmapi.route('/activity', methods=['POST'])
def add_activity():
    house_name = request.json['house']
    crop_no = request.json['crop_no']
    day_no = request.json['day_no']
    description = request.json['activity']

    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day %s of crop number %s in house %s not found" % (day_no, crop_no, house_name)}), 404

    activity = Activities(day, description)
    db.session.add(activity)
    db.session.commit()

    return activity_schema.jsonify(activity)


@farmapi.route('/get/activities/<house_name>/<crop_no>')
def get_activities(house_name, crop_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404

    days = crop.day.all()
    actv_days = {}
    for day in days:
        day_no = day.day
        acts = day.activities.all()
        if acts:
            description = acts[0].description
            actv_days[day_no] = description
    return jsonify(actv_days)


@farmapi.route('/get/activity/<house_name>/<crop_no>/<day_no>')
def get_activity(house_name, crop_no, day_no):
    house = House.query.filter_by(name=house_name).first()
    if not house:
        return jsonify({"Message": "House {} not found".format(house_name)}), 404
    crop = house.crop.filter_by(crop_number=crop_no).first()
    if not crop:
        return jsonify({"Message": "Crop number %s not found for house %s" % (crop_no, house_name)}), 404
    day = crop.day.filter_by(day=day_no).first()
    if not day:
        return jsonify({"Message": "Day %s of crop number %s in house %s not found" % (day_no, crop_no, house_name)}), 404
    acts = day.activities.all()
    if not acts:
        return jsonify({"Message": "No activity record for day %s " % day_no}), 404
    return activity_schema.jsonify(acts[0])
