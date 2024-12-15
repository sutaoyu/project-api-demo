def page_data_list(items: list, page_no: int, page_size: int):
    total_count = len(items)
    total_page = total_count // page_size
    if total_count % page_size != 0:
        total_page += 1
    start = (page_no - 1) * page_size
    end = page_no * page_size
    if end > total_count:
        end = total_count
    final_items = items[start:end]
    return total_page, total_count, final_items
