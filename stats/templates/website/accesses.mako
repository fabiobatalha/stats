<%inherit file="base.mako"/>

<%block name="central_container">
  <div class="row container-fluid">
    <div class="col-md-6">
      <iframe class="chartframebox" src="${pie}" width="100%" height="320"></iframe>
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
          <a href="${ request.route_url('pie_data', _query={'mode': selected_mode, 'code': selected_collection_code, 'tqx':'out:csv'}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="download csv"
            target="_blank">
              <span class="glyphicon glyphicon-list"></span>
          </a>
          <a href="${ request.route_url('pie_data', _query={'mode': selected_mode, 'code': selected_collection_code}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="JSON"
            target="_blank">
            <span class="glyphicon glyphicon-cloud-download"></span>
          </a>
        </div>
      </div>
    </div>
    <div class="col-md-6">
      <iframe class="chartframebox" src="${lines}" width="100%" height="320"></iframe>
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
          <a href="${ request.route_url('lines_data', _query={'mode': selected_mode, 'code': selected_collection_code, 'tqx':'out:csv'}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="download csv"
            target="_blank">
              <span class="glyphicon glyphicon-list"></span>
          </a>
          <a href="${ request.route_url('lines_data', _query={'mode': selected_mode, 'code': selected_collection_code}) }"
            class="btn btn-default btn-xs"
            data-toggle="tooltip"
            data-placement="top"
            title="JSON"
            target="_blank">
            <span class="glyphicon glyphicon-cloud-download"></span>
          </a>
        </div>
      </div>
    </div>
  </div>
</%block>

<%block name="extra_js">
 <script type='text/javascript'>
    $(document).ready(function() {
        $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    });
  </script>
</%block>
