from typing import Optional, Dict, Any
from dataclasses import dataclass, fields
from enum import Enum
import pytz
from datetime import datetime

class TIME_RANGES(str, Enum):
    ONE_YEAR = "1year"
    SIX_MONTHS = "6months"
    THREE_MONTHS = "3months"

class CITIES(str, Enum):
    NEW_YORK = "newYork"
    LOS_ANGELES = "losAngeles"
    SEATTLE = "seattle"
    CHICAGO = "chicago"

@dataclass
class CityDataset:
    endpoint: str
    identifier: str
    datasetUrl: str
    apiEndpoint: str
    query: str
    
@dataclass
class UnifiedCrimeData:
    report_number: str
    incident_datetime: str
    reported_datetime: str
    offense_type: str
    offense_description: str
    victim_age: Optional[str]
    victim_sex: Optional[str]
    location_description: str
    longitude: str
    latitude: str

UnifiedCrimeDataFieldNames = [field.name for field in fields(UnifiedCrimeData)]

class CITY_DATA_MODELS:
    pass

def flexible_dataclass(cls):
    def __init(self, **kwargs):
        for field in fields(cls):
            setattr(self, field.name, kwargs.get(field.name, field.default))
        self.__dict__.update({k: v for k, v in kwargs.items() if k not in {f.name for f in fields(cls)}})
    cls.__init__ = __init
    return dataclass(cls)

# Define timezones for each city
NYC_TIMEZONE = pytz.timezone('America/New_York')
LA_TIMEZONE = pytz.timezone('America/Los_Angeles')
SEATTLE_TIMEZONE = pytz.timezone('America/Los_Angeles')
CHICAGO_TIMEZONE = pytz.timezone('America/Chicago')

@flexible_dataclass
class NewYorkCrimeData(CITY_DATA_MODELS):
    cmplnt_num: str = ""
    addr_pct_cd: str = ""
    boro_nm: str = ""
    cmplnt_fr_dt: str = ""
    cmplnt_fr_tm: str = ""
    cmplnt_to_dt: str = ""
    cmplnt_to_tm: str = ""
    crm_atpt_cptd_cd: str = ""
    hadevelopt: str = ""
    jurisdiction_code: str = ""
    juris_desc: str = ""
    ky_cd: str = ""
    law_cat_cd: str = ""
    loc_of_occur_desc: str = ""
    ofns_desc: str = ""
    parks_nm: str = ""
    patrol_boro: str = ""
    pd_cd: str = ""
    pd_desc: str = ""
    prem_typ_desc: str = ""
    rpt_dt: str = ""
    station_name: str = ""
    susp_age_group: str = ""
    susp_race: str = ""
    susp_sex: str = ""
    vic_age_group: str = ""
    vic_race: str = ""
    vic_sex: str = ""
    x_coord_cd: str = ""
    y_coord_cd: str = ""
    latitude: str = ""
    longitude: str = ""
    lat_lon: Dict[str, str] = None
    geocoded_column: Dict[str, Any] = None

    def transform(self) -> UnifiedCrimeData:
        incident_dt = datetime.strptime(f"{self.cmplnt_fr_dt or ''}".strip(), "%Y-%m-%dT%H:%M:%S.%f").astimezone(NYC_TIMEZONE)
        reported_dt = datetime.strptime(self.rpt_dt or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(NYC_TIMEZONE)
        
        return UnifiedCrimeData(
            report_number=self.cmplnt_num or "",
            incident_datetime=incident_dt,
            reported_datetime=reported_dt,
            offense_type=self.law_cat_cd or "",
            offense_description=self.ofns_desc or "",
            victim_age=self.vic_age_group or "",
            victim_sex=self.vic_sex or "",
            location_description=self.loc_of_occur_desc or "",
            longitude=self.longitude or "",
            latitude=self.latitude or ""
        )
    pass

@flexible_dataclass
class LosAngelesCrimeData(CITY_DATA_MODELS):
    dr_no: str = ""
    date_rptd: str = ""
    date_occ: str = ""
    time_occ: str = ""
    area: str = ""
    area_name: str = ""
    rpt_dist_no: str = ""
    part_1_2: str = ""
    crm_cd: str = ""
    crm_cd_desc: str = ""
    mocodes: str = ""
    vict_age: str = ""
    vict_sex: str = ""
    vict_descent: str = ""
    premis_cd: str = ""
    premis_desc: str = ""
    weapon_used_cd: str = ""
    weapon_desc: str = ""
    status: str = ""
    status_desc: str = ""
    crm_cd_1: str = ""
    crm_cd_2: str = ""
    crm_cd_3: str = ""
    crm_cd_4: str = ""
    location: str = ""
    cross_street: str = ""
    lat: str = ""
    lon: str = ""

    def transform(self) -> UnifiedCrimeData:
        incident_dt = datetime.strptime(f"{self.date_occ or ''}".strip(), "%Y-%m-%dT%H:%M:%S.%f").astimezone(LA_TIMEZONE)
        reported_dt = datetime.strptime(self.date_rptd or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(LA_TIMEZONE)

        return UnifiedCrimeData(
            report_number=self.dr_no or "",
            incident_datetime=incident_dt,
            reported_datetime=reported_dt,
            offense_type=self.crm_cd_desc or "",
            offense_description=self.crm_cd_desc or "",
            victim_age=self.vict_age or "",
            victim_sex=self.vict_sex or "",
            location_description=self.premis_desc or "",
            longitude=self.lon or "",
            latitude=self.lat or ""
        )
    pass

@flexible_dataclass
class SeattleCrimeData(CITY_DATA_MODELS):
    report_number: str = ""
    offense_id: str = ""
    offense_start_datetime: str = ""
    report_datetime: str = ""
    group_a_b: str = ""
    crime_against_category: str = ""
    offense_parent_group: str = ""
    offense: str = ""
    offense_code: str = ""
    precinct: str = ""
    sector: str = ""
    beat: str = ""
    mcpp: str = ""
    _100_block_address: str = ""
    longitude: str = ""
    latitude: str = ""

    def transform(self) -> UnifiedCrimeData:
        incident_dt = datetime.strptime(self.offense_start_datetime or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(SEATTLE_TIMEZONE)
        reported_dt = datetime.strptime(self.report_datetime or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(SEATTLE_TIMEZONE)

        return UnifiedCrimeData(
            report_number=self.report_number or "",
            incident_datetime=incident_dt,
            reported_datetime=reported_dt,
            offense_type=self.offense_parent_group or "",
            offense_description=self.offense or "",
            victim_age="",
            victim_sex="",
            location_description=self._100_block_address or "",
            longitude=self.longitude or "",
            latitude=self.latitude or ""
        )
    pass

@flexible_dataclass
class ChicagoCrimeData(CITY_DATA_MODELS):
    id: str = ""
    case_number: str = ""
    date: str = ""
    block: str = ""
    iucr: str = ""
    primary_type: str = ""
    description: str = ""
    location_description: str = ""
    arrest: bool = False
    domestic: bool = False
    beat: str = ""
    district: str = ""
    ward: str = ""
    community_area: str = ""
    fbi_code: str = ""
    x_coordinate: str = ""
    y_coordinate: str = ""
    year: str = ""
    updated_on: str = ""
    latitude: str = ""
    longitude: str = ""
    location: Dict[str, str] = None

    def transform(self) -> UnifiedCrimeData:
        incident_dt = datetime.strptime(self.date or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(CHICAGO_TIMEZONE)
        reported_dt = datetime.strptime(self.updated_on or "", "%Y-%m-%dT%H:%M:%S.%f").astimezone(CHICAGO_TIMEZONE)

        return UnifiedCrimeData(
            report_number=self.case_number or "",
            incident_datetime=incident_dt,
            reported_datetime=reported_dt,
            offense_type=self.primary_type or "",
            offense_description=self.description or "",
            victim_age="",
            victim_sex="",
            location_description=self.location_description or "",
            longitude=self.longitude or "",
            latitude=self.latitude or ""
        )
    pass

@dataclass
class CityDatasets:
    newYork: CityDataset
    losAngeles: CityDataset
    seattle: CityDataset
    chicago: CityDataset