<%inherit file="base.mako"/>

<%block name="central_container">
  <div class="row container-fluid">
    <div class="col-md-6">
      <h4>Accesses by document type</h4>
      <iframe class="chartframebox" src="${ request.route_url('pie', _query={'mode': selected_mode, 'code': selected_code }) }" width="100%" height="320"></iframe>
      <div class="row container-fluid">
        <div class="btn-group">
          <a href="#"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="zoom chart"
            target="_blank">
              <span class="glyphicon glyphicon-zoom-in"></span>
          </a>
          <a href="${ request.route_url('pie_data', _query={'mode': selected_mode, 'code': selected_code, 'tqx':'out:csv'}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="download csv"
            target="_blank">
              <span class="glyphicon glyphicon-list"></span>
          </a>
          <a href="${ request.route_url('pie_data', _query={'mode': selected_mode, 'code': selected_code}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="JSON"
            target="_blank">
            <span class="glyphicon glyphicon-cloud-download"></span>
          </a>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="Link"
            placement="up"
            data-content="Embed this chart in you website: ${ request.route_url('pie', _query={'mode': selected_mode, 'code': selected_code }) }"
            target="_blank">
            <span class="glyphicon glyphicon-link"></span>
          </buttom>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="About"
            placement="up"
            data-content="Pizza chart with the portion of accesses of each kind of page: journal, html (fulltext), table of contents, pdf, abstract and issue."
            target="_blank">
            <span class="glyphicon glyphicon-info-sign"></span>
          </buttom>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <h4>Accesses by years and months</h4>
      <iframe class="chartframebox" src="${ request.route_url('lines', _query={'mode': selected_mode, 'code': selected_code }) }" width="100%" height="320"></iframe>
      <div class="row container-fluid">
        <div class="btn-group">
          <a href="#"
            type="button"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="zoom chart"
            target="_blank">
              <span class="glyphicon glyphicon-zoom-in"></span>
          </a>
          <a href="${ request.route_url('lines_data', _query={'mode': selected_mode, 'code': selected_code, 'tqx':'out:csv'}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="download csv"
            target="_blank">
              <span class="glyphicon glyphicon-list"></span>
          </a>
          <a href="${ request.route_url('lines_data', _query={'mode': selected_mode, 'code': selected_code}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="JSON"
            target="_blank">
            <span class="glyphicon glyphicon-cloud-download"></span>
          </a>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="Link"
            placement="up"
            data-content="Embed this chart in you website: ${ request.route_url('lines', _query={'mode': selected_mode, 'code': selected_code }) }"
            target="_blank">
            <span class="glyphicon glyphicon-link"></span>
          </buttom>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="About"
            placement="up"
            data-content="Lines chart with the accesses per year and months of a source. The source could be the entire website, a journal, issue or article."
            target="_blank">
            <span class="glyphicon glyphicon-info-sign"></span>
          </buttom>
        </div>
      </div>
    </div>
  </div>
  % if not selected_journal:
  <div class="row container-fluid">
    <div class="col-md-6">
      <h4>Accesses by subject area</h4>
      <iframe class="chartframebox" src="${ request.route_url('subject_area_pie', _query={'mode': selected_mode, 'code': selected_code }) }" width="100%" height="320"></iframe>
      <div class="row container-fluid">
        <div class="btn-group">
          <a href="#"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="zoom chart"
            target="_blank">
              <span class="glyphicon glyphicon-zoom-in"></span>
          </a>
          <a href="${ request.route_url('subject_area_pie_data', _query={'mode': selected_mode, 'code': selected_code, 'tqx':'out:csv'}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="download csv"
            target="_blank">
              <span class="glyphicon glyphicon-list"></span>
          </a>
          <a href="${ request.route_url('subject_area_pie_data', _query={'mode': selected_mode, 'code': selected_code}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="JSON"
            target="_blank">
            <span class="glyphicon glyphicon-cloud-download"></span>
          </a>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="Link"
            placement="up"
            data-content="Embed this chart in you website: ${ request.route_url('subject_area_pie', _query={'mode': selected_mode, 'code': selected_code }) }"
            target="_blank">
            <span class="glyphicon glyphicon-link"></span>
          </buttom>
          <buttom
            class="btn btn-default btn-xs"
            data-toggle="popover"
            data-placement="auto"
            title="About"
            placement="up"
            data-content="Pizza chart with the portion of accesses of each subjectarea."
            target="_blank">
            <span class="glyphicon glyphicon-info-sign"></span>
          </buttom>
        </div>
      </div>
    </div>
  </div>
  <div class="row container-fluid">
    <h4>Most accessed Journals</h4>
  </div>
  %endif # if not selected_journal
  <div class="row container-fluid">
    <h4>Most accessed Issues</h4>
  </div>
  <div class="row container-fluid">
    <h4>Most accessed Articles</h4>
  </div>
</%block>

<%block name="extra_js">
 <script type='text/javascript'>
    $(document).ready(function() {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });

    $(document).ready(function() {
        $("body").popover({ selector: '[data-toggle=popover]', container: 'body' });
    });
  </script>
</%block>
