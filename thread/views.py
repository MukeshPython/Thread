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

        api_urls = ['https://jsonplaceholder.typicode.com/posts/1',
                    'https://jsonplaceholder.typicode.com/posts/2',
                    'https://jsonplaceholder.typicode.com/posts/3',
                    'https://jsonplaceholder.typicode.com/posts/4']

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

