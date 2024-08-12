import requests

url = "https://jobs.lever.co/kandji"

payload = {
    "url": "<string>",
    "crawlerOptions": {
        "includes": ["<string>"],
        "excludes": ["<string>"],
        "generateImgAltText": True,
        "returnOnlyUrls": True,
        "maxDepth": 123,
        "mode": "default",
        "ignoreSitemap": True,
        "limit": 123,
        "allowBackwardCrawling": True,
        "allowExternalContentLinks": True
    },
    "pageOptions": {
        "headers": {},
        "includeHtml": True,
        "includeRawHtml": True,
        "onlyIncludeTags": ["<string>"],
        "onlyMainContent": True,
        "removeTags": ["<string>"],
        "replaceAllPathsWithAbsolutePaths": True,
        "screenshot": True,
        "fullPageScreenshot": True,
        "waitFor": 10000
    }
}
headers = {
    "Authorization": "Bearer fc-089e85d9f80b477884cd8e5b9b92c79e",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)