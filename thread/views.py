import time
import requests
import concurrent.futures
from django.http import JsonResponse  # Import JsonResponse to return a JSON response
from rest_framework.response import Response
from rest_framework import viewsets
from django.views import View
from rest_framework import generics
from adrf.views import APIView


# Define the URLs of the sample APIs you want to test
class Concurrent(APIView):

    def get(self, request):  # Change 'requests' to 'request'
        start = time.time()

        def fetch_data(url):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}

        api_urls = ['https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries']
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(fetch_data, api_urls))

        data=[{"data": result} for result in results]  # Create a response data dictionary
        end = time.time()
        total= end-start
        ans = {"data": data, "total": total}
        return Response(ans)

import asyncio
import nest_asyncio
import requests


class Asyncio(APIView):
    # def __init__(self):
    #     nest_asyncio.apply()
    async def get(self,request):
        start = time.time()
        async def fetch_data1(url):
            response = await asyncio.to_thread(requests.get, url)
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}
        api_urls = ['https://api.publicapis.org/entries',
                    'https://catfact.ninja/fact',
                    'https://api.coindesk.com/v1/bpi/currentprice.json',
                    'https://www.boredapi.com/api/activity']
        tasks = [fetch_data1(url) for url in api_urls]
        results = await asyncio.gather(*tasks)
        data=[{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response(ans)
#
# if __name__ == '__main__':
#     asyncio_example = AsyncioExample()
#     asyncio.run(asyncio_example.main())



import asyncio
import multiprocessing


# import aiohttp
# async def fetch_data_wrapper(url):
#     loop = asyncio.get_event_loop()
#     return await loop.run_in_executor(None, lambda: fetch_data2(url))

def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()


class Multiprocessing(APIView):

    def get(self,requests):
        start = time.time()

        api_urls = ['https://api.publicapis.org/entries',
                    'https://catfact.ninja/fact',
                    'https://api.coindesk.com/v1/bpi/currentprice.json',
                    'https://www.boredapi.com/api/activity']
        with multiprocessing.Pool(processes=len(api_urls)) as pool:
            results = pool.map(fetch_data, api_urls)
        end = time.time()
        total = end - start
        data = [{"data": result} for result in results]
        ans={"data":data,"total":total}
        return Response(ans)

import aiohttp
import asyncio


class Aiohttp(APIView):
    async def get(self,requests):
        start = time.time()
        async def fetch_data3(url):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    return {'error': f'Failed to retrieve data from {url}'}

        api_urls = ['https://api.publicapis.org/entries',
                    'https://catfact.ninja/fact',
                    # 'https://api.coindesk.com/v1/bpi/currentprice.json',
                    'https://www.boredapi.com/api/activity']
        tasks = [fetch_data3(url) for url in api_urls]
        results = await asyncio.gather(*tasks)
        end = time.time()
        total = end - start
        data = [{"data": result} for result in results]
        ans = {"data": data, "total": total}
        return Response(ans)


import httpx


class Httpx(APIView):
    async def get(self,requests):
        start = time.time()
        async def fetch_data4(url):
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
                return {'error': f'Failed to retrieve data from {url}'}
        api_urls = ['https://api.publicapis.org/entries',
                    'https://catfact.ninja/fact',
                    'https://api.coindesk.com/v1/bpi/currentprice.json',
                    'https://www.boredapi.com/api/activity']
        tasks = [fetch_data4(url) for url in api_urls]
        results = await asyncio.gather(*tasks)
        data = [{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response(ans)


from rest_framework import views
from rest_framework import status
import requests
import random
import string
from django.db import connection


class InsertApiData(views.APIView):
    def get(self, request):
        start = time.time()
        def fetch_data(url):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}

        api_urls = ['https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries',
                    'https://api.publicapis.org/entries',
                   # 'https://api.publicapis.org/entries',
                    # 'https://api.publicapis.org/entries',
                    ]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(fetch_data, api_urls))
        data = [result for result in results]  # Create a response data dictionary

        def generate_api_id():
            api_id = "API"+"".join(random.choice(string.digits) for i in range(6))
            cursor.execute("SELECT api_id FROM apis WHERE api_id=%s", (api_id,))
            db_id = cursor.fetchone()
            if not db_id:
                return api_id
            else:
                api_id = generate_api_id()
                return api_id

        # Insert data into the DBeaver table using raw queries
        with connection.cursor() as cursor:
            for i in range(len(data)):
                api_data = data[i]['entries']
                for item in api_data:
                    # api_id = generate_api_id()
                    raw_query = f"INSERT INTO apis (api_id, api, Description, Auth, HTTPS, Cors, Link, Category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    params = (generate_api_id(), item["API"], item["Description"], item["Auth"], item["HTTPS"], item["Cors"], item["Link"], item["Category"])
                    cursor.execute(raw_query, params)
        end =time.time()
        tot = end-start
        val = {"total":tot, "data":"Data inserted successfully"}
        return Response(val, status=status.HTTP_201_CREATED)


class InsertPageApiData(views.APIView):
    def get(self, request):
        start = time.time()

        def insert_data(data):
            with connection.cursor() as cursor:
                api_data = data
                for item in api_data:
                    # api_id = generate_api_id()
                    raw_query = """
                                    INSERT INTO pagination (
                                        api_id, id, name, tagline, first_brewed, description, image_url, 
                                        abv, ibu, target_fg, target_og, ebc, srm, ph, attenuation_level, 
                                        volume, boil_volume, method, ingredients, food_pairing, 
                                        brewers_tips, contributed_by
                                    ) VALUES (
                                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                                        %s, %s, %s, %s, %s, %s
                                    )
                                """
                    params = (
                        generate_api_id(),
                        item["id"],
                        item["name"],
                        item["tagline"],
                        item["first_brewed"],
                        item["description"],
                        item["image_url"],
                        item["abv"],
                        item["ibu"],
                        item["target_fg"],
                        item["target_og"],
                        item["ebc"],
                        item["srm"],
                        item["ph"],
                        item["attenuation_level"],
                        str(item["volume"]),
                        str(item["boil_volume"]),
                        str(item["method"]),
                        str(item["ingredients"]),
                        str(item["food_pairing"]),
                        item["brewers_tips"],
                        item["contributed_by"]
                    )

                    cursor.execute(raw_query, params)
        def generate_api_id():
            with connection.cursor() as cursor:
                api_id = "API"+"".join(random.choice(string.digits) for i in range(6))
                cursor.execute("SELECT api_id FROM pagination WHERE api_id=%s", (api_id,))
                db_id = cursor.fetchone()
                if not db_id:
                    return api_id
                else:
                    api_id = generate_api_id()
                    return api_id

        def fetch_data(url):
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(data)
                insert_data(data)
                return {"message": "success"}
            return {'error': f'Failed to retrieve data from {url}'}

        api_urls = ['https://api.punkapi.com/v2/beers/',
                    'https://api.punkapi.com/v2/beers/',
                    'https://api.punkapi.com/v2/beers/',
                    ]

        def page(url):
            for i in range(1, 11):
                api_url = str(url)+str(i)
                fetch_data(api_url)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(page, api_urls))

        # data = [result for result in results]  # Create a response data dictionary

        end = time.time()
        tot = end - start
        val = {"total": tot, "data": "Data inserted successfully"}

        return Response(val, status=status.HTTP_201_CREATED)
