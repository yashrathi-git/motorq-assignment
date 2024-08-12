import httpx
async def decode_vin(vin):
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

            return decoded_info
    except httpx.HTTPError as e:
        print('HTTP error occurred:', e)
        raise e
    except Exception as e:
        print('Error decoding VIN:', e)
        raise e

