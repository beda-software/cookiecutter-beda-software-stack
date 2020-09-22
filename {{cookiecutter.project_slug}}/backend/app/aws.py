import datetime

from aiohttp import web

from app import config
from app.contrib.amazon import generate_aws_signed_url
from app.fhirdate import get_now
from app.sdk import sdk


@sdk.operation(
    ["POST"],
    ["$aws-signed-upload"],
    public=True
)
async def operation_singed_upload(operation, request):
    resource = request["resource"]
    file_name = resource['fileName'].split(".")
    extension = file_name[-1]
    file_name[-1] = str(datetime.datetime.now().timestamp())
    file_name.append(extension)
    file_name = ".".join(file_name)
    now = get_now()
    object_name = "uploads/{year}/{month}/{day}/{file_name}".format(
        file_name=file_name, year=now.year, month=now.month, day=now.day)
    object_url = "https://{bucket}.s3.amazonaws.com/{object_name}".format(
        bucket=config.aws_bucket, object_name=object_name)
    signed_url = generate_aws_signed_url(
        config.aws_access_key_id,
        config.aws_secret_access_key,
        config.aws_bucket,
        object_name,
        3600,
        resource['contentType'],
        resource['method'],
    )

    return web.json_response({
        "signedUploadUrl": signed_url,
        "objectUrl": object_url,
        "fileName": file_name})


def get_signed_download_url(url):
    parts = url.split("https://{bucket}.s3.amazonaws.com/".format(
        bucket=config.aws_bucket))
    if len(parts) == 2:
        signed_url = generate_aws_signed_url(
            config.aws_access_key_id,
            config.aws_secret_access_key,
            config.aws_bucket,
            parts[1],
            3600)
        return signed_url
    return url


@sdk.operation(
    ["POST"],
    ["$aws-signed-download"],
    public=True
)
async def operation_singed_download(operation, request):
    # TODO: use get_signed_download_url
    resource = request["resource"]
    url = resource['url']
    parts = url.split("https://{bucket}.s3.amazonaws.com/".format(
        bucket=config.aws_bucket))
    if len(parts) == 2:
        signed_url = generate_aws_signed_url(
            config.aws_access_key_id,
            config.aws_secret_access_key,
            config.aws_bucket,
            parts[1],
            3600)
        return web.json_response({
            "signedUploadUrl": signed_url,
        })

    return web.json_response({
    "signedUploadUrl": url
    })
