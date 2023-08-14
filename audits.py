def third_party_summary(audits):
    data = audits['details']
    wasted_bytes = data['summary']['wastedBytes']
    wasted_ms = data['summary']['wastedMs']
    is_entity_grouped = data['isEntityGrouped']
    type_value = data['type']

    print("Общая информация:")
    print("Wasted Bytes:", wasted_bytes)
    print("Wasted Ms:", wasted_ms)
    print("Is Entity Grouped:", is_entity_grouped)
    print("Type:", type_value)

    # Извлечение информации по каждому subItem
    items = data['items']
    for item in items:
        entity = item['entity']
        transfer_size = item['transferSize']
        blocking_time = item['blockingTime']
        main_thread_time = item['mainThreadTime']
        print("\nИнформация по ресурсу:", entity)
        print("Transfer Size:", transfer_size)
        print("Blocking Time:", blocking_time)
        print("Main Thread Time:", main_thread_time)
        sub_items = item['subItems']['items']
        print("Подресурсы:")
        for sub_item in sub_items:
            sub_transfer_size = sub_item.get('transferSize', 'N/A')
            sub_url = sub_item.get('url', 'N/A')
            sub_blocking_time = sub_item.get('blockingTime', 'N/A')
            sub_main_thread_time = sub_item.get('mainThreadTime', 'N/A')
            print("  Ресурс:", sub_url)
            print("  Transfer Size:", sub_transfer_size)
            print("  Blocking Time:", sub_blocking_time)
            print("  Main Thread Time:", sub_main_thread_time)


def total_byte_weight(audits):
    items = audits['details']['items']
    for item in items:
        transfer_size = item['totalBytes']
        url = item['url']
        print('URL:', url)
        print("Transfer Size:", transfer_size)


def duplicated_javascript(audits):
    items = audits['details']['items']
    for item in items:
        source = item['source']
        wasted_bytes = item['wastedBytes']
        sub_items = item['subItems']['items']
        print(source, 'Potential Savings:', wasted_bytes)
        for sub_item in sub_items:
            source_transfer_bytes = sub_item.get('sourceTransferBytes')
            url = sub_item['url']
            print('    ', url, 'Transfer Size:', source_transfer_bytes)


def non_composited_animations(audits):
    items = audits['details']['items']
    for item in items:
        snippet = item['node']['snippet']
        sub_items = item['subItems']['items']
        result = {
            'Element': snippet,
            'sub_items': sub_items,
        }
        print(snippet)
        for sub_item in sub_items:
            failure_reason = sub_item['failureReason']
            animation = sub_item['animation']
            print('    ', failure_reason, animation)


def critical_request_chains(audits):
    chains = audits['details']['chains']
    for chain, data_chain in chains.items():
        chain_name = data_chain['request']['url']
        time = data_chain['request']['endTime'] - data_chain['request']['startTime']
        print('maximum delay: ', round(time * 1000, 3), 'msec')
        print(chain_name)
        children = data_chain['children']
        for item, data in children.items():
            url = data['request']['url']
            transfer_size = data['request']['transferSize']
            time = data['request']['endTime'] - data['request']['startTime']
            print('    ', url, transfer_size, 'Byte', round(time * 1000, 3), 'msec')


def unused_css_rules(audits):
    """Avoid chaining critical requests"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        transfer_size = item['totalBytes']
        potential_savings = item['wastedBytes']
        result = {'URL': url, 'Transfer Size': transfer_size, 'Potential Savings': potential_savings}
        print(url, 'Transfer Size:', transfer_size, 'Potential Savings:', potential_savings)


def modern_image_formats(audits):
    """Serve images in next-gen formats"""
    items = audits['details']['items']
    for item in items:
        node = item['node']['snippet']
        image_url = item['url']
        total_bytes = item['totalBytes']
        wasted_bytes = int(item['wastedBytes'])
        result = {node, image_url, 'Resource Size:', total_bytes, 'Potential Savings:', wasted_bytes}
        print(node, image_url, 'Resource Size:', total_bytes, 'Potential Savings:', wasted_bytes)

# TODO
def uses_passive_event_listeners(audits):
    """Uses passive listeners to improve scrolling performance"""


def largest_contentful_paint_element(audits):
    """Largest Contentful Paint element"""
    items = audits['details']['items']
    for item in items:
        if item['headings'][0]['key'] == 'node':
            for sub_item in item['items']:
                node_label = sub_item['node']['nodeLabel']
                snippet = sub_item['node']['snippet']

                print(node_label, snippet)
        elif item['headings'][0]['key'] == 'phase':
            for sub_item in item['items']:
                phase = sub_item['phase']
                percent = sub_item['percent']
                timing = int(sub_item['timing'])  # msec
                result = {'Phase': phase, '% of LCP': percent, 'Timing': timing}
                print(result)


def unsized_images(audits):
    """Image elements do not have explicit `width` and `height`"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        node = item['node']['nodeLabel']
        selector = item['node']['selector']
        result = {'url_image': url, 'node': node, 'selector': selector}
        print(result)


def lcp_lazy_loaded(audits):
    """Largest Contentful Paint image was not lazily loaded"""
    items = audits['details']['items']
    for item in items:
        snippet = item['node']['snippet']
        selector = item['node']['selector']
        result = {'snippet': snippet, 'selector': selector}
        print(result)

# TODO
def unminified_css(audits):
    """Minify CSS"""


def dom_size(audits):
    """Avoid an excessive DOM size"""
    items = audits['details']['items']
    for item in items:
        statistic = item['statistic']
        value = item['value'] and item['value']['value']
        node_label = item.get('node', {}).get('nodeLabel')
        snippet = item.get('node', {}).get('snippet')
        result = {'statistic': statistic, 'node_label': node_label, 'snippet': snippet, 'value': value}
        print(result)


def font_display(audits):
    """All text remains visible during webfont loads"""
    items = audits['details']['items']


def uses_text_compression(audits):
    """Enable text compression"""
    items = audits['details']['items']


def uses_rel_preload(audits):
    """Preload key requests"""
    items = audits['details']['items']


def user_timings(audits):
    """User Timing marks and measures"""
    items = audits['details']['items']
    for item in items:
        name = item['name']
        timing_type = item['timingType']
        start_time = item['startTime']
        duration = item['duration']
        result = {'Name': name, 'Type': timing_type, 'Start Time': start_time, 'Duration': duration}
        print(result)


def uses_rel_preconnect(audits):
    """Preconnect to required origins"""


def unminified_javascript(audits):
    """'Minify JavaScript"""


def bootup_time(audits):
    """JavaScript execution time"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        result = {
            'URL': item['url'],
            'Total CPU Time': item['total'],
            'Script Evaluation': item['scripting'],
            'Script Parse': item['scriptParseCompile'],
        }
        print(result)


def uses_responsive_images(audits):
    """Properly size images"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        result = {
            'URL': item['url'],
            'Selector': item['node']['selector'],
            'Resource Size': item['totalBytes'],
            'Potential Savings': item['wastedBytes'],
        }
        print(result)


def render_blocking_resources(audits):
    """Eliminate render-blocking resources"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        result = {
            'URL': item['url'],
            'Transfer Size': item['totalBytes'],
            'Potential Savings': item['wastedMs'],
        }
        print(result)


def metrics(audits):
    """Collects all available metrics."""
    items = audits['details']['items'][0]
    for k_item, v_item in items.items():
        result = {k_item: v_item}
        print(k_item, v_item)  # millisecond


def uses_optimized_images(audits):
    """Efficiently encode images"""
    items = audits['details']['items']


def no_document_write(audits):
    """Avoids `document.write()`"""
    items = audits['details']['items']


def third_party_facades(audits):
    """Lazy load third-party resources with facades"""
    items = audits['details']['items']


def mainthread_work_breakdown(audits):
    """Minimize main-thread work"""
    items = audits['details']['items']
    for item in items:
        group_label = item['groupLabel']
        duration = int(item['duration'])

        result = {
            'Category': group_label,
            'Time Spent, ms': duration,
        }
        print(result)


def unused_javascript(audits):
    """Reduce unused JavaScript"""
    items = audits['details']['items']
    for item in items:
        url = item['url']
        total_bytes = item['totalBytes']
        wasted_bytes = item['wastedBytes']

        result = {
            'url': url,
            'Transfer Size': total_bytes,
            'Potential Savings': wasted_bytes,
        }
        print(result)


def server_response_time(audits):
    """Initial server response time was short"""

dict_audits = {
    'third-party-summary': third_party_summary,
    'total-byte-weight': total_byte_weight,
    'duplicated-javascript': duplicated_javascript,
    'non-composited-animations': non_composited_animations,
    'critical-request-chains': critical_request_chains,
    'unused-css-rules': unused_css_rules,
    'unused-javascript': unused_javascript,
    'modern-image-formats': modern_image_formats,
    'uses-passive-event-listeners': uses_passive_event_listeners,  # TODO
    'largest-contentful-paint-element': largest_contentful_paint_element,
    'unsized-images': unsized_images,
    'lcp-lazy-loaded': lcp_lazy_loaded,
    'unminified-css': unminified_css,  # TODO
    'dom-size': dom_size,
    'font-display': font_display,  # TODO
    'uses-text-compression': uses_text_compression,  # TODO
    'uses-rel-preload': uses_rel_preload,  # TODO
    # 'performance-budget':
    'user-timings': user_timings,
    'uses-rel-preconnect': uses_rel_preconnect,  # TODO
    'unminified-javascript': unminified_javascript,  # TODO
    'uses-optimized-images': uses_optimized_images,  # TODO
    # 'timing-budget': timing_budget,
    'bootup-time': bootup_time,
    'uses-responsive-images': uses_responsive_images,
    'render-blocking-resources': render_blocking_resources,
    'metrics': metrics,
    'no-document-write': no_document_write,  # TODO
    'third-party-facades': third_party_facades,  # TODO
    'mainthread-work-breakdown': mainthread_work_breakdown,  # TODO
    'server-response-time': server_response_time,
}
