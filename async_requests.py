import aiohttp
import asyncio
import async_timeout


# python > 3.5 syntax
# async def fetch(session, url):
@asyncio.coroutine
def fetch(session, url):
    with async_timeout.timeout(10):
        # return generator until session completes get request
        # python 3.5 syntax
        # response = await session.get(url)
        response = yield from session.get(url)
        # then return another generator until we have content
        # python 3.5 syntax
        # return response, await response.text()
        return response, (yield from response.text())

# python > 3.5 syntax
# async def get_url(url):
@asyncio.coroutine
def get_url(url):
    # python > 3.5 syntax
    # async with aiohttp.ClientSession(
    with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        print('Making url call to: {}'.format(url))
        # will return generators until both resp and content have been fetched
        resp, html = yield from fetch(session, url)
        # This code only runs once we have both resp and content
        print('Got html for url: {}'.format(url))
        return resp


def test_async_request(url):
    # Return a generator from get_url that the event loop will 
    # call once data has returned from aiohttp
    resp = yield from get_url(url)
    # This code only runs once we have complete resp yield will skip over it 
    # like regular generator functionality
    if resp.status == 200:
        print('Request successfull.')
    return resp
    

if __name__ == '__main__':
    url_list = [
            'http://www.reddit.com/',
            'http://www.reddit.com/',
            'http://www.reddit.com/',
            'http://www.reddit.com/',
            ]
    tasks = []
    for url in url_list:
        tasks.append(asyncio.ensure_future(test_async_request(url)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))