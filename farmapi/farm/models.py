from farmapi import db, ma


class House(db.Model):
    """
    The House Table
    name: Name of the house
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<House {}>'.format(self.name)


class Crop(db.Model):
    """
    The number of the crop
    crop_number: number of the crop
    crop_name: name of the crop
    house: house model
    start_date: Day one date
    """
    id = db.Column(db.Integer, primary_key=True)
    crop_number = db.Column(db.String(10), unique=True)
    crop_name = db.Column(db.String(30))
    start_date = db.Column(db.String)

    # Relationships
    house = db.relationship('House', backref=db.backref('crop', lazy='dynamic'))
    house_name = db.Column(db.String, db.ForeignKey('house.name'))

    def __init__(self, house, crop_name, crop_number, start_date):
        self.crop_number = crop_number
        self.crop_name = crop_name
        self.house = house
        self.start_date = start_date

    def __repr__(self):
        return '<Crop {}: {}: {}>'.format(self.crop_number, self.crop_name, self.house_name)


class Day(db.Model):
    """
    Day of the crop
    day: Day of the crop - String
    crop: The crop object
    """
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), unique=True)

    # Relationships
    crop = db.relationship('Crop', backref=db.backref('day', lazy='dynamic'))
    crop_number = db.Column(db.String, db.ForeignKey('crop.crop_number'))

    def __init__(self, crop, day):
        self.day = day
        self.crop = crop

    def __repr__(self):
        return '<Day {}>'.format(self.day)


class Condition(db.Model):
    """
    The Condition of the House
    temp: Temperature in degrees celcius
    humidity: Relative humidity
    time: Time the record was taken 'hh:min'
    day: Day in the crop calendar
    """
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float)
    humidity = db.Column(db.Float)
    time = db.Column(db.String(20))

    # Relationships
    day = db.relationship('Day', backref=db.backref('condition', lazy='dynamic'))
    day_no = db.Column(db.String, db.ForeignKey('day.day'))

    def __init__(self, day, temp, humidity, time):
        self.temp = temp
        self.humidity = humidity
        self.time = time
        self.day = day

    def __repr__(self):
        return '<Condition on day {}>'.format(self.day_no)


class Harvest(db.Model):
    """
    Harvest table
    panets: number of panets harvested in a day
    """
    id = db.Column(db.Integer, primary_key=True)
    panets = db.Column(db.Integer)

    # Relationships
    day = db.relationship('Day', backref=db.backref('harvest', lazy='dynamic'))
    day_no = db.Column(db.String, db.ForeignKey('day.day'))

    def __init__(self, day, panets):
        self.panets = panets
        self.day = day

    def __repr__(self):
        return '<Harvest {}>'.format(self.panets)


class Activities(db.Model):
    """"
    Holds the activities done
    day: Day object
    description: A short description of the activity
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    # Relationships
    house = db.relationship('House', backref=db.backref('activities', lazy='dynamic'))
    house_name = db.Column(db.String, db.ForeignKey('house.name'))
    crop = db.relationship('Crop', backref=db.backref('activities', lazy='dynamic'))
    crop_number = db.Column(db.String, db.ForeignKey('crop.crop_number'))
    day = db.relationship('Day', backref=db.backref('activities', lazy='dynamic'))
    day_no = db.Column(db.String, db.ForeignKey('day.day'))

    def __repr__(self):
        return '<Activity on {}>'.format(self.day)


# The Schemas for serialization
class CropSchema(ma.Schema):
    class Meta:
        fields = ('crop_name', 'crop_number', 'house_name', 'start_date')


class DaySchema(ma.Schema):
    class Meta:
        fields = ('day', 'crop_number')


class ConditionSchema(ma.Schema):
    class Meta:
        fields = ('temp', 'humidity', 'time', 'day_no')


class HarvestSchema(ma.Schema):
    class Meta:
        fields = ('panets', 'day_no')


class ActivitiesSchema(ma.Schema):
    class Meta:
        fields = ('crop_number', 'day_no', 'description')
