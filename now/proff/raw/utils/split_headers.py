import json


def convert_headers_to_dict(headers):
    result = dict()
    for header in headers.split('\n'):
        data = header.split(':')
        key = data[0].replace(' ', '')
        if not key:
            continue

        result[key] = ''.join(data[1:]).strip()

    return result


if __name__ == '__main__':
    example = '''
    Cache-Control: max-age=0, private, must-revalidate
    Content-Encoding: gzip
    Content-Security-Policy: default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' uploads.github.com www.githubstatus.com collector.githubapp.com api.github.com www.google-analytics.com github-cloud.s3.amazonaws.com github-production-repository-file-5c1aeb.s3.amazonaws.com github-production-upload-manifest-file-7fdce7.s3.amazonaws.com github-production-user-asset-6210df.s3.amazonaws.com wss://live.github.com; font-src github.githubassets.com; form-action 'self' github.com gist.github.com; frame-ancestors 'none'; frame-src render.githubusercontent.com; img-src 'self' data: github.githubassets.com identicons.github.com collector.githubapp.com github-cloud.s3.amazonaws.com *.githubusercontent.com; manifest-src 'self'; media-src 'none'; script-src github.githubassets.com; style-src 'unsafe-inline' github.githubassets.com
    Content-Type: text/html; charset=utf-8
    Date: Sat, 28 Sep 2019 03:25:21 GMT
    ETag: W/"b47940756bb1038e283a90e4dcf21a22"
    Expect-CT: max-age=2592000, report-uri="https://api.github.com/_private/browser/errors"
    Server: GitHub.com
    Set-Cookie: user_session=xPw6-loUKMfRpzDUIg3zpaLguuYTVjmWUyXHT7dHRtjOrbhB; path=/; expires=Sat, 12 Oct 2019 03:25:19 -0000; secure; HttpOnly
    Set-Cookie: __Host-user_session_same_site=xPw6-loUKMfRpzDUIg3zpaLguuYTVjmWUyXHT7dHRtjOrbhB; path=/; expires=Sat, 12 Oct 2019 03:25:19 -0000; secure; HttpOnly; SameSite=Strict
    Set-Cookie: has_recent_activity=1; path=/; expires=Sat, 28 Sep 2019 04:25:19 -0000
    Set-Cookie: _gh_sess=Q2Q0UGtLRllXSGxSbkJXKzZxc0w1MlBjNjVLU2xQR3BKandwNitiMzR6aDVFeXRQQU5zNms2YWZNTjE2MmFvb3dOQk5aL282RDhBTFJQL2FXbDBDVWEvTmpjTzM4dVhSVXB4b3JsK1JEVHJsbEkzRmZ2Z1J4bHlPRHpqbmlOVGNqemxad2w3NnFuSktrWHZlYnlKUUF6WlhBTzBERDBZdzV6K1JHZnVraE0yZjVYYXFSeEZjMzByRTdqeEhJVWJodityYm5oQ1M5aklLajBYWjR0M3VuZ0VDelQwTzRRRnBFN1ZNdzkvM1lQNTlrODBiZVl3K28wNmxPRlEyK1o2NkNQQkFhRUo2eXVFQ05oNFNieUxCT2Jub0ZkNDdRQWJZemxVNm1CUy9kRmM9LS1QMWdJbWV4OEhEaHo4OW1lUUM5L1pnPT0%3D--77fce685e2dfb28832e47a4fcdca73ed0e916937; path=/; secure; HttpOnly
    Status: 200 OK
    Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
    Transfer-Encoding: chunked
    Vary: X-PJAX
    Vary: Accept-Encoding
    X-Content-Type-Options: nosniff
    X-Frame-Options: deny
    X-GitHub-Request-Id: C1B7:662B:14F237:1E1A03:5D8ED29F
    X-Request-Id: e341e11c-b2bd-4578-8855-064d54670942
    X-XSS-Protection: 1; mode=block
    '''
    print(json.dumps(convert_headers_to_dict(example), indent=4))
