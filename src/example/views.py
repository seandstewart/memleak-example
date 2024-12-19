import asyncio

import aiohttp.web
import faker
import orjson


class SampleView(aiohttp.web.View):
    async def get(self):
        await asyncio.sleep(0)
        fake: faker.Faker = self.request.config_dict["fake"]
        data = fake.pydict(
            nb_elements=1_000,
            value_types=(str, int),
        )
        body = orjson.dumps(data)
        response = aiohttp.web.json_response(
            body=body,
        )
        return response