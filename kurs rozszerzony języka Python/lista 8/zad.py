import prywatne
import asyncio
import aiohttp
from aiohttp import ClientSession


apiKey = prywatne.ApiKEY

async def get_API(session, url, host, params):
    headers = {
        "X-RapidAPI-Key": apiKey,
	    "X-RapidAPI-Host":  host
    }

    async with session.get(url, headers = headers, params = params) as result:
        res = await result.json()
    return res


# (url, host, params)
data = [("https://weatherapi-com.p.rapidapi.com/current.json", "weatherapi-com.p.rapidapi.com", {"q":"51.1,17"}),
        ("https://alpha-vantage.p.rapidapi.com/query", "alpha-vantage.p.rapidapi.com", {"interval":"5min","function":"TIME_SERIES_INTRADAY","symbol":"MSFT","datatype":"json","output_size":"compact"})]

async def main():
    async with aiohttp.ClientSession() as session:
        requests = [get_API(session, url, host, params) for url,host,params in data]
        pages = await asyncio.gather(*requests)
        print(pages[0] , "\n\n" , pages[1])
        
        



asyncio.run(main())