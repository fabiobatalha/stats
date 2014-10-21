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
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Argentina</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Brazil</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Chile</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Colombia</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Costa Rica</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Cuba</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Portugal</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Spain</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">South Africa</a></li>
                  <li role="presentation"><a role="menuitem" tabindex="-1" href="#">Venezuela</a></li>
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
              <label class="btn btn-default active">
                <input type="radio" name="options" id="option1" checked> Counter
              </label>
              <label class="btn btn-default">
                <input type="radio" name="options" id="option2"> SciELO
              </label>
            </div>
          </div> <!-- collapse -->
        </div> <!-- container-fluid -->
      </nav>
    </div>
    <div class="row">
      <div class="header-col level1">
        <div class="container-fluid">
            Brazil
        </div>
      </div>
    </div>
    <div class="row">
      <div class="header-col level2">
        <div class="container-fluid">
            Revista de Saúde Pública
        </div>
      </div>
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
  </body>
</html>