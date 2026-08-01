from fastapi import APIRouter, File, UploadFile

import cloudinary.uploader

import app.core.cloudinary_config

router = APIRouter(
    prefix="/api/uploads",
    tags=["uploads"]
)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...)
):

    result = cloudinary.uploader.upload(
        file.file,
        folder="mercadoliebre/products"
    )

    return {
        "url": result["secure_url"]
    }