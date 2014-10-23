# coding: utf-8
from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc
from gchart import gchart

from stats import tools

def get_ratchetctrl(request):
    mode = request.GET.get('mode', None)

    if mode == 'counter':
        ratchetctrl = request.ratchetctrl_counter
    elif mode == 'scielo':
        ratchetctrl = request.ratchetctrl
    else:
        ratchetctrl = request.ratchetctrl

    return ratchetctrl

@view_config(route_name='lines_data')
def general_lines_data(request):
    code = request.GET.get('code')
    begin = request.GET.get('begin', '0000-01-01')
    end = request.GET.get('end', '9999-12-31')
    tqx = tools.tqx_dict(request.GET.get('tqx', 'reqId:0'))

    ratchetctrl = get_ratchetctrl(request)

    if end < begin:
        raise exc.HTTPBadRequest()

    options = {}

    if not 'out' in tqx or tqx['out'] == 'gviz':
        description, data = ratchetctrl.general_article_year_month_lines_chart(
            code,
            'gviz',
            begin,
            end
        )

        chart = gchart.GChart(
            data,
            description,
            options
        )

        return Response(chart.data_table_response(req_id=tqx['reqId']), content_type='text/javascript')

    elif tqx['out'] == 'csv':
        data = ratchetctrl.general_article_year_month_lines_chart(
            code,
            'csv',
            begin,
            end
        )

        return Response(data, content_type='text/csv')

@view_config(route_name='pie_data')
def general_pie_data(request):
    code = request.GET.get('code')
    tqx = tools.tqx_dict(request.GET.get('tqx', 'reqId:0'))

    ratchetctrl = get_ratchetctrl(request)

    options = {}

    if not 'out' in tqx or tqx['out'] == 'gviz':
        description, data = ratchetctrl.general_source_page_pie_chart(
            code,
            'gviz'
        )

        chart = gchart.GChart(
            data,
            description,
            options
        )

        return Response(chart.data_table_response(req_id=tqx['reqId']), content_type='text/javascript')

    elif tqx['out'] == 'csv':
        data = ratchetctrl.general_source_page_pie_chart(
            code,
            'csv'
        )

        return Response(data, content_type='text/csv')


@view_config(route_name='lines', renderer='templates/general.mako')
def general_lines(request):
    begin = request.GET.get('begin', '0000-01-01')
    end = request.GET.get('end', '9999-12-31')
    importjs = request.GET.get('importjs', False)

    if end < begin:
        raise exc.HTTPBadRequest()

    options = {
        'legend': {'position': 'rigth'},
        'hAxis': {'title': 'Months'},
        'vAxis': {'title': 'Accesses'},
        'width': '500',
        'height': '300',
        'curveType': 'function',
        'pointSize': 5
    }

    chart = gchart.deploy(
        gchart.Line,
        '/general/lines/data/?%s' % request.query_string,
        options=options,
        importjs=True
    )

    return {'chart': chart}


@view_config(route_name='pie', renderer='templates/general.mako')
def general_pie(request):
    importjs = request.GET.get('importjs', False)

    options = {
        'legend': {'position': 'rigth'},
        'width': '500',
        'height': '300'
    }

    chart = gchart.deploy(
        gchart.Pie,
        '/general/pie/data/?%s' % request.query_string,
        options=options,
        importjs=True
    )

    return {'chart': chart}
