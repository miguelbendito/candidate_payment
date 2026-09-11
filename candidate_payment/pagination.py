def paginated_results(fetch_page_fn, page_size=100):
    page = 1
    while True:
        data = fetch_page_fn(page=page, page_size=page_size)
        if not data:  # empty page = done
            break
        yield from data
        if len(data) < page_size:  # last page was partial, stop
            break
        page += 1