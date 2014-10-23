 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
 <html>
  <header>
    <title>SciELO Stats</title>
    <link rel="stylesheet" href="/static/bootstrap-3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/bootstrap-3.2.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
  </header>
  <body>
    <div class="row">
      <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">
              <span class="glyphicon glyphicon-stats"></span>
              SciELO Stats
            </a>
          </div>
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Collections <span class="caret"></span></a>
                <ul class="dropdown-menu" role="menu">
                  % for acron, name in sorted(collections.items(), key=lambda x: x[1]):
                    <li role="presentation"><a role="menuitem" tabindex="-1" href="?collection=${acron}">${name}</a></li>
                  % endfor
                </ul>
              </li>
            </ul>
            <button type="submit" class="btn navbar-btn" data-toggle="modal" data-target="#journal_selector_modal">journal selector</button>
            <div class="btn-group navbar-btn navbar-right" data-toggle="buttons">
              <label class="btn btn-default ${'active' if selected_mode == 'counter' else ''}">
                <input type="radio" name="options" id="modecounter" ${'checked' if selected_mode == 'counter' else ''}>Counter
              </label>
              <label class="btn btn-default ${'active' if selected_mode == 'scielo' else ''}">
                <input type="radio" name="options" id="modescielo" ${'checked' if selected_mode == 'scielo' else ''}>SciELO
              </label>
            </div>
          </div> <!-- collapse -->
        </div> <!-- container-fluid -->
      </nav>
    </div>
    <div class="row">
      <div class="header-col level1">
        <div class="container-fluid">
            <span id="collection_name">${selected_collection}</span>
        </div>
      </div>
    </div>
    <div class="row">
      % if selected_journal:
      <div class="header-col level2">
        <div class="container-fluid">
            ${selected_journal} (${selected_journal_code})
            <a href="/?journal=clean" class="btn btn-default btn-xs navbar-right">remove</span></a>
        </div>
      </div>
      % endif
    </div>
    <div class="row">
      <nav class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
          <ul class="nav navbar-nav">
            <li class="${'active' if page == 'accesses' else ''}"><a href="${request.route_url('accesses')}">Accesses</a></li>
            <li class="${'active' if page == 'production' else ''}"><a href="${request.route_url('production')}">Production</a></li>
            <li class="${'active' if page == 'bibliometrics' else ''}"><a href="${request.route_url('bibliometrics')}">Bibliometrics</a></li>
          </ul>
        </div> <!-- div container-fluid -->
      </nav>
    </div> <!-- div row -->
    <div class="row container-fluid">
      <%block name="central_container" />
    </div><!-- div row -->
    <div class="modal fade" id="journal_selector_modal" tabindex="-1" role="dialog" aria-labelledby="journal_selector_modal" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
            <h4 class="modal-title" id="myModalLabel">Journal Selector</h4>
          </div>
          <form role="form" method="GET">
            <div class="modal-body">
                Select a Journal:
                <select class="form-control" name="journal">
                  % for issn, xylose_journal in sorted(journals.items(), key=lambda x: x[1].title):
                    <option value="${issn}">${xylose_journal.title}</option>
                  % endfor
                </select>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Select</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <script src="/static/jquery-1.11.1/jquery-1.11.1.min.js"></script>
    <script src="/static/bootstrap-3.2.0/js/bootstrap.min.js"></script>
    <script>
      $('#modescielo').change(function () {
        $.get("${request.route_url('ajx_toggle_mode', _query={'mode': 'scielo'})}", function (){
          location.reload();  
        });
      });
      $('#modecounter').change(function () {
        $.get("${request.route_url('ajx_toggle_mode', _query={'mode': 'counter'})}", function (){
          location.reload();
        });
      });
    </script>
    <%block name="extra_js" />
  </body>
</html>