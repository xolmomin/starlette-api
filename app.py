from models import Contact
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette import status
from uvicorn.main import run
from starlette.schemas import SchemaGenerator

from tortoise.contrib.starlette import register_tortoise

app = Starlette()

schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)


@app.route("/contact", methods=['GET', 'POST'])
async def list_all_and_create(request: Request) -> JSONResponse:
    if request.method == "POST":
        try:
            data = await request.json()
            name = data['name']
            phone = data['phone']
        except:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "cannot find name or phone")

        contact = await Contact.create(name=name, phone=phone)
        return JSONResponse({"contact": str(contact)}, status.HTTP_201_CREATED)
    else:
        contacts = await Contact.all()
        return JSONResponse({"users": [str(contact) for contact in contacts]})


@app.route("/contact/{id}", methods=['GET', 'DELETE', 'PUT', 'PATCH'])
async def add_user(request: Request) -> JSONResponse:
    try:
        contact = await Contact.filter(id=request.path_params.get('id')).first()
    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "id not found")

    if request.method == 'GET':
        return JSONResponse({"contact": str(contact)}, status.HTTP_200_OK)

    if request.method == 'DELETE':
        await contact.delete()
        return JSONResponse({"message": "contact successfully deleted!"}, status.HTTP_200_OK)

    if request.method == 'PUT' or request.method == 'PATCH':
        data = await request.json()
        await contact.update_from_dict(data)
        return JSONResponse({"contact": str(contact)}, status.HTTP_200_OK)


register_tortoise(
    app, db_url="sqlite://db.sqlite3", modules={"models": ["models"]}, generate_schemas=True
)

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8001)

# get - /contacts (list of contacts)
# post -  /contacts (create contact)
# get - /contacts/{id} (get one contact)
# delete - /contacts/{id} (delete contact)
# patch/update - contacts/{id} update contact
