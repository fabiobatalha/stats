# coding: utf-8
import json

from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc

from gchart import gchart


@view_config(route_name='lines_data')
def general_lines_data(request):

    code = request.GET.get('code')
    begin = request.GET.get('begin', '0000-01-01')
    end = request.GET.get('end', '9999-12-31')
    tqx = request.GET.get('tqx', 'reqId:0')

    req_id = tqx.split(':')[1]

    if end < begin:
        raise exc.HTTPBadRequest()

    options = {}

    description, data = request.ratchetctrl.general_article_year_month_lines_chart(
        code,
        begin,
        end
    )

    chart = gchart.GChart(
        data,
        description,
        options
    )

    return Response(chart.data_table_response(req_id=req_id), content_type='text/javascript')


@view_config(route_name='pie_data')
def general_pie_data(request):

    code = request.GET.get('code')
    tqx = request.GET.get('tqx', 'reqId:0')

    req_id = tqx.split(':')[1]

    options = {}

    description, data = request.ratchetctrl.general_source_page_pie_chart(code)

    chart = gchart.GChart(
        data,
        description,
        options
    )

    return Response(chart.data_table_response(req_id=req_id), content_type='text/javascript')

@view_config(route_name='lines', renderer='templates/general.mako')
def general_lines(request):

    code = request.GET.get('code')
    begin = request.GET.get('begin', '0000-01-01')
    end = request.GET.get('end', '9999-12-31')

    if end < begin:
        raise exc.HTTPBadRequest()

    options = {
        'title': 'fulltext and abstract accesses',
        'legend': {'position': 'rigth'},
        'hAxis': {'title': 'Months'},
        'vAxis': {'title': 'Accesses'},
        'width': '100%',
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

    code = request.GET.get('code')

    options = {
        'title': 'page source',
        'legend': {'position': 'rigth'},
        'width': '100%'
    }

    chart = gchart.deploy(
        gchart.Pie,
        '/general/pie/data/?%s' % request.query_string,
        options=options,
        importjs=True
    )

    return {'chart': chart}


@view_config(route_name='journals_list', renderer='templates/journals_list.mako')
def journals_list(request):

    options = {
        'title': 'fulltext and abstract accesses',
        'allowHtml': True,
        'page': 'enable',
        'pageSize': 20,
        'width': '100%',
        'showRowNumber': True,
        'sortColumn': 7,
        'sortAscending': False
    }

    description, data = request.ratchetctrl.journals_list()

    lst = gchart.deploy(
        gchart.List,
        '/general/lines/data/?%s' % request.query_string,
        options=options,
        importjs=True
    )

    return {'list': lst.decode('utf-8')}
