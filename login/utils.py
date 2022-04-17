import pprint

from aiogoogle import Aiogoogle


async def list_contacts(user_creds, client_creds):
    aiogoogle = Aiogoogle(user_creds=user_creds, client_creds=client_creds)
    people_v1 = await aiogoogle.discover("people", "v1")

    contacts_list = []

    def append_connections(connections):
        for connection in connections:
            phone_nums = connection.get("phoneNumbers")
            if phone_nums:
                num = phone_nums[0].get("canonicalForm")
            else:
                num = None

            if "names" not in connection:
                name = ""
            else:
                name = connection["names"][0]["displayName"]
            contacts_list.append({name: num})

    async with aiogoogle:
        pages = await aiogoogle.as_user(
            people_v1.people.connections.list(
                resourceName="people/me", personFields="names,phoneNumbers"
            ),
            full_res=True,
        )
    async for page in pages:
        append_connections(page["connections"])

    # pprint.pprint(contacts_list)
    # print("Length:")
    # print(len(contacts_list))
    return contacts_list
