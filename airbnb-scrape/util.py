import csv
import traceback
import MySQLdb
import MySQLdb.cursors as cursors
import os
import json

NUMBER = "number"
SW_LATT = "sw_lattitude"
SW_LNG = "sw_longitude"
NE_LATT = "ne_lattitude"
NE_LNG = "ne_longitude"
HOUSE_NO = "house_no"
STREET = "street"
CITY = "city"
STATE = "state"
COUNTRY = "country"
ZIPCODE = "zipcode"
PROP_NAME = "property_name"
PROP_URL = "property_url"
BEDROOMS = "no_bed_rooms"
BEDS = "no_beds"
BATHROOMS = "no_bathrooms"
MAX_PPL = "max_no_people"
NIGHT_MIN_STAY = "no_nights_min_stay"
CLEANING_FEE = "cleaning_fee"
SEC_DEPOSIT = "security_deposit"
WEEKLY_DIS = "weekly_discount"
MONTHLY_DIS = "monthly_discount"
EXTRA_PER_NIGHT = "extra_price_per_night"
EXTRA_AFTER_PPL_NO = "extra_after_no_people"
PRICE_PER_1 = "price_per_1"
PRICE_PER_3 = "price_per_3"
PRICE_PER_20 = "price_per_20"
PRICE_PER_ = "PRICE_PER_"
MAX_NO = 20 + 1
RESERVED_DAYS_12_MONTHS = "reserved_12_months"

def log(msg):
    print msg

def generate_headers(for_db = False):
    headers = [NUMBER, SW_LATT, SW_LNG, NE_LATT, NE_LNG, HOUSE_NO, STREET, CITY, STATE, ZIPCODE, PROP_NAME, PROP_URL, BEDROOMS, BEDS, BATHROOMS, MAX_PPL,
               NIGHT_MIN_STAY,  CLEANING_FEE, SEC_DEPOSIT, WEEKLY_DIS, MONTHLY_DIS, EXTRA_PER_NIGHT, EXTRA_AFTER_PPL_NO]
    if not for_db:
        headers.append(PRICE_PER_1)
        headers.append(PRICE_PER_3)
        headers.append(PRICE_PER_20)
    else:
        for i in range(1,MAX_NO):
            headers.append(PRICE_PER_ + str(i))

    headers.append(RESERVED_DAYS_12_MONTHS)
    return headers

REC_ID = 0

class HouseModel(object):
    def __init__(self):
        self.INPUT = ""
        global REC_ID
        REC_ID += 1
        self.NUMBER = REC_ID
        self.SW_LATT = "NA"
        self.SW_LNG = "NA"
        self.NE_LATT = "NA"
        self.NE_LNG = "NA"
        self.HOUSE_NO = "NA"
        self.STREET = "NA"
        self.CITY = "NA"
        self.STATE = "NA"
        self.COUNTRY = "NA"
        self.ZIPCODE = "NA"
        self.PROP_NAME = "NA"
        self.PROP_URL = "NA"
        self.BEDROOMS = "NA"
        self.BEDS = "NA"
        self.BATHROOMS = "NA"
        self.MAX_PPL = "NA"
        self.NIGHTS_MIN_STAY = "NA"
        self.CLEANING_FEE = "NA"
        self.SECURITY_DEPOSIT = "NA"
        self.WEEKLY_DIS = "NA"
        self.MONTHLY_DIS = "NA"
        self.EXTRA_PRICE_NIGHT = "NA"
        self.EXTRA_AFTER_PPL = "NA"
        self.PRICES_PER_ALL = [] # for 20 people
        for i in range(1,MAX_NO):
            self.PRICES_PER_ALL.append("NA")
        self.RESERVED_DAYS_12_MONTHS = "NA"

    def get_json(self,for_db=False):
        t = self
        d = {}
        d[NUMBER] = t.NUMBER
        d[SW_LATT] = t.SW_LATT
        d[SW_LNG] = t.SW_LNG
        d[NE_LATT] = t.NE_LNG
        d[NE_LNG] = t.NE_LNG
        d[HOUSE_NO] = t.HOUSE_NO
        d[STREET] = t.STREET
        d[CITY] = t.CITY
        d[STATE] = t.STATE
        d[ZIPCODE] = t.ZIPCODE
        if type(t.PROP_NAME) == type(u''):
            t.PROP_NAME = t.PROP_NAME.encode("utf-8")
        d[PROP_NAME] = t.PROP_NAME
        d[PROP_URL] = t.PROP_URL
        d[BEDROOMS] = t.BEDROOMS
        d[BEDS] = t.BEDS
        d[BATHROOMS] = t.BATHROOMS
        d[MAX_PPL] = t.MAX_PPL
        d[NIGHT_MIN_STAY] = t.NIGHTS_MIN_STAY
        d[CLEANING_FEE] = t.CLEANING_FEE
        d[SEC_DEPOSIT] = t.SECURITY_DEPOSIT
        d[WEEKLY_DIS] = t.WEEKLY_DIS
        d[MONTHLY_DIS] = t.MONTHLY_DIS
        d[EXTRA_PER_NIGHT] = t.EXTRA_PRICE_NIGHT
        d[EXTRA_AFTER_PPL_NO] = t.EXTRA_AFTER_PPL
        if not for_db:
            d[PRICE_PER_1] = str(t.PRICES_PER_ALL[0])
            d[PRICE_PER_3] = str(t.PRICES_PER_ALL[2])
            d[PRICE_PER_20] = str(t.PRICES_PER_ALL[19])
        else:
            for i in range(1,MAX_NO):
                d[PRICE_PER_ + str(i)] = str(t.PRICES_PER_ALL[i-1])

        d[RESERVED_DAYS_12_MONTHS] = t.RESERVED_DAYS_12_MONTHS

        return d

def isnumber(str_):
    for i in str_:
        if not i.isdigit():
            return False
    return True


class AirbnbDB(object):
    def __init__(self,db_url,username,password,database,table):
        self.database = database
        self.table = table
        self.db = MySQLdb.connect(db_url,username,password, cursorclass=cursors.SSCursor)
        cursor = self.db.cursor()
        if database == None or database.strip() == "":
            log("Error: Please provide database in config.json")
            raise KeyError
        create_db_sql = "CREATE DATABASE IF NOT EXISTS " + self.database
        cursor.execute(create_db_sql)
        cursor.execute("use " + database)
        self.db = MySQLdb.connect(db_url,username,password)
        columns = generate_headers(for_db=True)
        sql_str = ""
        for col in columns:
            if col == NUMBER:
                sql_str = sql_str + col + " int(10) PRIMARY KEY AUTO_INCREMENT, "
                continue
            if col == RESERVED_DAYS_12_MONTHS:
                sql_str = sql_str + col + " text, "
                continue
            sql_str = sql_str + col + " varchar(100), "
        sql_str = sql_str.strip(" ")
        sql_str = sql_str.strip(",")
        create_table_sql = "CREATE TABLE IF NOT EXISTS " + self.table + "(" \
                            + sql_str + \
                            ")"
        cursor.execute(create_table_sql)
        cursor.close()
    def close(self):
        try:
            self.db.close()
        except Exception as e:
            log("Error while closing DB, error: " + str(e))

    def retrieve_and_wrtie_to_csv(self, file_name, latest_num):
        try:
            with open(file_name, "wb") as fp:
                cursor  = self.db.cursor()
                cursor.execute("USE " + self.database)
                sql_txt = "SELECT " + ",".join(generate_headers())
                sql_txt = sql_txt + " FROM {} WHERE {} > {}".format(self.table, NUMBER, latest_num)
                cursor.execute(sql_txt)
                headers = [i[0] for i in cursor.description]
                writer = csv.DictWriter(fp, fieldnames=headers)
                writer.writeheader()
                for row in cursor:
                    try:
                        data = {}
                        for i in range(len(headers)):
                            data[headers[i]] = row[i]
                        writer.writerow(data)
                    except Exception as e:
                        traceback.print_exc()
                        log("Error while writing to CSV file..., data: " + str(row))
                log("Successfully wrote to CSV file..." + file_name)
        except Exception as e:
            log("Error while writing to CSV file...")
            traceback.print_exc()
        finally:
            cursor.close()

    def get_latest_num(self):
        latest_num = None
        try:
            cursor = self.db.cursor()
            cursor.execute("USE " + self.database)
            sql_txt = "SELECT MAX({}) FROM {} ".format(NUMBER, self.table)
            cursor._query(sql_txt)
            res = cursor.fetchone()
            if res is not None:
                latest_num = 0
                if len(res) > 0:
                    if res[0] != None:
                        latest_num = int(res[0])
            return latest_num
        except Exception as e:
            log("Error occured while reading latest record ID form database")
            traceback.print_exc()
            return latest_num
        finally:
            cursor.close()

    def write_to_db(self, res):
        try:
            cursor = self.db.cursor()
            cursor.execute("USE " + self.database)
            data = res.get_json(for_db=True)
            del data[NUMBER]
            cols_txt = ""
            vals_txt = ""
            sql_txt = ""
            update_txt = ""
            for key,value in data.items():
                value = unicode(value)
                value = value.encode("utf-8")
                if "'" in value:
                    value = value.replace("'","\\'")
                cols_txt = cols_txt + str(key) + ","
                vals_txt = vals_txt + "'" + value.strip() + "',"
                update_txt = update_txt + "{} = '{}',".format(str(key),value.strip())
            cols_txt = cols_txt.strip(",")
            vals_txt = vals_txt.strip(",")
            update_txt = update_txt.strip(",")
            cursor._query("SELECT {} FROM {} WHERE {} = '{}'".format(NUMBER,self.table,PROP_URL,data[PROP_URL]).strip())
            res = cursor.fetchone()
            if res is not None:
                number = res[0]
                sql_txt = "UPDATE {} set {} WHERE {} = {}".format(self.table,update_txt,NUMBER,number)
            else:
                sql_txt = "INSERT INTO {} ({}) VALUES ({})".format(self.table,cols_txt,vals_txt)
            res = cursor.execute(sql_txt)
            cursor.close()
            log("Successfully inserted/updated to DB.")
            self.db.commit()
        except:
            log("Error: while writing to DB, sql: " + str(data))
            traceback.print_exc()

def initialize(config_file):
    if not os.path.exists(config_file):
        log("Error: DB Config file does not exists")
        return None
    try:
        with open(config_file, "r") as fp:
            data = json.load(fp)
        input_file = data["input_file"]
        output_file = data["output_file"]
        db_obj = AirbnbDB(data["db_url"],data["username"],data["password"],data["database"],data["db_table"])
        return (input_file,output_file,db_obj)
    except Exception as e:
        traceback.print_exc()
        return None