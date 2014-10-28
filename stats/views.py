# coding: utf-8
from pyramid.view import view_config
from pyramid.response import Response
import pyramid.httpexceptions as exc
from gchart import gchart

from stats import tools
from stats import controller

def define_mode(wrapped):
    """
        Decorator to load the selected stats controller according to the given
        mode in the query_string
    """
    @tools.check_session
    def wrapper(request, *arg, **kwargs):
        mode = request.GET.get('mode', None)

        if mode == 'counter':
            setattr(request, 'statsctrl', request.stats_counter)
        elif mode == 'scielo':
            setattr(request, 'statsctrl', request.stats_scielo)
        else:
            setattr(request, 'statsctrl', request.stats_scielo)

        return wrapped(request, *arg, **kwargs)

    wrapper.__doc__ = wrapped.__doc__

    return wrapper

@view_config(route_name='subject_area_pie_data')
@define_mode
def subject_area_pie_data(request):
    code = request.GET.get('code')

    tqx = tools.tqx_dict(request.GET.get('tqx', 'reqId:0'))

    if not 'out' in tqx or tqx['out'] == 'gviz':
        description, data = request.statsctrl.subject_area_pie_chart(
            code,
            'gviz'
        )

        chart = gchart.GChart(
            data,
            description
        )

        return Response(chart.data_table_response(req_id=tqx['reqId']), content_type='text/javascript')

    elif tqx['out'] == 'csv':
        data = request.statsctrl.subject_area_pie_chart(
            code,
            'csv'
        )

        return Response(data, content_type='text/csv')

@view_config(route_name='list_journals_data')
@define_mode
def list_journals_data(request):

    return Response('True')

@view_config(route_name='lines_data')
@define_mode
def general_lines_data(request):
    code = request.GET.get('code')
    begin = request.GET.get('begin', '0000-01-01')
    end = request.GET.get('end', '9999-12-31')
    tqx = tools.tqx_dict(request.GET.get('tqx', 'reqId:0'))

    if end < begin:
        raise exc.HTTPBadRequest()

    options = {}

    if not 'out' in tqx or tqx['out'] == 'gviz':
        description, data = request.statsctrl.general_article_year_month_lines_chart(
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
        data = request.statsctrl.general_article_year_month_lines_chart(
            code,
            'csv',
            begin,
            end
        )

        return Response(data, content_type='text/csv')

@view_config(route_name='pie_data')
@define_mode
def general_pie_data(request):
    code = request.GET.get('code')
    tqx = tools.tqx_dict(request.GET.get('tqx', 'reqId:0'))

    if not 'out' in tqx or tqx['out'] == 'gviz':
        description, data = request.statsctrl.general_source_page_pie_chart(
            code,
            'gviz'
        )

        chart = gchart.GChart(
            data,
            description
        )

        return Response(chart.data_table_response(req_id=tqx['reqId']), content_type='text/javascript')

    elif tqx['out'] == 'csv':
        data = request.statsctrl.general_source_page_pie_chart(
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

@view_config(route_name='subject_area_pie', renderer='templates/general.mako')
def subject_area_pie(request):
    importjs = request.GET.get('importjs', False)

    options = {
        'legend': {'position': 'rigth'},
        'width': '500',
        'height': '300'
    }

    chart = gchart.deploy(
        gchart.Pie,
        '/subject_area/pie/data/?%s' % request.query_string,
        options=options,
        importjs=True
    )

    return {'chart': chart}
