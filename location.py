import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datawire.settings")
django.setup()

from authApp.models import Regions

import pandas as pd

def resolve_seed_data():

    df=pd.read_csv('/Users/macbook/Downloads/country.csv')

    row_iter = df.iterrows()

    for index, row in row_iter:

        Regions.objects.update_or_create(
            name=row['value'],
        )

        print(index," : " ,row['value'])

    return ""

    #Region 

    # df=pd.read_csv('/home/egovridc/Desktop/NIRC/Backend/nircmis_uaaa/nircmis_office_settings/Reginals.csv')

    # row_iter = df.iterrows()

    # for index, row in row_iter:

    #     Regions.objects.update_or_create(
    #         reginal_name=row['reginal_name'],
    #         reginal_napa_id=row['reginal_uniqueID'],
    #         reginal_postcode=row['reginal_code'],
    #     )

    
    # return ""

    # District

    # df=pd.read_csv('/home/masasijr/PROJECTS/NRIC/Backend/nircmis_uaaa/nircmis_office_settings/locations/Districs.csv')


    # row_iter = df.iterrows()

    # for index, row in row_iter:
    #     region=Regions.objects.filter(reginal_napa_id=row['parent_region']).first()
    #     if region is None:
    #         continue
    #     existing_district = Districs.objects.filter(district_name=row['distric_name']).exists()
    #     if existing_district:
    #         continue

    #     Districs.objects.update_or_create(
    #         district_name=row['distric_name'],
    #         district_napa_id=row['distric_uniqueID'],
    #         district_postcode=row['distric_code'],
    #         district_parent_region=region
    #     )
    #     print("created")

    # return ""

    # Wards

    # df=pd.read_csv('/home/masasijr/PROJECTS/NRIC/Backend/nircmis_uaaa/nircmis_office_settings/locations/Wards.csv')


    # row_iter = df.iterrows()

    # for index, row in row_iter:
    #     district=Districs.objects.filter(district_napa_id=row['parent_distric']).first()
    #     if district is None:
    #         continue
    #     existing_ward = Wards.objects.filter(ward_name=row['ward_name']).exists()
    #     if existing_ward:
    #         continue

    #     Wards.objects.update_or_create(
    #         ward_name=row['ward_name'],
    #         ward_napa_id=row['ward_uniqueID'],
    #         ward_postcode=row['ward_code'],
    #         ward_parent_distric=district
    #     )
    #     print("created")

    # return ""

    # return ""


    # Streets

    # df=pd.read_csv('//home/egovridc/Desktop/NIRC/Backend/nircmis_uaaa/nircmis_office_settings/Streets.csv')
     
    # row_iter = df.iterrows()

    # for index, row in row_iter:
    #     wards=Wards.objects.filter(ward_napa_id=row['parent_ward']).first()
    #     if wards is None:
    #         continue
    #     existing_street = Streets.objects.filter(street_name=row['street_name']).exists()
    #     if existing_street:
    #         continue

    #     streets, success = Streets.objects.update_or_create(
    #         street_name=row['street_name'],
    #         street_napa_id=row['street_uniqueID'],
    #         street_postcode=row['street_code'],
    #         street_parent_ward=wards
    #     )

    #     print(index," : " ,success)
    # return ""

resolve_seed_data()