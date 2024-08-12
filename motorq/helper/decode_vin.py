import json
import httpx
from motorq.redis_client import redis_client
async def decode_vin(vin):
    # Check if the result is in cache
    cached_result = redis_client.get(vin)
    if cached_result:
        print("=============== CACHE HIT ===============")
        return json.loads(cached_result)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json')
            response.raise_for_status()  

            data = response.json()['Results'][0]
            decoded_info = {
                'manufacturer': data['Make'],
                'model': data['Model'],
                'year': data['ModelYear']
            }

            redis_client.setex(vin, 3600, json.dumps(decoded_info))  

            return decoded_info
    except httpx.HTTPError as e:
        print('HTTP error occurred:', e)
        raise e
    except Exception as e:
        print('Error decoding VIN:', e)
        raise e

