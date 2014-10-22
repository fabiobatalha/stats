 <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
 <html>
  <header>
    <title>SciELO Stats</title>
    <link rel="stylesheet" href="/static/bootstrap-3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/bootstrap-3.2.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="/static/css/style.css">
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
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
            <form class="navbar-form navbar-left" role="search">
              <div class="form-group">
                <input type="text" class="form-control" placeholder="Journal Name">
              </div>
              <button type="submit" class="btn btn-default">select</button>
            </form>
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
            Journal Name
            <a href="#" class="btn btn-default btn-xs navbar-right">remove</span></a>
        </div>
      </div>
      % endif
    </div>
    <div class="row">
      <nav class="navbar navbar-default" role="navigation">
        <div class="container-fluid">
          <ul class="nav navbar-nav">
            <li><a href="/w/accesses/">Acessos</a></li>
            <li><a href="/w/production/">Produção</a></li>
            <li><a href="/w/bibliometrics/">Bibliometria</a></li>
          </ul>
        </div> <!-- div container-fluid -->
      </nav>
    </div> <!-- div row -->
    <div class="row">
      <div class="container-fluid">
        <%block name="central_container" />
      </div> <!-- div container-fluid -->
    </div><!-- div row -->
    <script src="/static/jquery-1.11.1/jquery-1.11.1.min.js"></script>
    <script src="/static/bootstrap-3.2.0/js/bootstrap.min.js"></script>
    <script>
      $('#modescielo').change(function () {
        $.get("/ajx/toggle_mode/?mode=scielo", function (){
          location.reload();  
        });
      });
      $('#modecounter').change(function () {
        $.get("/ajx/toggle_mode/?mode=counter", function (){
          location.reload();
        });
        location.reload();
      });
    </script>
    <%block name="extra_js" />
  </body>
</html>