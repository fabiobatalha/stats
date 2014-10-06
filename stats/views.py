# coding: utf-8

from pyramid.view import view_config
import pyramid.httpexceptions as exc

from gchart import gchart


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

    description, data = request.ratchetctrl.general_article_year_month_lines_chart(
        code,
        begin,
        end
    )

    chart = gchart.deploy(
        gchart.Line,
        description,
        data,
        options,
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

    description, data = request.ratchetctrl.general_source_page_pie_chart(code)

    chart = gchart.deploy(
        gchart.Pie,
        description,
        data,
        options,
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
        description,
        data,
        options,
        importjs=True,
        render=True
    )

    return {'list': lst.decode('utf-8')}
